from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.db import transaction
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.db.models import F
from django.http import JsonResponse
from django import views
from blog import forms
from blog import models
from bs4 import BeautifulSoup
from utils import page, verification_code, geetest
import datetime
import os


# Create your views here.
def index(request):
    if request.method == 'GET':
        # 查询所有用户的信息+分页信息
        article_amount = models.Article.objects.count()
        url = request.path_info
        # 当前页码
        current_page = request.GET.get('page', 1)
        page_html, articles = get_page_articles(current_page, article_amount, url)

        return render(request, "index.html", {
            "articles": articles,
            "page_html": page_html,
        })


def home(request, user_id, *args):
    # print(user_id,args[0],args[1])
    if request.method == 'GET':
        user = get_object_or_404(models.UserInfo, id=user_id)
        # 分类信息交给组件模板去处理
        # 这里处理该博客的文章列表
        # 查询所有用户的信息+分页信息
        article_list = models.Article.objects.filter(user_id=user_id)
        if args:
            if args[0] == "category":
                article_list = article_list.filter(category__id=args[1])
            elif args[0] == "tag":
                article_list = article_list.filter(tags__id=args[1])
            else:
                try:
                    year, month = args[1].split('-')
                    article_list = article_list.filter(create_time__year=year, create_time__month=month)
                except Exception as e:
                    article_list = []
        print("article_list = ", article_list)
        url = request.path_info
        article_amount = article_list.count()
        # 当前页码
        current_page = request.GET.get('page', 1)
        page_html, articles = get_page_articles(current_page, article_amount, url, article_list=article_list,
                                                is_article=1)

        return render(request, "home.html", {
            'user': user,
            "page_html": page_html,
            "articles": articles,
        })


def article(request, user_id, article_id):
    if request.method == 'GET':
        user = get_object_or_404(models.UserInfo, id=user_id)
        article = models.Article.objects.filter(id=article_id, user_id=user_id).first()
        # 获取评论消息 没有登录不查询评论信息
        comments = ""
        if request.user.is_authenticated():
            comments = article.comment_set.all()

        return render(request, "article.html", {"user": user, "article": article, 'comments': comments})


# 用于获取分页+文章数据
def get_page_articles(current_page, article_amount, url_prefix, per_page_data=2, page_show_tags=9, article_list=None,
                      is_article=0):
    page_object = page.MyPage(current_page, article_amount, url_prefix=url_prefix, per_page_data=per_page_data,
                              page_show_tags=page_show_tags)
    page_html = page_object.html
    article_start = page_object.start
    article_end = page_object.end

    if is_article:
        article_list = article_list[article_start:article_end]
    else:
        article_list = models.Article.objects.all()[article_start:article_end]

    return page_html, article_list


# 点赞功能
def thumbs_up(request):
    ret = {"code": 0}
    if request.user.is_authenticated():
        user_id = request.user.id
        article_user_id = request.POST.get("user_id")
        article_id = request.POST.get("article_id")
        is_up = request.POST.get("is_up",0)

        print("is_up = ",is_up)

        if str(article_user_id) == str(user_id):
            ret["code"] = 2

            if int(is_up):
                ret["error"] = "不能给自己点赞！"
            else:
                ret["error"] = "不能给自己反对！"
        else:
            try:
                with transaction.atomic():
                    article = models.Article.objects.filter(user_id=article_user_id, id=article_id).first()

                    if is_up:
                        article_up_down = models.ArticleUpDown(user_id=user_id, article_id=article_id, is_up=True)
                        article_up_down.save()
                        up_count = article.up_count + 1
                        article.up_count = up_count
                        article.save()

                        ret["type"] = 'up'
                        ret["up_down_num"] = up_count
                    else:
                        article_up_down = models.ArticleUpDown(user_id=user_id, article_id=article_id, is_up=False)
                        article_up_down.save()
                        # article.update(up_down=F("down_count") + 1)

                        down_count = article.down_count + 1
                        article.down_count = down_count
                        article.save()

                        ret["type"] = 'down'
                        ret["up_down_num"] = down_count

                    ret["code"] = 1

            except Exception as e:
                print(e)
                ret["code"] = 3
                ret["error"] = "只能给文章点赞或反对一次！"
    else:
        ret["code"] = 4
        ret["error"] = "登录后，才能给用户文章点赞和评论！"

    return JsonResponse(ret)


class Comment(views.View):
    def get(self, request, article_id):
        res = {"code": 1}
        comment_list = models.Comment.objects.filter(article_id=article_id)
        data = [{
            "id": comment.id,
            "create_time": comment.create_time,
            "content": comment.content,
            "pid": comment.parent_comment_id,
            "username": comment.user.username} for comment in comment_list]
        res['data'] = comment_list
        return JsonResponse(res)


# 评论功能
@login_required(login_url="/login/")
def comment(request):
    if request.method == 'POST':
        # 添加评论到评论表，更新文章表，使用事物
        user_id = request.POST.get("user_id")
        reviewer_id = request.POST.get("reviewer_id")
        content = request.POST.get("content")
        article_id = request.POST.get("article_id")
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 父级评论
        parent_comment_id = request.POST.get("parent_comment_id", "")
        res = {"code": 0}

        try:
            with transaction.atomic():
                article_obj = models.Article.objects.filter(id=article_id, user_id=user_id).update(
                    comment_count=F("comment_count") + 1)
                comment_obj = models.Comment.objects.create(article_id=article_id, user_id=reviewer_id, content=content,
                                                            create_time=create_time,
                                                            parent_comment_id=parent_comment_id)

                if user_id == reviewer_id:
                    res["build_owner"] = '<span>[楼主]</span>'
                else:
                    res['build_owner'] = ''

                # if parent_comment_id != "":
                #     content = '@' + comment_obj.user.username + content

                res['code'] = 1
                res['content'] = content
                print("article_obj = ", article_obj)
                res["comment_count"] = models.Article.objects.get(id=article_id, user_id=user_id).comment_count
                res['create_time'] = comment_obj.create_time
                res['user_id'] = user_id
                res['comment_id'] = comment_obj.id
                res['reviewer_id'] = request.user.id
                res['username'] = request.user.username

                print("=======res =========", res)

        except Exception as e:
            res['error'] = "评论内容: 此次评论失败！"
            res["code"] = 2

        return JsonResponse(res)


# Create your views here.
class Login(views.View):
    def get(self, request):
        login_obj = forms.LoginForm()
        return render(request, "login_slide_validate.html", {"login_obj": login_obj})

    def post(self, request):
        res = {"code": 0}
        username = request.POST.get("username")
        password = request.POST.get("password")
        v_code = request.POST.get("v_code").upper()
        print("login = ", username, password)
        print("login = ", v_code, request.session.get("v_code"))
        if v_code != request.session.get("v_code"):
            res = {"code": 2}
        else:
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                res = {"code": 1}
        return JsonResponse(res)


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# #请在官网申请ID使用，示例ID不可使用
# pc_geetest_id = "aaa60418dc158715b1eb902edf8db210"
# pc_geetest_key = "1cf2ef1ca367555e5efd30861c499a38"

def pcgetcaptcha(request):
    user_id = 'test'
    gt = geetest.GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def login_slide_validate(request):
    if request.method == "POST":
        res = {"code": 0}
        gt = geetest.GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        if result:
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username, password)
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                res = {"code": 1}
        else:
            res["code"] = 0
        return JsonResponse(res)

    login_obj = forms.LoginForm()
    return render(request, "login_slide_validate.html", {"login_obj": login_obj})


@login_required(login_url="/index/")
def logout(request):
    auth.logout(request)
    return redirect("/index/")


# @never_cache
def v_code(request):
    v_code_img, v_code_str = verification_code.random_verificate_code_img()
    request.session['v_code'] = v_code_str.upper()
    request.session.set_expiry(0)
    return HttpResponse(v_code_img, content_type="img/png")


class RegView(views.View):
    def get(self, request):
        reg_obj = forms.RegisterForm()
        return render(request, "register.html", {"reg_obj": reg_obj})

    def post(self, request):
        res = {"code": 0}
        v_code = request.POST.get("v_code", '1').upper()
        print("v_code = ", v_code)
        print(request.session.get("v_code", ""))
        if v_code != request.session.get("v_code", ""):
            res["code"] = 2
            res["error"] = "验证码错误！"
        else:
            reg_obj = forms.RegisterForm(request.POST)
            if reg_obj.is_valid():
                reg_obj.cleaned_data.pop("rep_password")

                avatar = request.FILES.get("avatar")
                models.UserInfo.objects.create_user(**reg_obj.cleaned_data, avatar=avatar)

                res["code"] = 1
                res["error"] = "注册成功！"
            else:
                res["code"] = 3
                res["error"] = reg_obj.errors

        return JsonResponse(res)


def article_edit(request):
    return render(request, "article_edit.html")


#后台
@login_required(login_url="/login_slide_validate/")
def backend(request):
    #获取当前用户的所有文章
    articles = models.Article.objects.filter(user=request.user)
    return render(request,"backend.html",{"articles":articles})


#添加新文章
@login_required(login_url="/login_slide_validate/")
def add_article(request):

    print("add_article ============================================")
    print(request.POST)

    if request.method == 'POST':
        #获取用户填写的文章内容
        is_update = int(request.POST.get("is_update",0))
        atricle_id = request.POST.get("atricle",0)

        print(is_update,atricle_id,type(is_update))

        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")

        # 清洗用户发布的文章的内容，去掉script标签
        soup = BeautifulSoup(content, "html.parser")
        script_list = soup.select("script")
        for i in script_list:
            i.decompose()

        if is_update:
            print("add_article update ============================================",is_update)
            with transaction.atomic():
                #先创建文章记录
                models.Article.objects.filter(id=atricle_id).update(
                    title=title,
                    desc = soup.text[0:150],
                    category_id=category_id
                )
                #2.创建文章详情记录
                models.ArticleDetail.objects.filter(article_id=atricle_id).update(
                    content=soup.prettify(),
                )
        else:
            print("add_article create ============================================")
            # print(soup.text)
            # print(soup.prettify())
            #写入数据库
            with transaction.atomic():
                #先创建文章记录
                article_obj = models.Article.objects.create(
                    title=title,
                    desc = soup.text[0:150],
                    user=request.user,
                    category_id=category_id
                )
                #2.创建文章详情记录
                models.ArticleDetail.objects.create(
                    content=soup.prettify(),
                    article=article_obj
                )
        return redirect('/blog/backend/')

    #把当前博客的文章分类查询出来
    categories = models.Category.objects.filter(blog__userinfo=request.user)
    return render(request,"add_article.html",{"categories":categories})


#富文本编辑器的图片上传
@login_required(login_url="/login_slide_validate/")
def upload(request):
    res = {"error":0}
    file_obj = request.FILES.get('imgFile')
    if file_obj:
        file_path = os.path.join(settings.MEDIA_ROOT,"article_imgs",file_obj.name)
        with open(file_path,"wb") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        url = "/media/aticle_imgs" + file_obj.name
        res["url"] = url
    return JsonResponse(res)


#修改文章
@login_required(login_url="/login_slide_validate/")
def edit_article(request):
    if request.method == "GET":
        article_id = request.GET.get("article")
        article = models.Article.objects.filter(id=article_id).first()
        # 把当前博客的文章分类查询出来
        categories = models.Category.objects.filter(blog__userinfo=request.user)
        return render(request, "add_article.html", {"article": article, "categories": categories,"is_update":1})
    else:
        return redirect("/blog/backend/")



#删除文章
@login_required(login_url="/login_slide_validate/")
def del_article(request):
    res = {"code":0}
    if request.method == "POST":
        article_id = request.POST.get("article_id")
        print("article_id = ",article_id)
        models.Article.objects.filter(id=article_id).delete()
        res = {"code": 1,"msg":"删除成功！"}
    else:
        res = {"code": 2,"error":"删除失败！"}
    return JsonResponse(res)









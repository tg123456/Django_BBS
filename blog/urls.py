from django.conf.urls import url
from blog import views


urlpatterns = [
    url(r'^backend/$',views.backend),
    url(r'^add_article/$',views.add_article),
    url(r'^del_article/$',views.del_article),
    url(r'^edit_article/',views.edit_article),
    url(r'^upload/$',views.upload),

    #点赞
    url(r'^thumbs_up/',views.thumbs_up),
    #评论
    url(r'^comment/',views.comment),

    #直接点击用户进入个人博客
    url(r'^(\d+)/$',views.home),

    #在个人博客里面进行分类选择
    url(r'^(\d+)/(archive|tag|category)/(.*)/',views.home),

    #进入个人文章
    url(r'^(\d+)/article/(\d+)/',views.article),

    #测试
    url(r'^article_edit/$',views.article_edit),

]






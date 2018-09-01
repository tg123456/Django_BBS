from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.png')

    blog = models.OneToOneField(to='Blog', null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用戶信息"
        verbose_name_plural = verbose_name


class Blog(models.Model):
    title = models.CharField(max_length=64,verbose_name="标题")
    theme = models.CharField(max_length=32,verbose_name="主題")

    def __str__(self):
        return self.title
    #
    # class Meta:
    #     verbose_name = "博客"
    #     verbose_name_plural = verbose_name


class Category(models.Model):
    title = models.CharField(max_length=32)
    blog = models.ForeignKey(to="Blog")

    def __str__(self):
        return "{}-{}".format(self.blog.title, self.title)

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    title = models.CharField(max_length=32)
    blog = models.ForeignKey(to="Blog")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to="UserInfo",verbose_name="作者")
    category = models.ForeignKey(to="Category", null=True, blank=True)  # 文章分类

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=("article", "tag"),
    )

    def __str__(self):
        # return "{}".format(self.title)
        return "{}__{}".format(self.user.username,self.title)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详情表
    """
    content = models.TextField()  # 文章内容
    article = models.OneToOneField(to="Article")

    def __str__(self):
        return "{}".format(self.article.title)

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name


class Article2Tag(models.Model):
    """
    文章和标签的多对多关系表
    """
    article = models.ForeignKey(to="Article")
    tag = models.ForeignKey(to="Tag")

    def __str__(self):
        return "{}-{}".format(self.article, self.tag)

    class Meta:
        unique_together = (("article", "tag"),)
        verbose_name = "文章-标签"
        verbose_name_plural = verbose_name


class ArticleUpDown(models.Model):
    """
    点赞表
    """
    user = models.ForeignKey(to="UserInfo", null=True)
    article = models.ForeignKey(to="Article", null=True)
    is_up = models.BooleanField(default=True)  # 点赞还是踩灭

    def __str__(self):
        return "{}-{}".format(self.user_id, self.article_id)

    class Meta:
        unique_together = (("article", "user"),)  # 同一个人只能给一篇文章点一次赞
        verbose_name = "点赞"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    article = models.ForeignKey(to="Article")
    user = models.ForeignKey(to="UserInfo")
    content = models.CharField(max_length=255)  # 评论内容
    create_time = models.DateTimeField(auto_now_add=True)

    parent_comment = models.ForeignKey("self", null=True,blank=True)  # 自己关联自己

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

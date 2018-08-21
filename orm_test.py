import os
import datetime

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "day75_BBS.settings")
    import django
    django.setup()

    from blog import models

    # user = models.UserInfo.objects.filter(username='TEST123456').first()
    # article = models.Article.objects.filter(user=user).first()
    # tags = article.tags
    # print(tags)

    # comment_id = models.Comment.objects.get(article_id='5', user_id='9',
    #                                         create_time='2018-08-20 20:01:03')
    # print(comment_id)







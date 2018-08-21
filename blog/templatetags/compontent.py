from django import template
from django.db.models import Count
from blog import models

register = template.Library()


@register.inclusion_tag("left_navigate_module.html")
def left_navigate_module(user_id):
    user = models.UserInfo.objects.filter(id=user_id).first()
    blog = user.blog
    categories = models.Category.objects.filter(blog=blog)
    tags = models.Tag.objects.filter(blog=blog)
    archives = models.Article.objects.filter(user_id=user_id).extra(
        select={'year': 'year(create_time)', 'month': 'month(create_time)'}).values('year', 'month'). \
        annotate(available=Count('create_time')).order_by('-year', '-month')

    return {
        "user":user,
        "categories": categories,
        "tags": tags,
        "archives": archives,
    }



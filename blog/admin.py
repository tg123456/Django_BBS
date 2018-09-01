from django.contrib import admin

from blog import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.Article2Tag)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Comment)

from django.db.models import F

class ArticleAdmin(admin.ModelAdmin):

    list_filter = ['id','user','title','category','tags']
    list_display_links = ['title','category',]
    list_editable = ['user']
    list_per_page = 3
    list_max_show_all = 2
    list_display = ['title','desc','create_time','user','category','up_count']
    search_fields = ['title','up_count','user__username','create_time']

    # actions_on_top = False
    # actions_selection_counter = True
    # show_full_result_count = True
    # list_select_related = True
    # add_form_template = 'add_article.html'

    raw_id_fields = ('category', 'tags',)

    fieldsets = (
        ('基本信息',{
            'fields':('title','desc','user')
        }),
        ('其他',{
            'classes':('comment_count'),
            'fields':('comment_count','down_count','up_count','category')
        })
    )

    # 批量操作
    def patch_init(self,request,queryset):
        queryset.update(up_count=F('up_count')+1)

    patch_init.short_description = "价格初始化"

    actions = [patch_init]

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','theme']

admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Blog)

# print(models.Article)
# print(admin.site._registry)

class ArticleLine(admin.StackedInline):
    extra = 3
    model = models.Article

class ArticleLine(admin.TabularInline):
    extra = 1  # 多一条空白
    model = models.Article

class UserAdmin(admin.ModelAdmin):
    #详情界面
    # 只显示那些字段
    fields = ('username','password')
    readonly_fields = ('password',)
    # 不显示那些字段
    exclude = ('last_name','first_name',)
    # list_display = ('id','username')
    inlines = [ArticleLine]

    # radio_fields = {"id": admin.VERTICAL}

admin.site.register(models.UserInfo,UserAdmin)


class TagAdmin(admin.ModelAdmin):

    list_filter = ['title','blog']
    list_display = ['title','blog']

admin.site.register(models.Tag,TagAdmin)


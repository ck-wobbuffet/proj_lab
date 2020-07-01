#coding=gbk
from django.contrib import admin
from .models import Articles,ArticleType

# Register your models here.
@admin.register(ArticleType)
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'article_type',
                    'author',
                    'get_read_num',
                    'created_time',
                    'last_updated_time')
'''
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','article')
'''
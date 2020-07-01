from django.contrib import admin
from .models import ReadNum,ReadDetails
# Register your models here.

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('content_object','object_id','read_num')


@admin.register(ReadDetails)
class ReadDetailsAdmin(admin.ModelAdmin):
    list_display = ('date','content_type', 'read_num',)

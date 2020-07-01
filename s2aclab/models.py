from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadNumExpandMethod, ReadDetails



# Create your models here.

class ArticleType(models.Model):
    type_name = models.CharField(max_length=20)
    def __str__(self):
        #显式显示
        return self.type_name

class Articles(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=100)
    article_type = models.ForeignKey(ArticleType,on_delete=models.DO_NOTHING,related_name='art_art')
    content = RichTextUploadingField(config_name='upload_ckeditor')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # created_time = models.DateTimeField(auto_now_add=True)
    created_time = models.DateTimeField(auto_now_add=False)
    last_updated_time = models.DateTimeField(auto_now=True)

    read_details = GenericRelation(ReadDetails)  # content_object = GenericForeignKey('content_type', 'object_id')
    # read_num = models.IntegerField(default=0)
    # get_read_num = ReadNumExpandMethod()

    def __str__(self):
        #显式显示
        return "<Article:%s>" % self.title
    
    class Meta: # 排序
        ordering = ['-created_time']

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    article = models.OneToOneField(Articles, on_delete=models.DO_NOTHING)   #   read和article一对一
'''

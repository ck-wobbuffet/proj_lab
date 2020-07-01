#coding=gbk
from django.urls import path
from . import views
#start with article
urlpatterns = [
    #http://localhost:8000/article/1
        path('<int:art_pk>', views.article_details,name='article_details'),
        #localhost:8000/a
        path('', views.articles_list, name='articles_list'),
        path('type/<int:art_type_pk>', views.article_with_type, name='article_with_type'),
        path('date/<int:year>/<int:month>',views.article_with_date, name='article_with_date'),
]

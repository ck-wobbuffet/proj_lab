from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import ArticleType,Articles
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from read_statistics.models import ReadNum
from read_statistics.utils import get_read_statistics
from comment.models import Comment
from comment.forms import CommentFrom


def get_all_common_data(request,articles_all_list):
    paginator = Paginator(
        articles_all_list, settings.ARTICLE_NUMBER_EACH_PAGE)  # 8篇一页
    # 获取页码参数（GET请求）  .GET 字典 使用get方法判断是否有page值，没有返回1
    page_num = request.GET.get("page", 1)
    # 输入许可字符范围外的字符会返回1
    page_of_articles = paginator.get_page(page_num)

    # 获取当前页
    current_page = page_of_articles.number
    # 页码显示范围
    page_range = [i for i in range(
        current_page-2, current_page+3) if 0 < i <= paginator.num_pages]
    # 第一页
    if page_range[0] >= 2:
        page_range.insert(0, 1)  # 第一位插入1页码
        if page_range[1] != 2:
            page_range.insert(1, '...')   # 加上...
    # 最后一页
    if page_range[-1] <= paginator.num_pages - 1:
        if page_range[-1] != paginator.num_pages - 1:
            page_range.append('...')      # 加上...
        page_range.append(paginator.num_pages)


                                                            
    context = {}
    # context['articles'] = page_of_articles.object_list  #   前端页面
    context['page_of_articles'] = page_of_articles  # 当前页码
    # context['article_types'] = artcile_types_list  # 所有分类
    context['article_types'] = ArticleType.objects.annotate(article_count=Count('art_art'))  # 所有分类
    # context['article_dates'] = Articles.objects.dates('created_time', 'month', order='DESC')
    context['article_dates'] = get_categories_count()   #   日期分类与数量
    context['page_range'] = page_range
    return context


#   获取对应的分类与博文数 
def get_categories_count():
    '''
    # 获取对应分类的博文数量 简单粗暴方法 占服务器
    article_types = ArticleType.objects.all()
    artcile_types_list = []
    for article_type in article_types:
            #   类对象`article_type（ArticleType)`添加属性`.article_count`
        article_type.article_count = Articles.objects.filter(
            article_type=article_type).count()
        artcile_types_list.append(article_type)

    # 获取对应分类的博文数量 annotate
    # ArticleType.objects.annotate(article_count=Count('art_art'))    # 返回sql语句
    '''

    # 获取对应日期的博文数量
    article_dates = Articles.objects.dates('created_time', 'month', order = 'DESC')
    article_dates_dict = dict()
    for date in article_dates:
        article_dates_dict[date] = Articles.objects.filter(created_time__year=date.year,
                                                            created_time__month=date.month).count()

    return article_dates_dict



'''
    页面    # Create your views here.
'''
# Create your views here.
def article_details(request, art_pk):
    
    article = get_object_or_404(Articles, pk=art_pk)
    read_cookie_key = get_read_statistics(request=request, obj=article)
    article_content_type = ContentType.objects.get_for_model(article)
    print(f'model={type(article_content_type.model)}')  # model=<class 'str'>
#       article_content_type = <class 'django.contrib.contenttypes.models.ContentType' >#
    print(f'article_content_type={type(article_content_type)}')
    comments = Comment.objects.filter(content_type=article_content_type, object_id=art_pk,parent=None)
    
    context = {}
    context['article'] = article
    context['next_article'] = Articles.objects.filter(created_time__gt=article.created_time).last()  # .last()表示取最后一条
    context['previous_article'] = Articles.objects.filter(created_time__lt=article.created_time).first()  # .first()表示取第一条
    # context['user'] = request.user
    context['comments'] = comments.order_by('-comment_time')  # 所有评论
    '''reply没写完---------------2020--6-13-------------'''
    context['comment_form'] = CommentFrom(initial={'content_type': article_content_type, 'object_id': art_pk,'reply_comment_id':0})

    response = render(request, 'article_details.html', context)  #   响应
    # cookie提交给服务器，max_age ： cookie有效时长，过期刷新cookie，单位为s
    response.set_cookie(read_cookie_key, value='true', max_age=600)
    return response



def articles_list(request):
    articles_all_list = Articles.objects.all()

    context = get_all_common_data(request, articles_all_list)
    
    return render(request, 'articles_list.html', context)


def article_with_type(request, art_type_pk):
    article_type = get_object_or_404(ArticleType, pk=art_type_pk)   
    articles_all_list = Articles.objects.filter(article_type=article_type)

    context = get_all_common_data(request,articles_all_list)
    print(f'art_type_pk={article_type}')
    print(f'type_art_type_pk={type(article_type)}')
    print(f'dir_art_type_pk={dir(article_type)}')

    context['article_type'] = article_type
    return render(request, 'article_with_type.html', context)


def article_with_date(request, year, month):

    articles_all_list = Articles.objects.filter(created_time__year=year, created_time__month=month)

    context = get_all_common_data(request,articles_all_list)

    context['article_with_date'] = '%s-%s'%(year,month)
    return render(request, 'article_with_date.html', context)

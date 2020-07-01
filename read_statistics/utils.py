from datetime import datetime,timedelta
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum, ReadDetails
from s2aclab.models import Articles


# 获取总阅读数据 和一天的阅读数据
def get_read_statistics(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # # 当浏览器中cookie不存在时 阅读加1.
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     # 存在记录
        #     readnum = ReadNum.objects.get(
        #         content_type=ct, object_id=obj.pk)
        # else:
        #     # 没有记录
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # 总阅读数+1
        readnum,created_flag = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)    # get_or_create()返回元组
        readnum.read_num += 1  # 阅读数+1
        readnum.save()

        #当天阅读数+1
        date = timezone.now().date()
        readdetails, created_flag = ReadDetails.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readdetails.read_num += 1
        readdetails.save()

    return key


# 获取一周内的流量数据
def get_one_week_read_statistics(content_type):
    today = timezone.now().date()
    dates = []
    read_sum = []
    for i in range(6, -1,-1):
        date = today + timedelta(days= -i)
        dates.append(date.strftime('%m/%d'))
        readdetails = ReadDetails.objects.filter(content_type=content_type, date=date)
        res = readdetails.aggregate(read_num_sum=Sum('read_num'))    # 返回字典{'read_num_sum':?}
        read_sum.append(res['read_num_sum'] or 0)
    return read_sum,dates


# 获取一天内的热门
def get_today_hot_read(content_type):
    today = timezone.now().date()
    readdetails = ReadDetails.objects.filter(content_type=content_type, date=today).order_by('-read_num')

    return readdetails[:5]


# 获取昨天热门
def get_yesterday_hot_read(content_type):
    yes = timezone.now().date() + timedelta(days=-1)
    readdetails = ReadDetails.objects.filter(
        content_type=content_type, date=yes).order_by('-read_num')

    return readdetails[:5]


# 获取一周内的热门
def get_one_week_hot_articles():
    today = timezone.now().date()
    date = today + timedelta(days=-6)
    articles = Articles.objects.filter(
        read_details__date__lte=today,read_details__date__gte=date
        ).values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    
    return articles[:7]
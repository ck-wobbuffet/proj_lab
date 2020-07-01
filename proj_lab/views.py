from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.db.models import Count

from read_statistics.utils import get_one_week_read_statistics, get_today_hot_read, get_yesterday_hot_read, get_one_week_hot_articles
from s2aclab.models import Articles,ArticleType
from .forms import LoginForm, RegisterForm



def home(request):
    content_type = ContentType.objects.get_for_model(Articles)
    read_sum, dates = get_one_week_read_statistics(content_type)

    # week hot ¨
    week_hot = cache.get('week_hot')
    if not week_hot:
        week_hot = get_one_week_hot_articles()
        cache.set('week_hot', week_hot, 3600)  #   3600s
        print('calculate')
    else:
        print('use cache')

    context = {}
    context['artilce_types'] = ArticleType.objects.annotate(article_count=Count('art_art'))
    context['read_sum'] = read_sum
    context['dates'] = dates
    context['today_hot'] = get_today_hot_read(content_type)
    context['yesterday_hot'] = get_yesterday_hot_read(content_type)
    context['week_hot'] = week_hot
    return render(request, 'home.html', context)
    

def login(request):
    '''    
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': 'Wrong password or account! '})
     '''
    if request.method == 'POST':
       login_form = LoginForm(request.POST)

       if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            # register
            user = User.objects.create_user(username, password, email)
            user.save()
            # sign in
            # user = auth.authenticate(request, username=username, password=password) user already exists
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegisterForm()
    
    context = {}
    context['register_form'] = register_form
    #   {'register_form': <RegisterForm bound=False, valid=Unknown, fields=(username;password;password_again;email)>}
    return render(request,'register.html',context)


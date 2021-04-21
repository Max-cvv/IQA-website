from django.shortcuts import render,redirect
from django.urls import reverse
from website.models import Users, Records
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from django.contrib.auth import logout
from utils.utils import login_decorator
# Create your views here.

def test1(request):
    return render(request,'wesite/test.html')


#用户端
def log_in(request):

    if request.method=='GET':
        return render(request,'wesite/login.html')
    elif request.method=="POST":
        user=request.POST.get('u')
        user_find = Users.objects.filter(check_list = user)
        if user_find:
            #request.session.set_expiry(10)  #session认证时间为10s，10s之后session认证失效
            #request.session['username']=user   #user的值发送给session里的username
            user_find = Users.objects.get(check_list = user)
            if user_find.submit_time:
                context = {'script':"alert", 'wrong':'您已参与！'}
                return render(request,'wesite/login.html', context)
            else:
                user_find.login_time = datetime.datetime.now()
                user_find.save()
                request.session['is_login']=True   #认证为真
                request.session['userID']=user_find.id
                return redirect(reverse('index'))
        else:
            context = {'script':"alert", 'wrong':'未找到！'}
            return render(request,'wesite/login.html', context)
    return render(request,'wesite/login.html')

@login_decorator('is_login', 'user_login')
def index(request):
    return render(request, 'wesite/index.html')


@csrf_exempt
def record(request):
    if request.method=='POST':
        record = Records(user_id=request.session['userID'],img1=request.POST.get('img1'),img2=request.POST.get('img2'),\
            result = request.POST.get('result'),operation = request.POST.get('operation'), \
            operation_scroll = request.POST.get('operation_scroll'), op_time = request.POST.get('op_time'))
        record.save()
        return JsonResponse({'state':'ok'})
    else:
        return JsonResponse({'state':'fail'})


@csrf_exempt
def submit(request):
    if request.method=='POST':
        user = Users.objects.get(id=request.session['userID'])
        user.submit_time=datetime.datetime.now()
        user.screen_width = request.POST.get('screen_width')
        user.screen_height = request.POST.get('screen_height')
        user.window_width = request.POST.get('window_width')
        user.window_height = request.POST.get('window_height')
        user.screen_colorDepth = request.POST.get('screen_colorDepth')
        user.save()
        #request.session.clear()
        logout(request)
        return JsonResponse({'state':'ok'})
    return JsonResponse({'state':'fail'})

@csrf_exempt
def get_next(request):
    if request.method=='POST':
        return JsonResponse({'state':'ok', 'device1':1, 'device2':1, 'photo_num':random.randint(1,58)})
    return JsonResponse({'state':'fail'})


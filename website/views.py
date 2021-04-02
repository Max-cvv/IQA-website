from django.shortcuts import render,redirect
from django.urls import reverse
from website.models import Users, Records, Managers
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import random

# Create your views here.
def log_in(request):

    if request.method=='GET':
        return render(request,'login.html')
    elif request.method=="POST":
        user=request.POST.get('u')
        user_find = Users.objects.filter(check_list = user)
        if user_find:
            #request.session.set_expiry(10)  #session认证时间为10s，10s之后session认证失效
            #request.session['username']=user   #user的值发送给session里的username
            user_find = Users.objects.get(check_list = user)
            if user_find.submit_time:
                context = {'script':"alert", 'wrong':'您已参与！'}
                return render(request,'login.html', context)
            else:
                user_find.login_time = datetime.datetime.now()
                user_find.save()
                request.session['is_login']=True   #认证为真
                request.session['userID']=user_find.id
                return redirect(reverse('index'))
        else:
            context = {'script':"alert", 'wrong':'未找到！'}
            return render(request,'login.html', context)
    return render(request,'login.html')

def manager_login(request):

    if request.method=='GET':
        return render(request,'manager_login.html')
    elif request.method=="POST":
        user=request.POST.get('u')
        password = request.POST.get('p')
        user_find = Managers.objects.filter(user_id = user, user_password = password)
        if user_find:
            #request.session.set_expiry(10)  #session认证时间为10s，10s之后session认证失效
            #request.session['username']=user   #user的值发送给session里的username
            request.session['is_login_manager']=True   #认证为真
            return redirect(reverse('manager_index'))
        else:
            context = {'script':"alert", 'wrong':'用户名或密码错误！！'}
            return render(request,'manager_login.html', context)
    return render(request,'manager_login.html')

def manager_index(request):
    if request.session.get('is_login_manager',None):
#        request.session.clear()
        return render(request, 'manage/manage_base.html')
    else:
        return redirect(reverse('manager_login'))


def index(request):
    if request.session.get('is_login',None):
#        request.session.clear()
        return render(request, 'index.html')
    else:
        return redirect(reverse('login'))

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
        request.session.clear()
        return JsonResponse({'state':'ok'})
    return JsonResponse({'state':'fail'})

@csrf_exempt
def get_next(request):
    if request.method=='POST':
        return JsonResponse({'state':'ok', 'device1':1, 'device2':1, 'photo_num':random.randint(1,58)})
    return JsonResponse({'state':'fail'})

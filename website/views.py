from django.shortcuts import render,redirect
from django.urls import reverse
from website.models import Users, Records, Managers
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import random

# Create your views here.

#装饰器函数
def login_decorator(session_item = 'is_login_manager', redirect_url = 'manager_login'):
    def decorator(func):
        def wrapper(request, *args, **kargs):
            if request.session.get(session_item,None):
                return func(request, *args, **kargs)
            else:
                return redirect(reverse(redirect_url))
        return wrapper
    return decorator


#用户端
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

@login_decorator('is_login', 'login')
def index(request):
    return render(request, 'index.html')


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


#管理端
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
            return redirect(reverse('manager_users_list'))
        else:
            context = {'script':"alert", 'wrong':'用户名或密码错误！！'}
            return render(request,'manager_login.html', context)
    return render(request,'manager_login.html')

@login_decorator()
def manager_users_list(request):
    user_find = Users.objects.all()
    return render(request, 'manage/manage_users_list.html', {'users_list':user_find})


@login_decorator()
def manager_records_list(request):
    record_find = Records.objects.all().order_by("user_id")
    record_img = []
    for record in record_find:
        record.op_time = float(record.op_time)/1000
        D1 = int(record.img1/10000)
        D2 = int(record.img2/10000)
        CO1 = int((record.img1-D1*10000)/1000)
        CO2 = int((record.img2-D2*10000)/1000)
        img1 = record.img1 % 1000
        img2 = record.img2 % 1000
        dic = {'D1':D1, 'D2':D2, 'CO1':CO1, 'CO2':CO2, 'img1':img1, 'img2':img2}
        record_img.append(dic)
    return render(request, 'manage/manage_records_list.html', {'records_list':zip(record_find,record_img)})

@login_decorator()
def user_reset(request, user_id):
    user_find = Users.objects.get(id = user_id)
    user_find.screen_width = None
    user_find.screen_height = None
    user_find.window_width = None
    user_find.window_height = None
    user_find.login_time = None
    user_find.submit_time = None
    user_find.save()
    return redirect(reverse('manager_users_list'))

@login_decorator()
def user_delete(request, user_id):
    user_find = Users.objects.get(id = user_id)
    user_find.delete()
    return redirect(reverse('manager_users_list'))

@login_decorator()
def user_add(request):
    users = Users.objects.all().order_by("id")
    i = 1
    for user_num in users:
        if i != user_num.id:
            break
        i += 1
    user = Users(id = i, name = request.GET.get('name'), check_list = request.GET.get('check'))
    user.save()
    return redirect(reverse('manager_users_list'))

@login_decorator()
def record_delete(request, record_id):
    record_find = Records.objects.get(id = record_id)
    record_find.delete()
    return redirect(reverse('manager_records_list'))

@login_decorator()
def manage_logout(request):
    request.session.flush()
    return redirect(reverse('manager_login'), permanent=True)


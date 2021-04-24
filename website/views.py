from django.shortcuts import render,redirect
from django.urls import reverse
from website.models import Users, Records, Question
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
from django.contrib.auth import logout
from utils.utils import login_decorator
# Create your views here.

def homepage(request):
    if request.session.get('is_login',None):
        return redirect(reverse('index'))
    else:
        return render(request,'wesite/homepage.html')


#homepage
@csrf_exempt
def hand_form(request):
    if request.method=='POST':
        age=request.POST.get('age') 
        gender=request.POST.get('gender')
        edu=request.POST.get('edu')
        isGlasses=request.POST.get('isGlasses')
        pho=request.POST.get('pho')
        screen=request.POST.get('screen')

        qa = Question(age = age, gender = gender, edu = edu, isGlasses = isGlasses, pho = pho)
        qa.save()
        user = Users(login_time = datetime.datetime.now())
        user.save()

        request.session['is_login']=True   #认证为真
        request.session['userID']=user.id

        return JsonResponse({'state':'ok', })
    else:
        return JsonResponse({'state':'fail'})



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


@login_decorator('is_login', 'homepage')
def index(request):
    return render(request, 'wesite/index_test.html')


@csrf_exempt
def creatRecordList(request):
    if request.method=='POST':
        user_id = request.session['userID']
        user_find = Users.objects.get(id = user_id)
        user_find.screen_width = request.POST.get('screen_width')
        user_find.screen_height = request.POST.get('screen_height')
        user_find.window_width = request.POST.get('window_width')
        user_find.window_height = request.POST.get('window_height')
        user_find.screen_colorDepth = request.POST.get('screen_colorDepth')
        user_find.save()

        if user_find.record_all:
            pass
        else:
            #获得需要评价的总数和具体条目
            record_list = []
            record_all = 20

            user_find.record_all = record_all
            user_find.record_now = 1
            user_find.save()

            for i in range(1,record_all+1):
                img = random.randint(1,58)
                record = Records(user_id=user_id,user_record_id = i, img1=11000+img,img2=21000+img)
                record.save()

        record_now = user_find.record_now
        record_all = user_find.record_all
        if record_now == 1:
            progress = 0
        else:
            progress = record_now/record_all

        #获得当前要显示的两张图片
        record = Records.objects.get(user_id=user_id, user_record_id = record_now)
        D1 = int(record.img1/10000)
        D2 = int(record.img2/10000)
        CO1 = int((record.img1-D1*10000)/1000)
        CO2 = int((record.img2-D2*10000)/1000)
        img1 = record.img1 % 1000
        img2 = record.img2 % 1000
        return JsonResponse({'state':'ok', 'device1':D1, 'device2':D2,'co1':CO1, 'co2':CO2, \
                'photo_num1':img1, 'photo_num1':img2, 'progress':progress})
    return JsonResponse({'state':'fail'})


@csrf_exempt
def record(request):
    if request.method=='POST':
        user_id = request.session['userID']
        user_find = Users.objects.get(id = user_id)
        record_now = user_find.record_now
        record_next = record_now + 1
        record_all = user_find.record_all
        user_find.record_now = record_now + 1
        user_find.save()

        record = Records.objects.get(user_id=user_id, user_record_id = record_now)
        record.result = request.POST.get('result')
        record.operation = request.POST.get('operation')
        record.operation_scroll = request.POST.get('operation_scroll')
        record.submit_time = datetime.datetime.now()
        record.save()

        if record_next <= record_all:
            record = Records.objects.get(user_id=user_id, user_record_id = record_next)
            progress = record_next/record_all
            D1 = int(record.img1/10000)
            D2 = int(record.img2/10000)
            CO1 = int((record.img1-D1*10000)/1000)
            CO2 = int((record.img2-D2*10000)/1000)
            img1 = record.img1 % 1000
            img2 = record.img2 % 1000
            return JsonResponse({'state':'ok', 'device1':D1, 'device2':D2,'co1':CO1, 'co2':CO2, \
                    'photo_num1':img1, 'photo_num1':img2, 'progress':progress})
        else:
            user_find.submit_time=datetime.datetime.now()
            user_find.save()
            logout(request)
            return JsonResponse({'state':'handSuccess'})
    else:
        return JsonResponse({'state':'fail'})




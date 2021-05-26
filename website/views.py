from django.shortcuts import render,redirect
from django.urls import reverse
from website.models import Users, Records, Question ,Tiaomu, Devices, Lab
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
import os
from django.contrib.auth import logout
from utils.utils import login_decorator
from utils.utils import compute_rank_scores,extract_pair_data
# Create your views here.
from django.conf import settings
STATIC_ROOT = os.path.join(settings.STATIC_ROOT, 'upload')

color = ["background-color:#8c4646;","background-color:#588c7e;","background-color:#acbc8a;","background-color:#ecd189;","background-color:#e99469;","background-color:#db6b5c;","background-color:#babca2;","background-color:#f9d49c;"]

def generateCode(codeLength):
    codeList = '0123456789QAZWSXEDCRFVTGBYHNUJMIKOLP'
    code = ''
    for i in range(codeLength):
        code += random.choice(codeList)

    return code

def homepage(request):
    if Lab.objects.filter(status=1):
        is_start = 1
    else:
        is_start = 0
    return render(request,'wesite/homepage.html', {'after':0, 'is_start':is_start})

def homepage_after(request):
    if Lab.objects.filter(status=1):
        is_start = 1
    else:
        is_start = 0
    record_find = Records.objects.all()
    data1 = []
    for record in record_find:
        D1 = record.device1
        D2 = record.device2
        CO1 = record.co1
        CO2 = record.co2
        img1 = record.img_num1
        img2 = record.img_num2
        result = record.result
        if img1 == img2 and D1 != 8 and D2 != 8 and D1 != 9 and D2 != 9:#and dataGet[1] == 1:
            if result == 0:
                data1.append((D1, D2))
            if result == 1:
                data1.append((D2, D1))
    data_pair = extract_pair_data(data1)
    ranks = compute_rank_scores(data_pair)
    name = {}
    devices = Devices.objects.all()
    for device in devices:
        name[device.id] = device.name
    ranklist = []
    i = 0
    for rank in ranks:
        ranklist.append(['手机{}'.format(i+1), 'style = width:'+str(round(rank[1],2))+'%;'+color[i%8], str(round(rank[1],2))])
        i+=1
    return render(request, 'wesite/homepage.html', {'after':1,'ranks':ranklist, 'is_start':is_start})


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
        
        code = generateCode(6)
        #code = 'NLIEGG'
        findUser = Users.objects.filter(check_list=code)
        while findUser:
            code = generateCode(6)
            findUser = Users.objects.filter(check_list=code)
        
        users = Users.objects.all().order_by("id")
        i = 1
        for user_num in users:
            if i != user_num.id:
                break
            i += 1
        user = Users(id = i, check_list = code, record_now = 1)
        user.save()
        qa = Question(user_id = user.id, age = age, gender = gender, edu = edu, isGlasses = isGlasses, pho = pho, screen = screen[0:30])
        qa.save()
        #获得需要评价的总数和具体条目
        #img_index = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26,  29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 51, 53, 54, 55, 56]
        #tiaomu1 = [(4, 14), (8, 9), (5, 12), (3, 13), (6, 10), (7, 11), (2, 12), (4, 13), (15, 16), (6, 11), (9, 10), (7, 13), (3, 15), (8, 14), (4, 10), (2, 7), (5, 15), (12, 16), (8, 13), (3, 9), (4, 16), (12, 15), (2, 9), (10, 14), (7, 16), (5, 9), (8, 15), (7, 14), (4, 9), (2, 16), (7, 12), (8, 11), (10, 13), (9, 16), (14, 15), (5, 6), (2, 11), (9, 15), (3, 12), (5, 10), (6, 9), (2, 3), (12, 13), (4, 6), (3, 7), (2, 5), (6, 15), (9, 11), (2, 10), (4, 5), (7, 15), (8, 10), (11, 14), (5, 7), (6, 12), (13, 14), (3, 8), (5, 11), (2, 13), (8, 12), (4, 11), (3, 10), (13, 15), (4, 8), (6, 14), (3, 16), (4, 15), (6, 13), (9, 12), (7, 10), (11, 13), (6, 8), (5, 16), (11, 12), (2, 15), (6, 7), (5, 13), (10, 11), (2, 4), (5, 14), (3, 6), (2, 8), (11, 16), (4, 7), (3, 14), (11, 15), (4, 12), (3, 5), (7, 8), (10, 12), (3, 11), (8, 16), (2, 14), (3, 4), (7, 9), (2, 6), (13, 16), (5, 8), (9, 14), (6, 16), (10, 15), (12, 14), (9, 13), (14, 16), (10, 16)]
        #tiaomu_list = [Tiaomu(img1 = i[0], img2 = i[1]) for i in tiaomu1]
        #Tiaomu.objects.bulk_create(tiaomu_list)
        
        #group = [(0,15), (15,30), (30, 45),(45,60), (60, 75), (75, 90), (90, 105)]
        #nightImg = [107,108,109,110,111,112,113,116,117,119,122,124,125,126,127,128,129,130,131,132,133,134,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,153,154,155,156,158,160,161]
        #random.shuffle(nightImg)

        lab_co2 = [i for i in range(11,61)]
        lab_co4 = [i for i in range(5,55)]
        #group_id = user.id % len(group)
        group_id = user.id % 2
        if group_id==0:
            lab_now = lab_co2
            co_now = 2
        else:
            lab_now = lab_co4
            co_now = 4
        
        #tiaomuGet = Tiaomu.objects.all()[group[group_id][0]:group[group_id][1]]

        record_all = 60
        user.record_all = record_all
        user.save()

        record_list = []
        for i in range(1,51):
            D1 = random.randint(1,7)
            D2 = random.randint(1,7)
            while D1 ==D2:
                D2 = random.randint(1,7)
            record_list.append([D1,D2,co_now,lab_now[i-1],lab_now[i-1]])
        for i in range(1,7):
            D1 = random.randint(1,7)
            D2 = random.randint(1,7)
            while D1 ==D2:
                D2 = random.randint(1,7)
            record_list.append([10, 10, i, D1, D2])
        random.shuffle(record_list)
        for i in range(1,5):
            j = 5-i
            record_now_repeat = record_list[(j-1)*14]
            if record_now_repeat[0]==record_now_repeat[1]:
                record_list.insert(j*14, [10, 10, record_now_repeat[2], record_now_repeat[4], record_now_repeat[3]])
            else:
                record_list.insert(j*14, [record_now_repeat[1], record_now_repeat[0], record_now_repeat[2], record_now_repeat[3], record_now_repeat[4]])
        i = 1
        for record_item in record_list:
            record = Records(user_id=user.id,user_record_id = i, device1=record_item[0], device2=record_item[1], co1 = record_item[2], co2 = record_item[2], img_num1=record_item[3],img_num2=record_item[4])
            record.save()
            i+=1

        #i = 46
        # for couple in tiaomuGet:
        #     record = Records(user_id=user.id,user_record_id = i, device1=6, device2=6, co1 = 1, co2 = 1,img_num1=couple.img1,img_num2=couple.img2)
        #     record.save()
        #     if i == record_all:break
        #     i = i+1

        
        
        
        response = JsonResponse({'state':'ok', 'code':code})
        response.set_cookie("user_check_code", code, 60*60*24*7)

        return response
    else:
        return JsonResponse({'state':'fail'})



#用户端
def log_in(request):
  
    if request.method=='GET':
        return render(request,'wesite/login.html')
    elif request.method=="POST":
        if not Lab.objects.filter(status=1):
            context = {'script':"alert", 'wrong':'未在实验开展时间！'}
            return render(request,'wesite/login.html', context)
        user=request.POST.get('u')
        user_find = Users.objects.filter(check_list = user)
        if user_find:
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


        record_now = user_find.record_now
        record_all = user_find.record_all
        if record_now == 1:
            progress = 0
        else:
            progress = record_now/record_all

        #获得当前要显示的两张图片
        record = Records.objects.get(user_id=user_id, user_record_id = record_now)
        D1 = record.device1
        D2 = record.device2
        CO1 = record.co1
        CO2 = record.co2
        img1 = record.img_num1
        img2 = record.img_num2
        return JsonResponse({'state':'ok', 'device1':D1, 'device2':D2,'co1':CO1, 'co2':CO2, \
                'photo_num1':img1, 'photo_num2':img2, 'progress':progress})
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
            D1 = record.device1
            D2 = record.device2
            CO1 = record.co1
            CO2 = record.co2
            img1 = record.img_num1
            img2 = record.img_num2
            return JsonResponse({'state':'ok', 'device1':D1, 'device2':D2,'co1':CO1, 'co2':CO2, \
                    'photo_num1':img1, 'photo_num2':img2, 'progress':progress, 'now':record_next})
        else:
            user_find.submit_time=datetime.datetime.now()
            user_find.save()
            logout(request)
            return JsonResponse({'state':'handSuccess'})
    else:
        return JsonResponse({'state':'fail'})




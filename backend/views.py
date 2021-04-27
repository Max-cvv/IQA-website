from django.shortcuts import render,redirect
from django.urls import reverse
from website.models import Users, Records, Managers, Question
from django.contrib.auth import logout
from utils.utils import login_decorator
from utils.utils import compute_rank_scores,extract_pair_data

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
name = ["小米6","华为畅享7plus","魅族16","华为nova2plus","红米k20pro","iphone11","iphone7","oppoR9s","oppoR9s"]
color = ["background-color:#8c4646;","background-color:#588c7e;","background-color:#acbc8a;","background-color:#ecd189;","background-color:#e99469;","background-color:#db6b5c;","background-color:#babca2;","background-color:#f9d49c;"]
#获得实时排名
@login_decorator()
def get_rank(request):
    record_find = Records.objects.all()
    data1 = []
    for record in record_find:
        D1 = int(record.img1/10000)
        D2 = int(record.img2/10000)
        CO1 = int((record.img1-D1*10000)/1000)
        CO2 = int((record.img2-D2*10000)/1000)
        img1 = record.img1 % 1000
        img2 = record.img2 % 1000
        result = record.result
        if img1 == img2 and D1 != 8 and D2 != 8:#and dataGet[1] == 1:
            

            if result == 0:
                data1.append((D1, D2))
            if result == 1:
                data1.append((D2, D1))
    data_pair = extract_pair_data(data1)
    ranks = compute_rank_scores(data_pair)
    ranklist = []
    i = 0
    for rank in ranks:
        ranklist.append([name[rank[0]-1], 'style = width:'+str(round(rank[1],2))+'%;'+color[i], str(round(rank[1],2))])
        i+=1
    return render(request, 'backend/manage_rank.html', {'ranks':ranklist})




#管理端
def manager_login(request):
    if request.method=='GET':
        return render(request,'backend/manager_login.html')
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
            return render(request,'backend/manager_login.html', context)
    return render(request,'backend/manager_login.html')

@login_decorator()
def manager_users_list(request):
    user_find = Users.objects.all()
    return render(request, 'backend/manage_users_list.html', {'users_list':user_find})

@login_decorator()
def manager_question_list(request):
    gender = ['男','女']
    age = ['1-20岁', '20-30岁', '30-50岁', '50岁以上']
    isGlasses = ['是','否']
    edu = ['高中及以下', '本科或专科', '研究生', '博士及以上']
    pho = ['经常', '一般', '很少', '几乎没有']

    qas = Question.objects.all()
    for qs in qas:
        qs.gender = gender[int(qs.gender) -1]
        qs.age = age[int(qs.age) -1]
        qs.isGlasses = isGlasses[int(qs.isGlasses) -1]
        qs.edu = edu[int(qs.edu) -1]
        qs.pho = pho[int(qs.pho) -1]
    return render(request, 'backend/manage_question_list.html', {'qas':qas})


@login_decorator()
def manager_records_list(request):
    record_find = Records.objects.all().order_by("user_id")
    record_img = []
    for record in record_find:
        if record.op_time:
            record.op_time = float(record.op_time)/1000
        else:
            record.op_time = 0
        D1 = int(record.img1/10000)
        D2 = int(record.img2/10000)
        CO1 = int((record.img1-D1*10000)/1000)
        CO2 = int((record.img2-D2*10000)/1000)
        img1 = record.img1 % 1000
        img2 = record.img2 % 1000
        

        dic = {'D1':D1, 'D2':D2, 'CO1':CO1, 'CO2':CO2, 'img1':img1, 'img2':img2}
        record_img.append(dic)
    return render(request, 'backend/manage_records_list.html', {'records_list':zip(record_find,record_img)})

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


def manage_logout(request):
    #request.session.clear()
    logout(request)
    return redirect(reverse('manager_login'))

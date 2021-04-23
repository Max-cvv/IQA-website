from django.shortcuts import render,redirect
from django.urls import reverse
from website.models import Users, Records, Managers
from django.contrib.auth import logout
from utils.utils import login_decorator
# Create your views here.

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

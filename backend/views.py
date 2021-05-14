from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from website.models import Users, Records, Managers, Question, Devices, Process
from django.contrib.auth import logout
from utils.utils import login_decorator, compute_rank_scores, extract_pair_data
from io import BytesIO
import xlwt
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


from django.conf import settings
STATIC_ROOT = os.path.join(settings.STATIC_ROOT, 'files/photo')
num_progress = 0
# Create your views here.
name = ["小米6","华为畅享7plus","魅族16","华为nova2plus","红米k20pro","iphone11","iphone7","oppoR9s","oppoR9s"]
color = ["background-color:#8c4646;","background-color:#588c7e;","background-color:#acbc8a;","background-color:#ecd189;","background-color:#e99469;","background-color:#db6b5c;","background-color:#babca2;","background-color:#f9d49c;"]
#获得实时排名
@login_decorator()
def get_rank(request):
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


def excel(request):
    
    """导出excel表"""
    # 创建工作簿
    ws = xlwt.Workbook(encoding='utf-8')
    # 添加第一页数据表
    w = ws.add_sheet('sheet1') # 新建sheet（sheet的名称为"sheet1"）
    # 写入表头
    w.write(0, 0, u'地名')
    w.write(0, 1, u'次数')
    w.write(0, 2, u'经度')
    w.write(0, 3, u'纬度')
    
    # 写出到IO
    output = BytesIO()
    ws.save(output)
    # 重新定位到开始
    output.seek(0)
    response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename='+'test'+'.xls'
    #response.write(output.getvalue())
    return response

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
def database(request):

    devices = Devices.objects.all()#.order_by("user_id")
    if not devices:
        return render(request, 'backend/manage_database.html', {'is_device':0})
    device_id = request.GET.get('device', 1)

    root_device = os.path.join(STATIC_ROOT,"D{}".format(device_id))
    device_content = os.listdir(root_device)

    co_id = request.GET.get('co_id', device_content[0])
    root_co = os.path.join(root_device,co_id)

    i = 1
    img_path_list = []
    img_index = []
    while True:
        path_photo = os.path.join(root_co, '{}'.format(i))
        if os.path.isdir(path_photo):
            img_path_list.append("files/photo/D{}/{}/{}/7/0_0.jpg".format(device_id, co_id, i))
            if i%6 == 0:
                img_index.append(1)
            else:
                img_index.append(0)
            i+=1
        else:
            break
    
    img_index[-1] = 0

    co_id = request.GET.get('co_id', device_content[0])
    content = {}
    content['is_device'] = 1
    content['devices'] = devices
    content['co'] = device_content
    content['device_id'] = device_id
    content['co_id'] = co_id
    content['imgs'] = zip(img_path_list, img_index, [j for j in range(1,i)])

    return render(request, 'backend/manage_database.html', content)

@login_decorator()
def device_add(request):
    devices = Devices(name = request.GET.get('name'), resolution = request.GET.get('resolution'))
    devices.save()
    return redirect(reverse('manager_database'))

@login_decorator()
def full_img(request):
    device = request.GET.get('device')
    co = request.GET.get('co_id')
    img = request.GET.get('img_num')

    url_img = "files/photo/D{}/{}/{}/".format(device, co, img)
    url_xml = "files/photo/D{}/{}/xml/{}.xml".format(device, co, img)
    return render(request, 'backend/manage_full_img.html', {'device':device, 'co_id':co, 'url_img':url_img, 'url_xml':url_xml})

@csrf_exempt
def upload(request):
    file = request.FILES.get('file',None)
    name = request.FILES['file'].name
    co_num = request.POST.get('num','1')

    file_path = settings.STATIC_ROOT
    #if not os.path.exists(file_path):               # 文件夹不存在则创建
    #    os.mkdir(file_path)

    global num_progress
    process_all_num = len(list(file.chunks()))
    j = 0
    with open(os.path.join(file_path,name),'wb') as fp:    # 写文件
        for i in file.chunks():
            fp.write(i)
            j+=1
            #num_progress = j/process
            process_get = Process.objects.all().order_by('id').last()
            process_get.process = int(j*100/process_all_num)
            process_get.save()
    return JsonResponse({'status':True,'msg':'ok'})


def process(request):
    status = request.GET.get('status', 0)
    #global num_progress
    if int(status) == 0:
        num_progress = 0
        process_get = Process(process = 0, status = 0)
        process_get.save()
        return JsonResponse(process_get.process, safe =False)
    else:
        process_get = Process.objects.all().order_by('id').last()
        return JsonResponse({'process':process_get.process, 'text':'{}%'.format(process_get.process)})



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
    record_find = Records.objects.all()#.order_by("user_id")
    #paginator = Paginator(record_find, 20)
    #page_num = request.GET.get('page', 1)
    #record_find_page = paginator.get_page(page_num)
    return render(request, 'backend/manage_records_list.html', {'records_list':record_find})

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
    Users.objects.get(id = user_id).delete()
    Records.objects.filter(user_id = user_id).delete()
    Question.objects.filter(user_id = user_id).delete()
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

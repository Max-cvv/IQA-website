from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from website.models import Users, Records, Managers, Question, Devices, Process, Lab
from django.contrib.auth import logout
from utils.utils import login_decorator, compute_rank_scores, extract_pair_data, unzip_file, transpose_img
from io import BytesIO
import xlwt
import os
import deepzoom
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


from django.conf import settings
STATIC_ROOT = os.path.join(settings.STATIC_ROOT, 'files/photo')

def get_paginator(data, page_number, per_page_num):
    context = {}
    paginator = Paginator(data, per_page_num)
    page = paginator.get_page(page_number)
    #context[list_name] = page
    context['count'] = paginator.count
    context['num_pages'] = paginator.num_pages
    context['per_page'] = paginator.per_page
    context['has_next'] = page.has_next()
    if context['has_next']:
        context['next_page_number'] = page.next_page_number()
    
    context['has_previous'] = page.has_previous()
    if context['has_previous']:
        context['previous_page_number'] = page.previous_page_number()
    context['start_index'] = page.start_index()
    context['end_index'] = page.end_index()
    context['page_range'] = paginator.page_range

    context['page_number'] = page_number
    
    return page, context

# Create your views here.
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
        ranklist.append([name[rank[0]], 'style = width:'+str(round(rank[1],2))+'%;'+color[i%8], str(round(rank[1],2))])
        i+=1
    return render(request, 'backend/manage_rank.html', {'ranks':ranklist})


def excel(request):
    
    """导出excel表"""
    # 创建工作簿
    ws = xlwt.Workbook(encoding='utf-8')
    # 添加第一页数据表
    w = ws.add_sheet('设备信息') # 新建sheet
    # 写入表头
    w.write(0, 0, u'设备id')
    w.write(0, 1, u'手机型号')
    w.col(1).width = 256*20
    w.write(0, 2, u'分辨率')
    w.col(2).width = 256*10
    devices = Devices.objects.all().order_by('id')
    i = 1
    for device in devices:
        w.write(i, 0, 'D{}'.format(device.id))
        w.write(i, 1, device.name)
        w.write(i, 2, device.resolution)
        i+=1

    # 添加第二页数据表
    w = ws.add_sheet('用户信息') # 新建sheet
    # 写入表头
    w.write(0, 0, u'用户id')
    w.write(0, 1, u'屏幕分辨率')
    w.write(0, 2, u'窗口大小')
    w.write(0, 3, u'登录时间')
    w.write(0, 4, u'提交时间')
    w.write(0, 5, u'年龄')
    w.write(0, 6, u'性别')
    w.write(0, 7, u'是否戴眼镜')
    w.write(0, 8, u'拍摄习惯')
    w.write(0, 9, u'教育背景')
    users = Users.objects.all().order_by('id')
    i = 1
    gender = ['男','女']
    age = ['1-20岁', '20-30岁', '30-50岁', '50岁以上']
    isGlasses = ['是','否']
    edu = ['高中及以下', '本科或专科', '研究生', '博士及以上']
    pho = ['经常', '一般', '很少', '几乎没有']
    for user in users:
        w.write(i, 0, user.id)
        w.write(i, 1, '{}*{}'.format(user.screen_width, user.screen_height))
        w.write(i, 2, '{}*{}'.format(user.window_width, user.window_height))
        w.write(i, 3, '{}'.format(user.login_time))
        w.write(i, 4, '{}'.format(user.submit_time))
       

        qs = Question.objects.get(user_id = user.id)
        
        w.write(i, 5, age[int(qs.age) -1])
        w.write(i, 6, gender[int(qs.gender) -1])
        w.write(i, 7, isGlasses[int(qs.isGlasses) -1])
        w.write(i, 8, pho[int(qs.pho) -1])
        w.write(i, 9, edu[int(qs.edu) -1])
        i+=1

    # 添加第三页数据表
    w = ws.add_sheet('操作记录') # 新建sheet
    # 写入表头
    w.write(0, 0, u'记录id')
    w.write(0, 1, u'用户id')
    w.write(0, 2, u'图片1')
    w.write(0, 3, u'图片2')
    w.write(0, 4, u'选择结果')
    w.write(0, 5, u'拖动操作')
    w.write(0, 6, u'放缩操作')
    w.write(0, 7, u'提交时间')
    w.col(2).width = 256*15
    w.col(3).width = 256*15
    record_find = Records.objects.all()
    i = 1
    
    for record in record_find:
        w.write(i, 0, record.id)
        w.write(i, 1, record.user_id)
        w.write(i, 2, 'D{}-CO{}-{}'.format(record.device1, record.co1, record.img_num1))
        w.write(i, 3, 'D{}-CO{}-{}'.format(record.device2, record.co2, record.img_num2))
        if record.result == 0:
            w.write(i, 4, 1)
        elif record.result == 1:
            w.write(i, 4, 2)
        else:
            w.write(i, 4, 0)
        
        w.write(i, 5, record.operation)
        w.write(i, 6, record.operation_scroll)
        w.write(i, 7, '{}'.format(record.submit_time))
        i+=1


    # 写出到IO
    output = BytesIO()
    ws.save(output)
    # 重新定位到开始
    output.seek(0)
    response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename='+'database'+'.xls'
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
            return redirect(reverse('manager_database'))
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
    device_content.sort(key = lambda x: int(x[2:]))

    co_id = request.GET.get('co_id', device_content[0])
    root_co = os.path.join(root_device,co_id)

    photo_list = os.listdir(root_co)
    if 'xml' in photo_list:
        photo_list.remove('xml')
    photo_list.sort(key=lambda x: int(x))

    i = 1
    img_path_list = []
    img_index_tab = []
    img_index = []
    for photo_item in photo_list:
        img_path_list.append("files/photo/D{}/{}/{}/7/0_0.jpg".format(device_id, co_id, photo_item))
        img_index.append(int(photo_item))
        if i%6 == 0:
            img_index_tab.append(1)
        else:
            img_index_tab.append(0)
        i+=1
        
    
    img_index_tab[-1] = 0

    co_id = request.GET.get('co_id', device_content[0])
    content = {}
    content['is_device'] = 1
    content['devices'] = devices
    content['co'] = device_content
    content['device_id'] = device_id
    content['co_id'] = co_id
    content['imgs'] = zip(img_path_list, img_index_tab, img_index)

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
    #由于上传文件很大，处理时间长，需要配置nginx最大上传和响应时间
    file = request.FILES.get('file',None)
    if not file:
        return JsonResponse({'status':False,'msg':'ok'})
    name = request.FILES['file'].name
    device_num = request.POST.get('device_num','1')
    co_num = request.POST.get('co_num','1')

    file_path = os.path.join(settings.STATIC_ROOT, 'upload', name)
    

    process_get = Process.objects.all().order_by('id').last()
    process_get.status = 1
    process_get.save()

    #将上传的压缩包写入存储中
    process_all_num = len(list(file.chunks()))  #用于记录进度
    j = 0

    with open(file_path,'wb') as fp:    # 写文件
        for i in file.chunks():
            fp.write(i)
            j+=1
            process_get = Process.objects.all().order_by('id').last()
            process_get.process = int((j*100/process_all_num)/2)
            process_get.save()
    
    #处理为deepzoom
    photo_path = os.path.join(settings.STATIC_ROOT, 'upload', 'photo')
    isExists = os.path.exists(photo_path)
    if not isExists:
        os.makedirs(photo_path)

    
    unzip_file(file_path, photo_path)
    os.remove(file_path)
    photo_list = os.listdir(photo_path)
    photo_list.sort(key=lambda x: int(os.path.splitext(x)[0]))

    process_all_num = len(photo_list)
    j = 0

    creator = deepzoom.ImageCreator(
        tile_size=256,
        tile_overlap=1,
        tile_format="jpg",
        image_quality=1,
        #resize_filter="bicubic",
        #resize_filter="nearest",
    )

    for photo in photo_list:
        photo_src = os.path.join(photo_path, photo)
        if os.path.splitext(photo)[1] == '.bmp':
            pass
        else:
            transpose_img(photo_src)
        root_path = os.path.join(STATIC_ROOT,"D{}/co{}".format(device_num, co_num))
        
        xml_path = os.path.join(root_path, 'xml')
        isExists = os.path.exists(xml_path)
        if not isExists:
            os.makedirs(xml_path)

        
        photo_num =os.path.splitext(photo)[0]
        photo_dest = os.path.join(root_path, photo_num)
        xml_dest = os.path.join(xml_path, '{}.xml'.format(photo_num))
        creator.create(photo_src, photo_dest, xml_dest)
        os.remove(photo_src)
        j+=1
        process_get = Process.objects.all().order_by('id').last()
        process_get.process = 50 + int((j*100/process_all_num)/2)
        process_get.save()
    

    return JsonResponse({'status':True,'msg':'ok'})

#处理前端的处理进度请求
def process(request):
    status = request.GET.get('status', 0)
    if int(status) == 0:
        process_get = Process(process = 0, status = 0)
        process_get.save()
        return JsonResponse(process_get.process, safe =False)
    else:
        process_get = Process.objects.all().order_by('id').last()
        return JsonResponse({'status': process_get.status, 'process':process_get.process, 'text':'{}%'.format(process_get.process)})



@login_decorator()
def manager_users_list(request):
    user_find = Users.objects.all().order_by('id')
    page_num = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    
    user_find,context  = get_paginator(user_find, page_num, per_page)
    return render(request, 'backend/manage_users_list.html', {'users_list':user_find, 'context':context})

@login_decorator()
def manager_question_list(request):
    gender = ['男','女']
    age = ['1-20岁', '20-30岁', '30-50岁', '50岁以上']
    isGlasses = ['是','否']
    edu = ['高中及以下', '本科或专科', '研究生', '博士及以上']
    pho = ['经常', '一般', '很少', '几乎没有']

    qas = Question.objects.all().order_by("user_id")
    page_num = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    
    qas_page,context  = get_paginator(qas, page_num, per_page)
    for qs in qas_page:
        qs.gender = gender[int(qs.gender) -1]
        qs.age = age[int(qs.age) -1]
        qs.isGlasses = isGlasses[int(qs.isGlasses) -1]
        qs.edu = edu[int(qs.edu) -1]
        qs.pho = pho[int(qs.pho) -1]
    return render(request, 'backend/manage_question_list.html', {'qas':qas_page, 'context':context})



@login_decorator()
def manager_records_list(request):
    record_find = Records.objects.all().order_by("user_id")
    page_num = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    
    record_find_page,context  = get_paginator(record_find, page_num, per_page)
    return render(request, 'backend/manage_records_list.html', {'records_list':record_find_page, 'context':context})



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

@login_decorator()
def manage_lab(request):
    labs = Lab.objects.all()
    if Lab.objects.filter(status=1):
        is_start=1
    else:
        is_start=0
    return render(request, 'backend/manage_lab.html', {'labs':labs, 'is_start':is_start})

@login_decorator()
def lab_status(request, lab_id):
    lab = Lab.objects.get(id = lab_id)
    if lab.status == 0:
        if Lab.objects.filter(status=1):
            return HttpResponse("错误！")
        else:
            lab.status=1
            lab.save()
            return redirect(reverse('manager_lab'))
    else:
        lab.status=0
        lab.save()
        return redirect(reverse('manager_lab'))


def manage_logout(request):
    #request.session.clear()
    logout(request)
    return redirect(reverse('manager_login'))

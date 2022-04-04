# 图像主观质量评价网站
用于两两比较图像质量主观评价django-web项目

## 环境配置
1. 安装requirements.txt中的依赖项，项目中使用python3.6.9
2. 项目中使用deepzoom显示高分辨率图片，采用的[Python Deep Zoom Tools](https://github.com/openzoom/deepzoom.py)  
为满足项目需求，在使用时进行了一定修改，因此通过此项目中的deepzoom进行安装，方法如下：
    + 切换到项目中deepzoom目录下 `cd deepzoom`
    + 在此目录下 `python setup.py install`
## 如何使用
1. 项目目录下 `python manage.py runserver`
2. 第一步成功后登入网址即为主观实验平台，可以直接使用
3. 针对实验管理，将2中网址加上`/manage/`登入管理平台，用户名密码均为`admin`,管理平台功能如下：
    + 数据库：查看照片、增加设备、上传照片。对于上传照片，把照片（推荐为jpg格式）按顺序编号（1.jpg、2.jpg...），并将照片打包为zip压缩包，压缩包主目录下即为照片
    + 实验信息查看（用户列表、操作记录、问卷信息、实时排名）：查看一些主观评测的数据
    + 实验管理：自定义实验评测开始停止、评测内容、评测数量等
## 网站界面

1. 主页

   ![image-20220404161043837](https://cdn.jsdelivr.net/gh/Max-cvv/imagehosting/img/image-20220404161043837.png)

2. 实验界面

   ![image-20220404162053194](https://cdn.jsdelivr.net/gh/Max-cvv/imagehosting/img/image-20220404162053194.png)

3. 管理界面

   ![image-20220404161701745](https://cdn.jsdelivr.net/gh/Max-cvv/imagehosting/img/image-20220404161701745.png)

4. 部署在服务器上的网址

   [网站](http://39.97.96.45/)，服务器2022.5.4到期

from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=30, blank=True,null=True)
    check_list = models.CharField(max_length=30, blank=True,null=True)
    screen_width = models.IntegerField(blank=True,null=True)
    screen_height = models.IntegerField(blank=True,null=True)
    window_width = models.IntegerField(blank=True,null=True)
    window_height = models.IntegerField(blank=True,null=True)
    screen_colorDepth = models.IntegerField(blank=True,null=True)
    login_time = models.DateTimeField(blank=True,null=True)
    submit_time = models.DateTimeField(blank=True,null=True)

    record_now = models.IntegerField(blank=True,null=True)
    record_all = models.IntegerField(blank=True,null=True)

class Records(models.Model):
    user_id = models.IntegerField()
    user_record_id = models.IntegerField(blank=True,null=True)
    device1 = models.IntegerField(blank=True,null=True)
    device2 = models.IntegerField(blank=True,null=True)
    co1 = models.IntegerField(blank=True,null=True)
    co2 = models.IntegerField(blank=True,null=True)
    img_num1 = models.IntegerField(blank=True,null=True)
    img_num2 = models.IntegerField(blank=True,null=True)
    img1 = models.IntegerField(blank=True,null=True)
    img2 = models.IntegerField(blank=True,null=True)
    result = models.IntegerField(blank=True,null=True)
    operation = models.IntegerField(blank=True,null=True)
    operation_scroll = models.IntegerField(blank=True,null=True)
    op_time = models.IntegerField(blank=True,null=True)
    submit_time = models.DateTimeField(blank=True,null=True)

class Managers(models.Model):
    user_id = models.CharField(max_length=30)
    user_password = models.CharField(max_length=30)

class Question(models.Model):
    user_id = models.IntegerField(blank=True,null=True)
    age = models.IntegerField()
    isGlasses = models.IntegerField()
    gender = models.IntegerField()
    edu = models.IntegerField()
    pho = models.IntegerField()
    screen = models.CharField(max_length=60,blank=True,null=True)

class Tiaomu(models.Model):
    img1 = models.IntegerField(blank=True,null=True)
    img2 = models.IntegerField(blank=True,null=True)
    

class Devices(models.Model):
    name = models.CharField(max_length=30)
    resolution = models.CharField(max_length=30)
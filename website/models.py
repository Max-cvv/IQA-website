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

class Records(models.Model):
    user_id = models.IntegerField()
    img1 = models.IntegerField()
    img2 = models.IntegerField()
    result = models.IntegerField()
    operation = models.IntegerField()
    operation_scroll = models.IntegerField()
    op_time = models.IntegerField()

class Managers(models.Model):
    user_id = models.CharField(max_length=30)
    user_password = models.CharField(max_length=30)
    

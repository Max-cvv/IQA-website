from django.urls import path
from website import views

urlpatterns = [
    
    path('', views.homepage, name = "homepage"),
    path('subbmit_success/', views.homepage_after, name = "homepage_after"),

    path('login/', views.log_in, name = 'user_login'),
    path('index/', views.index, name = 'index'),


    path('record/',  views.record, name = 'record'),
   
    path('hand_form/', views.hand_form),

    path('creatRecordList/', views.creatRecordList),
]

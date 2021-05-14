from django.urls import path
from backend import views

urlpatterns = [
    
    #认证，注销
    path('', views.manager_login, name = 'manager_login'),
    path('logout/', views.manage_logout, name = 'manager_logout'),

    path('0/', views.database, name = 'manager_database'),
    path('1/', views.manager_users_list, name = 'manager_users_list'),
    path('2/', views.manager_records_list, name = 'manager_records_list'),
    path('3/', views.manager_question_list, name = 'manager_question_list'),
    path('4/', views.get_rank, name = 'manager_question_list'),


    path('0/add_device/', views.device_add),
    path('0/full_img/', views.full_img),
    path('0/upload/', views.upload, name = 'upload'),
    path('0/process/', views.process, name = 'process'),

    path('excel/', views.excel),

    path('delete/<user_id>/', views.user_delete),
    path('adduser/', views.user_add),
    path('record/delete/<record_id>/', views.record_delete),
]

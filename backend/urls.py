from django.urls import path
from backend import views

urlpatterns = [
    
    #认证，注销
    path('', views.manager_login, name = 'manager_login'),
    path('logout/', views.manage_logout, name = 'manager_logout'),

    path('1/', views.manager_users_list, name = 'manager_users_list'),
    path('2/', views.manager_records_list, name = 'manager_records_list'),
    path('reset/<user_id>/', views.user_reset),
    path('delete/<user_id>/', views.user_delete),
    path('adduser/', views.user_add),
    path('record/delete/<record_id>/', views.record_delete),
]

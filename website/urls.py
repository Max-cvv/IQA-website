from django.urls import path
from website import views

urlpatterns = [
    path('', views.log_in, name = 'login'),
    path('index/', views.index, name = 'index'),
    path('manage/', views.manager_login, name = 'manager_login'),
    path('manage/1/', views.manager_users_list, name = 'manager_users_list'),
    path('manage/2/', views.manager_records_list, name = 'manager_records_list'),
    path('reset/<user_id>/', views.user_reset),
    path('delete/<user_id>/', views.user_delete),
    path('adduser/', views.user_add),
    path('record_delete/<record_id>/', views.record_delete),

    path('manage_logout/', views.manage_logout),

    path('record/',  views.record, name = 'record'),
    path('submit/', views.submit, name = 'submit'),
    path('get_next/', views.get_next, name = 'get_next'),
]

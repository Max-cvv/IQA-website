from django.urls import path
from website import views

urlpatterns = [
    path('', views.log_in, name = 'login'),
    path('index/', views.index, name = 'index'),
    path('manage/', views.manager_login, name = 'manager_login'),
    path('manage_site/', views.manager_index, name = 'manager_index'),
    path('record/',  views.record, name = 'record'),
    path('submit/', views.submit, name = 'submit'),
    path('get_next/', views.get_next, name = 'get_next'),
]

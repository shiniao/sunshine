from django.urls import path

from . import views, auth

urlpatterns = [
    # path('account/'),

    # 获取某个用户所有todo
    path('todos/', views.todo_list, name='todo_list'),
    # 获取单个todo
    path('todos/<str:uuid>/', views.todo_detail, name='todo_detail'),

    # jwt
    # path('login/', views.login),
    # path('register/', views.register),

]

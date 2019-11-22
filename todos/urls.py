from django.urls import path

from . import views

urlpatterns = [
    # 所有todos
    path('todos/a/', views.todos_list, name='todo_list'),
    # 单个todo
    path('todos/a/<int:id>/', views.todo_detail, name='todo_detail'),

    # 已完成todos
    path('todos/f/', views.todo_finished_list, name='todo_finished_list'),

    # 分页排序todos(finished=false)
    path('todos/<str:sort>/', views.todo_page_list, name='todo_page_list'),

]

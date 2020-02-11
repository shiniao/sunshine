import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods

from todos.models import Todo
from .auth import auth_required, parser
from .utils import my_response


# There is views.


@auth_required
@require_http_methods(['GET', 'POST'])
def todo_list(request, user):
    if request.method == 'GET':
        # 获取该用户的所有土豆
        todo_all = user.todos.all()

        # TODO 去除今天之前的土豆

        # 每页多少todo，默认5个
        per_page = request.GET.get('per_page', 5)
        paginator = Paginator(todo_all, per_page)
        # 请求页数,默认第一页
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        data = {
            'count': len(page_obj),
            'todos': [model_to_dict(page) for page in page_obj]
        }
        return my_response(data)

    if request.method == 'POST':
        # 添加一个土豆
        todo_new = json.loads(request.body)
        try:
            todo = Todo()
            for k, v in todo_new.items():
                todo.k = v

            todo.owner = user
            todo.save()

        except Exception as e:
            return my_response(message='Database error', code=400)

        return my_response('Create success')


@require_http_methods(['GET', 'PUT', 'DELETE'])
def todo_detail(request, id, user):
    # 获取用户的todo信息
    try:
        todo = user.todos.get(id=id)
    except Todo.DoesNotExist:
        return my_response(message='Todo does not exist', code=400)

    if request.method == 'GET':
        return my_response(model_to_dict(todo))

    elif request.method == 'PUT':
        # 解析请求的json数据
        todo_new = json.loads(request.body)
        for k, v in todo_new.items():
            # 不允许修改创建时间和拥有者
            if k == 'created':
                return my_response(message='Created field forbidden change', code=403)
            if k == 'owner':
                return my_response(message='Owner field forbidden change', code=403)

            todo.k = v

        todo.save()
        return my_response('Success update')

    elif request.method == 'DELETE':
        todo.delete()

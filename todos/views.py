import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods

from todos.models import Todo
from .auth import auth_required
from .utils import my_response, bad_request_400, forbidden_403, not_found_404, http_methods_required


# There is views.


@auth_required
@http_methods_required(['GET', 'POST'])
def todo_list(request, user):
    if request.method == 'GET':
        # 获取该用户的所有土豆
        todo_all = user.todos.all()

        # 去除今天之前的土豆
        todo_all = [todo for todo in todo_all if not todo.is_past()]

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

        for k, v in todo_new.items():
            if k not in Todo.__dict__:
                return bad_request_400('Todo field error')

        try:
            todo = Todo(**todo_new)
            todo.owner = user
            todo.save()

        except Exception as e:
            return bad_request_400(message='Database error')

        return my_response('Create success')


@auth_required
@http_methods_required(['GET', 'PUT', 'DELETE'])
def todo_detail(request, user, uuid):
    # 获取用户的todo信息
    try:
        # 土豆不存在
        todo = user.todos.get(uuid=uuid)
    except Todo.DoesNotExist:
        return not_found_404('Todo does not exist')

    # 土豆已经过期
    if todo.is_past():
        return bad_request_400(message='Todo is expired')

    if request.method == 'PUT':
        # 解析请求的json数据
        todo_new = json.loads(request.body)
        for k, v in todo_new.items():
            if k not in Todo.__dict__:
                return bad_request_400('Todo field error')
            # 不允许修改创建时间和拥有者
            if k == 'created':
                return forbidden_403('Created field forbidden change')
            if k == 'owner':
                return forbidden_403('Owner field forbidden change')
        try:
            todo.__dict__.update(**todo_new)
            todo.save()
        except Exception as e:
            return bad_request_400('Database error')

        return my_response('Success update')

    if request.method == 'DELETE':
        todo.delete()
        return my_response('Delete success')

    return my_response(model_to_dict(todo))

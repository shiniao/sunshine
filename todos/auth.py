import json
import time

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from todos.utils import my_response


@require_http_methods(['POST'])
def login(request):
    """sign the token string"""

    # 获取用户信息
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            return my_response(message="User does not exist", code=401)
        if not user.check_password(data.get('password')):
            return my_response(message="Password is wrong", code=401)
        else:
            payload = {
                # 签发者
                "iss": "shiniao",
                # 签发时间
                "iat": int(time.time()),
                # 过期时间
                "exp": int(time.time()) + 86400 * 7,
                # 用户名
                "username": data.get('username')
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
            return my_response(token)


@require_http_methods(['POST'])
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # 如果用户已经存在
        if User.objects.get(username=data['username']) is not None:
            return my_response('User already exist', 400)

        u = User()
        for k, v in data.items:
            u.k = v
        u.save()
        # TODO 邮箱验证
        return my_response('User create success')


def auth_required(func):
    """jwt authorization"""

    def wrapper(request, *args, **kwargs):
        try:
            auth = request.headers.get('Authorization').split()
        except AttributeError:
            return my_response('No authenticate header', 401)

        if auth[0] == 'Bearer':
            try:
                # decode the jwt information, get the username char
                data = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return my_response('Token expired', 401)
            except jwt.InvalidTokenError:
                return my_response('Invalid token', 401)
            except Exception as e:
                return my_response('Can not get the user object', 401)

            username = data.get('username')

            try:
                # get the db user
                user = User.objects.get(username=username)
                kwargs['user'] = user
            except User.DoesNotExist:
                return my_response(message="User does not exist", code=401)

            if not user.is_active:
                return my_response(message="User inactive or deleted", code=401)

        else:
            return my_response(message="The auth type not supported", code=401)

        return func(request, *args, **kwargs)

    return wrapper

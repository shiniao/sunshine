import json
import time

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from todos.utils import my_response, not_found_404, forbidden_403, bad_request_400, unauthorized_401, \
    not_allowed_method_405, http_methods_required


@http_methods_required(['POST'])
def login(request):
    """sign the token string"""

    # 获取用户信息
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            # 判断用户是否存在
            user = User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            return not_found_404("User does not exist")

        # 检查密码
        if not user.check_password(data.get('password')):
            return bad_request_400("Password is wrong")

        # 签发token
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


@http_methods_required(['POST'])
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # todo 判断user字段是否正确

        # 如果用户已经存在
        if User.objects.get(username=data['username']) is not None:
            return bad_request_400('User already exist')

        try:
            u = User(**data)
            u.save()
        except Exception as e:
            return my_response('Database error', 400)

        # TODO 邮箱验证
        return my_response('User create success')


def auth_required(func):
    """jwt authorization"""

    def wrapper(request, *args, **kwargs):
        try:
            auth = request.headers.get('Authorization').split()
        except AttributeError:
            return unauthorized_401()

        if auth[0] == 'Bearer':
            try:
                # decode the jwt information, get the username char
                data = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return unauthorized_401('Token expired')
            except jwt.InvalidTokenError:
                return unauthorized_401('Invalid token')
            except Exception as e:
                return unauthorized_401('Can not get the user object')

            username = data.get('username')

            try:
                # get the db user
                user = User.objects.get(username=username)
                kwargs['user'] = user
            except User.DoesNotExist:
                return not_found_404("User does not exist")

            if not user.is_active:
                return bad_request_400("User inactive or deleted")

        else:
            return unauthorized_401(message="The auth type not supported")

        return func(request, *args, **kwargs)

    return wrapper

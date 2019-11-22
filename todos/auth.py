import time

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# 签发token
@api_view(['POST'])
def sign(request):
    # 获取用户信息
    if request.method == 'POST':
        data = request.data
        try:
            user = User.objects.get(email=data.get('email'))
        except User.DoesNotExist:
            return Response({"message": "User Does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(data.get('password')):
            return Response({"message": "Password is wrong"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            payload = {
                # 签发者
                "iss": "shiniao.fun",
                # 签发时间
                "iat": int(time.time()),
                # 过期时间
                "exp": int(time.time()) + 86400 * 7,
                "email": data.get('email')
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('ascii')
            return Response({"token": token})


# 解析token中的username
def parser(request):

    auth = request.headers.get('Authorization')
    auth = auth.split()
    # 用户通过API获取数据验证流程
    if auth[0] == 'Bearer':
        try:
            data = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
            username = data.get('username')
        except Exception as e:
            return None

        try:
            # 获取token中的username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        return user

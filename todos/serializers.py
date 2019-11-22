from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Todo


# 用户序列化
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# todos序列化
class TodoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Todo
        fields = ('id', 'title', 'finished', 'expired', 'priority', 'owner')

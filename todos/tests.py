# Create your tests here.
import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import Todo
from django.utils import timezone
import datetime


class TestTodosModel(TestCase):

    def test_is_today(self):
        # 未来土豆
        # TODO 未来土豆不能删除
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_todo = Todo(created=future_date)
        self.assertIs(future_todo.is_today(), False)

        # 过去土豆
        past_date = timezone.now() + datetime.timedelta(days=-1)
        past_todo = Todo(created=past_date)
        self.assertIs(past_todo.is_today(), False)

        # 现在土豆
        now_todo = Todo(created=timezone.now())
        self.assertIs(now_todo.is_today(), True)


class TestTodosViews(TestCase):
    """测试视图函数"""

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username='user1', password='123123')
        self.user2 = User.objects.create_user(username='user2', password='123123')

        for i in range(5):
            Todo.objects.create(
                title='test{}'.format(i),
                owner=self.user1)
        data = {
            "username": "user1",
            "password": "123123"
        }
        rsp = self.client.post('/auth/login/', data, content_type='application/json')
        token = rsp.json()['message']
        self.client = Client(
            HTTP_AUTHORIZATION='Bearer {}'.format(token),
            HTTP_CONTENT_TYPE='application/json')

    def test_router_todos_get(self):
        rsp = self.client.get('/api/v1/todos/', {'per_page': 3, 'page': 1})
        self.assertEqual(rsp.status_code, 200, rsp.json())
        self.assertEqual(rsp.json()['message']['count'], 3)
        self.assertEqual(len(rsp.json()['message']['todos']), 3)

    def test_router_todos_post(self):
        todo = {
            'title': '烫头'
        }
        rsp = self.client.post('/api/v1/todos/',
                               data=json.dumps(todo),
                               content_type='application/json')
        print(rsp.json())
        self.assertEqual(rsp.status_code, 200, rsp.json())
        self.assertContains(rsp.json()['message'], 'success')

    def test_router_todo_get(self):
        rsp = self.client.get('/api/v1/todos/1/')
        self.assertEqual(rsp.status_code, 200, rsp.json())
        self.assertEqual(rsp.json()['message']['title'], 'test0')

    def test_router_todo_post_put(self):
        data = {
            'title': '抽烟',
        }
        rsp = self.client.post('/api/v1/user1/todos/1/', data=data, content_type='application/json')
        self.assertEqual(rsp.status_code, 200, rsp.json())
        todo = Todo.objects.get(id=1)
        self.assertEqual(todo.title, data['title'])


class TestAuth(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='auth_user', password='123456')

    def test_token(self):
        data = {
            "username": "auth_user",
            "password": "123456"
        }
        rsp = self.client.post('/auth/login/', data, content_type='application/json')
        self.assertEqual(rsp.status_code, 200, rsp.json())

    def test_auth_requirement(self):
        pass

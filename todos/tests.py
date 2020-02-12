# Create your tests here.
import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import Todo
from django.utils import timezone
import datetime


class TestTodosModel(TestCase):
    """测试数据库model"""

    def test_is_past(self):
        # 未来土豆
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_todo = Todo(created=future_date)
        self.assertIs(future_todo.is_past(), False)

        # 过去土豆
        past_date = timezone.now() + datetime.timedelta(days=-1)
        past_todo = Todo(expired=past_date)
        self.assertIs(past_todo.is_past(), True)

        # 现在土豆
        now_todo = Todo(created=timezone.now())
        self.assertIs(now_todo.is_past(), False)


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
        # 获取token
        rsp = self.client.post('/auth/login/', data, content_type='application/json')
        token = rsp.json()['message']
        self.client = Client(
            HTTP_AUTHORIZATION='Bearer {}'.format(token),
            HTTP_CONTENT_TYPE='application/json')

    # TODO test
    def test_todo_remove_past(self):
        pass

    def test_todos_get(self):
        rsp = self.client.get('/api/v1/todos/', {'per_page': 3, 'page': 1})
        self.assertEqual(rsp.status_code, 200, rsp.json())
        self.assertEqual(rsp.json()['message']['count'], 3)
        self.assertEqual(len(rsp.json()['message']['todos']), 3)

    def test_todos_post(self):
        todo = {
            'title': '烫头'
        }
        rsp = self.client.post('/api/v1/todos/',
                               data=json.dumps(todo),
                               content_type='application/json')
        print(rsp.json())
        self.assertEqual(rsp.status_code, 200)
        dtodo = self.user1.todos.get(title=todo['title'])
        self.assertEqual(dtodo.title, todo['title'])

    def test_todo_get(self):
        uuid = self.user1.todos.all()[0].uuid
        rsp = self.client.get('/api/v1/todos/{}/'.format(uuid))
        self.assertEqual(rsp.status_code, 200, rsp.json())
        self.assertEqual(rsp.json()['message']['title'], 'test0')

    def test_todo_put(self):
        """测试更新土豆"""
        data = {
            'title': '抽烟',
        }
        uuid = self.user1.todos.all()[0].uuid
        rsp = self.client.put('/api/v1/todos/{}/'.format(uuid),
                              data=data,
                              content_type='application/json')
        self.assertEqual(rsp.status_code, 200)
        todo = self.user1.todos.all()[0]
        self.assertEqual(todo.title, data['title'])

    def test_todo_delete(self):
        """测试删除土豆"""
        uuid = self.user1.todos.all()[0].uuid
        rsp = self.client.delete('/api/v1/todos/{}/'.format(uuid))
        print(rsp.content)
        self.assertEqual(rsp.status_code, 200)
        with self.assertRaises(Todo.DoesNotExist) as e:
            self.user1.todos.get(uuid=uuid)

    def test_todo_field_error(self):
        """测试字段不正确情况下报错"""
        data = {
            'titl': '抽烟',
        }
        uuid = self.user1.todos.all()[0].uuid
        rsp = self.client.put('/api/v1/todos/{}/'.format(uuid),
                              data=data,
                              content_type='application/json')
        self.assertEqual(rsp.status_code, 400)


class TestAuth(TestCase):
    """测试jwt认证"""

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


class TestUtils(TestCase):

    def test_http_methods_required(self):
        rsp = self.client.get('/auth/login/')
        self.assertEqual(rsp.status_code, 405)

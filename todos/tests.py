# Create your tests here.
from django.test import TestCase
from .models import Todo
from django.utils import timezone
import datetime

class TestTodosModel(TestCase):
    def test_is_today(self):

        # 未来土豆
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


class TestAuth(TestCase):
    def test_sing(self):
        pass

    def test_paser(self):
        pass
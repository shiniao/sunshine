from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
import uuid


# There is models.


class Todo(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # 标题
    title = models.CharField(max_length=50)
    # 描述
    description = models.TextField(default="")
    # 是否完成(默认未完成)
    finished = models.BooleanField(default=False)
    # 创建时间（创建时自动生成，不更新）
    created = models.DateTimeField(auto_now_add=True)
    # 更新时间 (创建时生成后期自动更新)
    updated = models.DateTimeField(auto_now=True)
    # 过期时间
    expired = models.DateField(null=True)
    # 优先级(默认0代表没有优先级)
    priority = models.IntegerField(default=0)
    # 拥有者
    owner = models.ForeignKey(
        'auth.User', related_name='todos', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def is_past(self):
        """判断土豆是否过期， 今天之前的全部过期，不显示"""
        if self.expired is None:
            return False
        return (self.expired.day - timezone.now().day) < 0

    class Meta:
        # 排序
        ordering = ["expired"]
        # permissions = [('can_create', 'Can create a todos')]

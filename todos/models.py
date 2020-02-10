from django.db import models
from django.utils import timezone

# There is models.


class Todo(models.Model):
    # 标题(不允许为空)
    title = models.CharField(max_length=300)
    # 完成(默认未完成)
    finished = models.BooleanField(default=False)
    # 创建时间（创建时自动生成）
    created = models.DateTimeField(auto_now_add=True)
    # 过期时间
    expired = models.DateField(blank=True, null=True)
    # 优先级(默认为3)
    priority = models.IntegerField(default=4)
    # 拥有者
    owner = models.ForeignKey(
        'auth.User', related_name='todos', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def is_today(self):
        """判断土豆是否过期， 如果不是当天创建的则过期"""
        return (timezone.now().day-self.created.day) == 0

    class Meta:
        # 排序
        ordering = ["expired"]

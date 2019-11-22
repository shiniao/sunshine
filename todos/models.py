from django.db import models


# There is models.

class Todo(models.Model):
    # 标题(不允许为空)
    title = models.CharField(max_length=300)
    # 完成(默认未完成)
    finished = models.BooleanField(default=False)
    # 过期时间
    expired = models.DateField(blank=True, null=True)
    # 优先级(默认为3)
    priority = models.IntegerField(default=4)
    # 拥有者
    owner = models.ForeignKey('auth.User', related_name='todos', on_delete=models.CASCADE)

    class Meta:
        # 排序
        ordering = ["expired"]

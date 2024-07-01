from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.phase.models import UserPhase


class User(AbstractUser):
    name = models.CharField(max_length=30, verbose_name="真实姓名")
    school = models.CharField(max_length=100, verbose_name="学校", blank=True, null=True, default="")
    department = models.CharField(max_length=50, verbose_name="所属院系", blank=True, null=True, default="")
    user_phase = models.ForeignKey(UserPhase, verbose_name="用户所处阶段", default=1, on_delete=models.CASCADE)
    score = models.CharField(max_length=10, verbose_name="成绩", blank=True, null=True, default="")
    memo = models.TextField(verbose_name="自我介绍", blank=True, null=True, default="")

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

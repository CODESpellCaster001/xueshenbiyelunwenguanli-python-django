from django.db import models
from apps.user.models import User


# Create your models here.
class Feedback2Teacher(models.Model):
    feedback = models.TextField(verbose_name="反馈内容", blank=True, null=True)
    teacher = models.ForeignKey(User, models.CASCADE)

    class Meta:
        verbose_name = '学生对教师的反馈'
        verbose_name_plural = verbose_name


class Feedback2Student(models.Model):
    feedback = models.TextField(verbose_name="反馈内容", blank=True, null=True)
    student = models.ForeignKey(User, models.CASCADE)

    class Meta:
        verbose_name = '教师对学生的反馈'
        verbose_name_plural = verbose_name

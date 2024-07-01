from django.db import models
from apps.user.models import User


# Create your models here.
class TopicRecord(models.Model):
    limit_num_choices = (
        (1, '限1人'),
        (2, '限2人'),
        (3, '限3人'),
    )

    title = models.CharField(max_length=100, verbose_name='题目')
    detail = models.TextField(verbose_name='描述')
    chosen_num = models.SmallIntegerField(verbose_name='已选人数', default=0)
    limit_num = models.SmallIntegerField(verbose_name='限选人数', choices=limit_num_choices)
    release_time = models.DateTimeField(verbose_name="出题时间", blank=True, null=True, auto_now=True)
    last_edit_time = models.DateTimeField(verbose_name="最后编辑时间", blank=True, null=True, auto_now_add=True)
    is_chosen = models.BooleanField(verbose_name='选题状态', default=0)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = verbose_name


class Topic2Teacher(models.Model):
    topic = models.ForeignKey(TopicRecord, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)


class Topic2Student(models.Model):
    topic = models.ForeignKey(TopicRecord, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

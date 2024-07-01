from django.db import models
from apps.topic_record.models import TopicRecord
from apps.user.models import User
from apps.phase.models import AnnexPhase


class Annex(models.Model):
    file = models.FileField(upload_to="fdfs", blank=True, null=True, verbose_name="附件")
    raw_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="原始文件名")
    detail = models.TextField('描述', default=" ")
    annex_phase = models.ForeignKey(AnnexPhase, default=7, on_delete=models.CASCADE, verbose_name="文件类型")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="上传者")
    topic = models.ForeignKey(TopicRecord, on_delete=models.CASCADE, blank=True, null=True, verbose_name="题目")

    class Meta:
        verbose_name = '文件'
        verbose_name_plural = verbose_name

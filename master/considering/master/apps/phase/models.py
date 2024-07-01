from django.db import models


# Create your models here.
class UserPhase(models.Model):
    phase_choice = (
        (1, '未选题'),
        (2, '等待指导老师和教学秘书确认选题'),
        (3, '指导老师已确认选题，等待教学秘书确认选题'),
        (4, '已选题'),
        (5, '未上传开题报告'),
        (6, '已经上传开题报告'),
        (7, '未上传中期报告'),
        (8, '已经上传中期报告'),
        (9, '未答辩'),
        (10, '等待指导老师和教学秘书确认答辩'),
        (11, '指导老师已确认答辩，等待教学秘书确认答辩'),
        (12, '已答辩'),

    )

    user_phase = models.CharField(verbose_name="用户所处阶段名称", max_length=100)

    class Meta:
        verbose_name = '用户阶段'
        verbose_name_plural = verbose_name


class AnnexPhase(models.Model):
    annex_phase = models.CharField(verbose_name="文件所属类型", max_length=100)

    class Meta:
        verbose_name = '文件类型'
        verbose_name_plural = verbose_name

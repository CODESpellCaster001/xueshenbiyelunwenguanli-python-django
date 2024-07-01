# Generated by Django 3.0.4 on 2020-04-26 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TopicRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='题目')),
                ('detail', models.TextField(verbose_name='描述')),
                ('chosen_num', models.SmallIntegerField(default=0, verbose_name='已选人数')),
                ('limit_num', models.SmallIntegerField(choices=[(1, '限1人'), (2, '限2人'), (3, '限3人')], verbose_name='限选人数')),
                ('release_time', models.DateTimeField(auto_now=True, null=True, verbose_name='出题时间')),
                ('last_edit_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='最后编辑时间')),
                ('chosen_topic_status', models.BooleanField(default=0, verbose_name='选题状态')),
            ],
            options={
                'verbose_name': '题目',
                'verbose_name_plural': '题目',
            },
        ),
    ]

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect

# Create your views here.
from rolepermissions.checkers import has_role

from apps.annex.forms import AnnexForm
from apps.annex.models import Annex
from apps.topic_record.models import Topic2Student, Topic2Teacher
from apps.user.models import User
from django.conf import settings
import os

from utils.fdfs.storage import FDFSStorage


@login_required
def upload_middle_topic(request):
    user = request.user
    user_obj = User.objects.get(id=user.id)
    if request.method == "POST":
        form = AnnexForm(request.POST)
        file = request.FILES.get("file")
        temp_file = "%s/%s" % (settings.MEDIA_ROOT, file.name)
        with open(temp_file, 'wb') as upload_files:
            for chunk in file.chunks():
                upload_files.write(chunk)

        file_path = os.path.abspath(temp_file)
        print("##本地文件绝对路径", file_path)
        fdfs_storage = FDFSStorage()
        remote_file_id = fdfs_storage.upload(file_path)[1]

        if form.is_valid():
            form = form.clean()
            print("##FORM内容:", form)
            if has_role(user_obj, ['student']):
                topic2student_obj = Topic2Student.objects.get(student=user.id)
                annex_topic = topic2student_obj.topic
                annex_obj = Annex.objects.create(file=remote_file_id, annex_phase_id=4, raw_name=form['raw_name'],
                                                 uploader=user,
                                                 detail="form.detail", topic=annex_topic)
                annex_obj.save()

                # 更改学生状态为已经上传中期文档
                user_obj.user_phase_id = 8
                user_obj.save()
                print("************************")
                print("学生状态")
                print(user_obj.user_phase_id)
                print("************************")
            elif has_role(user_obj, ['teacher']):
                # topic2teacher_obj = Topic2Teacher.objects.get(teacher_id=user.id)
                # annex_topic = topic2teacher_obj.topic
                annex_obj = Annex.objects.create(file=remote_file_id, annex_phase_id=3, raw_name=form['raw_name'],
                                                 uploader=user,
                                                 detail="中期报告模板", topic=None)
                annex_obj.save()
            else:
                return HttpResponse("你是个管理员吧？？？")
            return redirect(reverse('topic:my_topic'))

    return render(request, "middle_topic/upload_middle_topic.html")

@login_required
def download_middle_topic(request):
    user = request.user
    user_obj = User.objects.get(id=user.id)

    if has_role(user_obj, ['student']):
        topic2student_obj = Topic2Student.objects.get(student_id=user_obj.id)
        topic_id = topic2student_obj.topic_id
        topic2teacher_obj = Topic2Teacher.objects.get(topic_id=topic_id)
        teacher_obj = topic2teacher_obj.teacher

        open_topic_template = Annex.objects.get(uploader=teacher_obj, annex_phase_id=3)
        print(open_topic_template)
        uploader_name = User.objects.get(id=open_topic_template.uploader_id).name

        context = {
            'uploader_name': uploader_name,
            'open_topic_template': open_topic_template
        }
        return render(request, 'middle_topic/download_middle_topic.html', context=context)

    elif has_role(user_obj, ['teacher']):
        topic2teacher_list = Topic2Teacher.objects.filter(teacher_id=user.id)
        # 通过教师查询到题目
        print(isinstance(topic2teacher_list, list))
        topic_list = list()
        for topic2teacher_obj in topic2teacher_list:
            topic_list.append(topic2teacher_obj.topic)
        print(topic_list)

        topic_annex_dict = dict()
        for topic_obj in topic_list:
            topic_annex_dict[topic_obj] = Annex.objects.filter(annex_phase_id=4, topic_id=topic_obj.id)

        context = {
            "topic_annex_dict": topic_annex_dict
        }
        return render(request, 'middle_topic/download_middle_topic.html', context=context)
    else:
        pass

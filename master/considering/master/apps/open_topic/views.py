import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from rolepermissions.checkers import has_role
# Create your views here.
from apps.annex.forms import AnnexForm
from apps.annex.models import Annex
from apps.topic_record.models import Topic2Student, Topic2Teacher
from apps.user.models import User
from utils.common.get_name_role import get_name_role
from utils.fdfs.storage import FDFSStorage
from django.conf import settings


@login_required
def upload_open_topic(request):
    user = request.user
    user_obj = User.objects.get(id=user.id)
    # name = get_name_role(request)[0]
    # role = get_name_role(request)[1]
    # context = {
    #     "name": name,
    #     "role": role,
    # }
    if request.method == "POST":
        form = AnnexForm(request.POST)
        file = request.FILES.get("file")
        temp_file = "%s/%s" % (settings.MEDIA_ROOT, file.name)
        with open(temp_file, 'wb') as upload_files:
            for chunk in file.chunks():
                upload_files.write(chunk)

        file_path = os.path.abspath(temp_file)
        fdfs_storage = FDFSStorage()
        remote_file_id = fdfs_storage.upload(file_path)[1]

        if form.is_valid():
            form = form.clean()
            print("##FORM内容:", form)
            if has_role(user_obj, ['student']):
                topic2student_obj = Topic2Student.objects.get(student=user.id)
                annex_topic = topic2student_obj.topic
                annex_obj = Annex.objects.create(file=remote_file_id, annex_phase_id=2, raw_name=form['raw_name'],
                                                 uploader=user,
                                                 detail="form.detail", topic=annex_topic)
                annex_obj.save()
                # 更改学生状态为已经上传开题报告
                user_obj.user_phase_id = 6
                user_obj.save()
            elif has_role(user_obj, ['teacher']):
                # topic2teacher_obj = Topic2Teacher.objects.get(teacher_id=user.id)
                # annex_topic = topic2teacher_obj.topic
                annex_obj = Annex.objects.create(file=remote_file_id, annex_phase_id=1, raw_name=form['raw_name'],
                                                 uploader=user,
                                                 detail="开题报告模板", topic=None)
                annex_obj.save()
            else:
                return HttpResponse("你是个管理员吧？？？")
            return redirect(reverse('topic:my_topic'))

    return render(request, "open_topic/upload_open_topic.html")


@login_required
def download_open_topic(request):
    user = request.user
    user_obj = User.objects.get(id=user.id)
    name = get_name_role(request)[0]
    role = get_name_role(request)[1]
    if has_role(user_obj, ['student']):
        topic2student_obj = Topic2Student.objects.get(student_id=user_obj.id)
        topic_id = topic2student_obj.topic_id
        topic2teacher_obj = Topic2Teacher.objects.get(topic_id=topic_id)
        teacher_obj = topic2teacher_obj.teacher

        open_topic_template = Annex.objects.get(uploader=teacher_obj, annex_phase_id=1)
        print(open_topic_template)
        uploader_name = User.objects.get(id=open_topic_template.uploader_id).name

        context = {
            "name": name,
            "role": role,
            'uploader_name': uploader_name,
            'open_topic_template': open_topic_template
        }
        return render(request, 'open_topic/download_open_topic.html', context=context)

    elif has_role(user_obj, ['teacher']):
        # 教师下载的是当前题目下，所有学生的开题报告
        # teacher_obj = User.objects.get(id=user.id)
        # topic2teacher_objs = Topic2Teacher.objects.filter(teacher_id=user.id)
        # topic_obj_list = list()
        # annex_obj_list = list()
        # for topic_obj in topic2teacher_objs:
        #     topic_obj_list.append(topic_obj.topic)
        #     # topic_annex_list = Annex.objects.filter(topic=topic_obj.topic)
        # for topic in topic_obj_list:
        #     topic_annex_list = Annex.objects.filter(annex_phase_id=2, topic_id=99)
        #     print("----------")
        #     print(topic.id)
        #     # annex_obj_list.append(topic_annex_list)
        #
        # print("开题部分")
        # print(topic_obj_list, "长度：", len(topic_obj_list))
        # print(topic_annex_list, "长度：", len(topic_annex_list))
        # for annex in topic_obj_list:
        #     print(annex.title)
        # context = {
        #     'topic_result': topic_obj_list,
        #     'annex_result': topic_annex_list,
        # }

        topic2teacher_list = Topic2Teacher.objects.filter(teacher_id=user.id)
        # 通过教师查询到题目
        print(isinstance(topic2teacher_list, list))
        topic_list = list()
        for topic2teacher_obj in topic2teacher_list:
            topic_list.append(topic2teacher_obj.topic)
        print(topic_list)

        topic_annex_dict = dict()
        for topic_obj in topic_list:
            topic_annex_dict[topic_obj] = Annex.objects.filter(annex_phase_id=2, topic_id=topic_obj.id)
        print("####")
        # print(topic_annex_dict)

        topic = topic_annex_dict.keys()

        for annex in topic_annex_dict:
            # print(topic_annex_dict[annex].file)
            for temp in topic_annex_dict[annex]:
                print(temp.file)

        for key, value in topic_annex_dict.items():
            print("KEY", key.title)
            # print("Value", value[0].file)

        context = {
            # "topic_result": topic,
            "name": name,
            "role": role,
            "topic_annex_dict": topic_annex_dict
        }
        return render(request, 'open_topic/download_open_topic.html', context=context)
    else:
        pass

import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from rolepermissions.checkers import has_role
# Create your views here.
from apps.annex.forms import AnnexForm
from apps.annex.models import Annex
from apps.phase.models import UserPhase
from apps.topic_record.models import Topic2Student, Topic2Teacher
from apps.user.models import User
from utils.fdfs.storage import FDFSStorage
from django.conf import settings

@login_required
def upload_graduation_topic(request, student_id):
    user = request.user
    user_obj = User.objects.get(id=user.id)
    if request.method == "GET":
        context = {
            "student_id": student_id,
        }
        return render(request, "defense/upload_annex_and_request_defense.html", context)

    if request.method == "POST":
        form = AnnexForm(request.POST)
        file = request.FILES.get("file")
        temp_file = "%s/%s" % (settings.MEDIA_ROOT, file.name)
        with open(temp_file, 'wb') as upload_files:
            for chunk in file.chunks():
                upload_files.write(chunk)
        # 写入临时文件
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
                annex_obj = Annex.objects.create(file=remote_file_id, annex_phase_id=5, raw_name=form['raw_name'],
                                                 uploader=user,
                                                 detail="论文", topic=annex_topic)
                annex_obj.save()
                # 更改学生状态为已经上传论文并申请了答辩
                user_obj.user_phase_id = 10
                user_obj.save()
                print("##################")
                print("学生状态")
                print(user_obj.user_phase_id)
                print("##################")
            elif has_role(user_obj, ['teacher']):
                # topic2teacher_obj = Topic2Teacher.objects.get(teacher_id=user.id)
                # annex_topic = topic2teacher_obj.topic
                annex_obj = Annex.objects.create(file=remote_file_id, annex_phase_id=6, raw_name=form['raw_name'],
                                                 uploader=user,
                                                 detail="答辩文档", topic=None)


            else:
                return HttpResponse("你是个管理员吧？？？")
            # return redirect(reverse('topic:my_topic'))
            return render(request, "defense/upload_annex_and_request_defense.html", {"student_id": student_id})

@login_required
def download_graduation_topic(request):
    user = request.user
    user_obj = User.objects.get(id=user.id)

    if has_role(user_obj, ['student']):
        topic2student_obj = Topic2Student.objects.get(student_id=user_obj.id)
        topic_id = topic2student_obj.topic_id
        topic2teacher_obj = Topic2Teacher.objects.get(topic_id=topic_id)
        teacher_obj = topic2teacher_obj.teacher

        open_topic_template = Annex.objects.get(uploader=teacher_obj, annex_phase_id=6)
        print(open_topic_template)
        uploader_name = User.objects.get(id=open_topic_template.uploader_id).name

        context = {
            'uploader_name': uploader_name,
            'open_topic_template': open_topic_template
        }
        return render(request, 'open_topic/download_open_topic.html', context=context)

    elif has_role(user_obj, ['teacher']):
        # 教师下载的是当前题目下，所有学生的开题报告
        topic2teacher_list = Topic2Teacher.objects.filter(teacher_id=user.id)
        # 通过教师查询到题目
        print(isinstance(topic2teacher_list, list))
        topic_list = list()
        for topic2teacher_obj in topic2teacher_list:
            topic_list.append(topic2teacher_obj.topic)
        print(topic_list)

        topic_annex_dict = dict()
        for topic_obj in topic_list:
            topic_annex_dict[topic_obj] = Annex.objects.filter(annex_phase_id=5, topic_id=topic_obj.id)
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
            "topic_annex_dict": topic_annex_dict
        }
        return render(request, 'open_topic/download_open_topic.html', context=context)
    else:
        pass

@login_required
def waiting_for_confirm_defense(request):
    user = request.user
    user_obj = User.objects.get(id=user.id)
    if has_role(user_obj, ['teacher']):
        # 查找当前教师的学生的题目
        topic2teacher = Topic2Teacher.objects.filter(teacher_id=user_obj.id)
        topic_list = list()
        for t2t in topic2teacher:
            topic_list.append(t2t.topic_id)

        # print("Topic List:", topic_list)
        # print("-------------------------")
        topic2student_list = list()
        for i in range(len(topic_list)):
            topic2student_list.append(Topic2Student.objects.filter(topic_id=topic_list[i]))
        # print("Topic2Student List", topic2student_list)

        topic2student_list_clean = list()
        for j in range(len(topic2student_list)):
            if isinstance(topic2student_list[j], list):
                for item in topic2student_list[j]:
                    topic2student_list_clean.append(item)
            else:
                topic2student_list_clean.append(topic2student_list[j])

        # print("整理后的Topic2Student List", topic2student_list_clean)

        student_id_list = list()
        for t2s in topic2student_list_clean:
            for item in t2s:
                student_id_list.append(item.student_id)

        student_list = list()
        for student_id in student_id_list:
            student_list.append(User.objects.get(id=student_id))


        result_list = list()
        for student in student_list:
            if student.user_phase_id == 10:
                result_list.append(student)


        annex2student = dict()
        for student in result_list:
            # annex = get_object_or_404(Annex,)
            annex = Annex.objects.get(uploader=student, annex_phase_id=5)
            annex2student[student] = annex

        print(annex2student)
        context = {
            "result": annex2student,
        }

        # 展示所有确认状态为2的学生
        return render(request, "defense/waiting_for_confirm_defense.html", context=context)
    else:
        return HttpResponse("无访问权限")

@login_required
def confirm_defense(request, user_id):
    student_obj = User.objects.get(id=user_id)
    # 更改确认状态，教师确认
    student_obj.user_phase = UserPhase.objects.get(id=11)
    student_obj.save()
    return redirect(reverse('defense:waiting_for_confirm_defense'))

@login_required
def student_list(request):
    teacher = get_object_or_404(User, id=request.user.id)
    topic2teacher = Topic2Teacher.objects.filter(teacher=teacher)
    topic_list = list()
    for t2t in topic2teacher:
        topic_list.append(t2t.topic)

    print("topic_list")
    print(topic_list)

    topic2student_set = list()
    for topic in topic_list:
        topic2student = Topic2Student.objects.filter(topic=topic)
        if len(topic2student) != 0:
            topic2student_set.append(topic2student)
    print("student_set")
    print(topic2student_set)
    # topic_list_clean = list()
    # for topic_set in topic_list:
    #     for topic in topic_set:
    #         topic_list_clean.append(topic)
    # print("topic_list_clean")
    # print(topic_list_clean)
    context = {
        "result": topic2student_set,
    }
    return render(request, "defense/student_list.html", context=context)

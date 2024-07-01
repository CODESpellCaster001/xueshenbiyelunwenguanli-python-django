from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from rolepermissions.checkers import has_role

from apps.topic_record.models import TopicRecord, Topic2Student, Topic2Teacher
from apps.phase.models import UserPhase
from apps.user.models import User


# Create your views here.
@login_required
def choose_topic(request, topic_id):
    student = request.user
    topic = TopicRecord.objects.get(id=topic_id)
    topic2student = Topic2Student.objects.filter(topic=topic)
    print("Topic2Student")
    print(topic2student)


    Topic2Student.objects.create(student_id=student.id, topic_id=topic.id)
    student_object = User.objects.get(username=student.username)

    print("修改前用户阶段：", student_object.user_phase)

    # 修改学生状态
    student_object.user_phase_id = 2
    student_object.save()
    print("修改后用户阶段：", student_object.user_phase)

    # 修改题目人数
    if topic.chosen_num < topic.limit_num:
        topic.chosen_num += 1
        topic.save()
        return redirect(reverse("choose_topic:show_chosen_topic"))
    elif topic.chosen_num == topic.limit_num:
        topic.is_chosen = 1
        topic.save()
        return HttpResponse("该题目已达到限选人数")

@login_required
def show_chosen_topic(request):
    student = request.user
    # topic2student_object = Topic2Student.objects.filter(student_id=student.id).first()
    topic2student_object = get_object_or_404(Topic2Student, student_id=student.id)
    topic_object = TopicRecord.objects.get(id=topic2student_object.topic_id)
    student_object = User.objects.get(username=student.username)
    topic2teacher_object = Topic2Teacher.objects.get(topic_id=topic2student_object.topic_id)
    teacher_object = User.objects.get(id=topic2teacher_object.teacher_id)

    phase = UserPhase.objects.get(id=student_object.user_phase_id)

    context = {
        "title": topic_object.title,
        "limit_num": topic_object.limit_num,
        "user_status": phase.user_phase,
        "teacher": teacher_object.name,
        "topic_id": topic_object.id
    }
    return render(request, 'choose_topic/chosen_topic.html', context)

@login_required
def confirm_choose_topic(request, user_id):
    user = User.objects.get(id=request.user.id)
    student_obj = User.objects.get(id=user_id)
    # 更改确认状态，教师确认
    if has_role(user, ['teacher']):
        student_obj.user_phase = UserPhase.objects.get(id=3)
        student_obj.save()
    elif has_role(user, ['admin']):
        student_obj.user_phase = UserPhase.objects.get(id=4)
        student_obj.save()
    return redirect(reverse('choose_topic:show_waiting_for_confirm_choose_topic'))

@login_required
def show_waiting_for_confirm_choose_topic(request):
    # 确认当前教师
    teacher = request.user
    teacher_obj = User.objects.get(id=teacher.id)

    # 查找当前教师的学生的题目
    topic2teacher = Topic2Teacher.objects.filter(teacher_id=teacher_obj.id)
    topic_list = list()
    for t2t in topic2teacher:
        topic_list.append(t2t.topic_id)

    print("Topic List:", topic_list)
    print("-------------------------")
    topic2student_list = list()
    for i in range(len(topic_list)):
        topic2student_list.append(Topic2Student.objects.filter(topic_id=topic_list[i]))
    print("Topic2Student List", topic2student_list)

    topic2student_list_clean = list()
    for j in range(len(topic2student_list)):
        if isinstance(topic2student_list[j], list):
            for item in topic2student_list[j]:
                topic2student_list_clean.append(item)
        else:
            topic2student_list_clean.append(topic2student_list[j])

    print("整理后的Topic2Student List", topic2student_list_clean)

    student_id_list = list()
    for t2s in topic2student_list_clean:
        for item in t2s:
            student_id_list.append(item.student_id)

    student_list = list()
    for student_id in student_id_list:
        student_list.append(User.objects.get(id=student_id))

    print("--------------------")
    print("学生列表", student_list)
    print("GUANLIYUAN？")
    print(has_role(teacher_obj, ['admin']))
    print("老师？？")
    print(has_role(teacher_obj, ['teacher']))

    result_list = list()

    # if has_role(teacher_obj, ['admin']):
    #     print("glyglygly")
    #     student_phase_3_list = User.objects.filter(user_phase_id=3)

    if has_role(teacher_obj, ['teacher']):
        print("tttttt")
        for student in student_list:
            if student.user_phase_id == 2:
                result_list.append(student)

    student2topic_dict = dict()
    for student in result_list:
        topic = get_object_or_404(Topic2Student, student = student)
        student2topic_dict[student] = topic.topic.title

    print("DIXT")
    print(student2topic_dict)
    context = {
        "result": student2topic_dict,

        # "admin_result": student_phase_3_list
    }

    # 展示所有确认状态为2的学生
    return render(request, "choose_topic/waiting_for_confirm.html", context=context)
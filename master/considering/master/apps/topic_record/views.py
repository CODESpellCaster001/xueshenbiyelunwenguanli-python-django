from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from apps.topic_record.models import TopicRecord, Topic2Teacher, Topic2Student
from utils.common.get_name_role import get_name_role
from rolepermissions.checkers import has_role
from apps.topic_record.forms import TopicRecordForm


# topic/index
# 获取所有题目
@login_required
def all_topic(request):
    result = TopicRecord.objects.all()
    name = get_name_role(request)[0]
    role = get_name_role(request)[1]

    print(name, role)

    context = {
        'result': result,
        'name': name,
        'role': role,
    }
    return render(request, "topic_record/../../templates/topic_record/index.html", context=context)


# topic/my_topic
# 获取当前用户的题目[学生获取已选题目，教师获取已出题目]
@login_required
def my_topic(request):
    user = request.user
    topic_list = list()

    if has_role(user, ['student']):
        # 学生从Topic2Student查询已选题目
        result_list = Topic2Student.objects.filter(student=user)
        for item in result_list:
            topic = TopicRecord.objects.get(id=item.topic.id)
            topic_list.append(topic)
    elif has_role(user, ['teacher']):
        # 教师从Topic2Teacher查询已出题目
        result_list = Topic2Teacher.objects.filter(teacher=user)
        for item in result_list:
            topic = TopicRecord.objects.get(id=item.topic.id)
            topic_list.append(topic)
    context = {
        'result': topic_list,
        'name': get_name_role(request)[0],
        'role': get_name_role(request)[1],
    }
    return render(request, "topic_record/../../templates/topic_record/my_topic.html", context)

@login_required
def create_topic(request):
    user = request.user
    name = get_name_role(request)[0]
    role = get_name_role(request)[1]

    if request.method == 'POST':
        form = TopicRecordForm(request.POST)
        if form.is_valid():
            form.save()
        title = form.clean().get("title")
        print(title)
        print('-------')
        pops = form.clean().pop("title")
        print(pops)
        topic = TopicRecord.objects.filter(title=title)
        topic = topic[0]
        Topic2Teacher.objects.create(topic=topic, teacher=user)

        return redirect(reverse('topic:my_topic'))

    context = {
        'name': name,
        'role': role,
    }
    return render(request, "topic_record/../../templates/topic_record/create_topic.html", context)

@login_required
def delete_topic(request, topic_id):
    TopicRecord.objects.get(id=topic_id).delete()
    return redirect(reverse("topic:my_topic"))

@login_required
def edit_topic(request, topic_id):
    topic_obj = TopicRecord.objects.get(id=topic_id)
    if request.method == 'GET':
        title = topic_obj.title
        detail = topic_obj.detail
        context = {
            "topic_id": topic_id,
            "title": title,
            "detail": detail,
        }
        return render(request, "topic_record/../../templates/topic_record/edit_topic.html", context)
    else:
        form = TopicRecordForm(instance=topic_obj, data=request.POST)
        form.save()
        if form.is_valid():
            return render(request, "topic_record/../../templates/topic_record/edit_topic.html", {'topic_id': topic_id})

@login_required
def topic_detail(request, topic_id):
    if request.method == 'GET':
        topic = TopicRecord.objects.get(id=topic_id)
        title = topic.title
        chosen_num = topic.chosen_num
        limit_num = topic.limit_num
        release_time = topic.release_time
        last_edit_time = topic.last_edit_time
        detail = topic.detail

        topic2teacher = Topic2Teacher.objects.get(topic=topic)
        teacher_name = topic2teacher.teacher.name
        name = get_name_role(request)[0]
        role = get_name_role(request)[1]
        context = {
            "name": name,
            "role": role,
            "title": title,
            "teacher": teacher_name,
            "chosen_num": chosen_num,
            "limit_num": limit_num,
            "release_time": release_time,
            "last_edit_time": last_edit_time,
            "detail": detail
        }
        return render(request, "topic_record/../../templates/topic_record/topic_detail.html", context)

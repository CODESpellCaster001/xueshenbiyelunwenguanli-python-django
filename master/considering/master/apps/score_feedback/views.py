from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from rolepermissions.checkers import has_role

from apps.score_feedback.models import Feedback2Student, Feedback2Teacher
from apps.topic_record.models import Topic2Student, Topic2Teacher
from apps.user.models import User


@login_required
def get_score_set_feedback(request):
    user = request.user
    user_obj = User.objects.get(id=user.id)
    if has_role(user_obj, ['student']):
        topic2student = Topic2Student.objects.filter(student=user_obj)[0]
        # 当前学生的Topic
        topic_obj = topic2student.topic
        # 获取当前题目所有学生
        student_obj_list = Topic2Student.objects.filter(topic=topic_obj)
        print("###当前题目的学生列表", student_obj_list)

        # 获取当前题目的指导老师
        teacher_obj = Topic2Teacher.objects.get(topic=topic_obj)

        # 获取导师评价
        feedback2student = Feedback2Student.objects.get(student=user_obj)
        feedback = feedback2student.feedback
        for student in student_obj_list:
            print("学生成绩", student.student.score)
        context = {
            "student_id": user_obj.id,
            "student_obj_list": student_obj_list,
            "topic": topic_obj.title,
            "teacher": teacher_obj.teacher.name,
            "feedback": feedback
        }

        return render(request, "score_feedback/score_feedback.html", context=context)
    elif has_role(user_obj, ['teacher']):
        return HttpResponse("22")


@login_required
def waiting_for_score(request):
    # 通过当前教师用户查询题目
    teacher = User.objects.get(id=request.user.id)
    topic2teacher = Topic2Teacher.objects.filter(teacher=teacher)
    topic_list = list()
    for t2t in topic2teacher:
        topic_list.append(t2t.topic)
    # print("##当前教师题目列表")
    # print(topic_list)
    # 通过题目查询所有状态为已经答辩[待评分]的学生
    student_list = list()
    for topic in topic_list:
        # print(topic.title)
        print(topic.id)

        student_list.append(Topic2Student.objects.filter(topic_id=topic.id))
    # print("##题目-学生")
    # print(student_list)

    student_list_clean = list()
    for student in student_list:
        # if len(student):
        #     student_list.remove(student)
        if len(student) != 0:
            for item in student:
                if item.student.user_phase_id == 11:
                    student_list_clean.append(student)

    print("QQQQQ")
    print(student_list_clean)
    #
    # print("#######################3")
    for student in student_list_clean:
        for temp in student:
            print(temp.student.name)
    # 返回学生列表
    context = {
        "result": student_list_clean,
    }
    return render(request, "score_feedback/waiting_for_score.html", context=context)


@login_required
def set_score_set_feedback(request, student_id):
    user = User.objects.get(id=request.user.id)

    if request.method == "GET":
        topic2student = Topic2Student.objects.get(student_id=student_id)
        title = topic2student.topic.title
        student_name = topic2student.student.name
        detail = topic2student.topic.detail
        student_id = topic2student.student.id
        context = {
            "student_id": student_id,
            "title": title,
            "student_name": student_name,
            "detail": detail,
        }
        return render(request, "score_feedback/set_score_set_feedback.html", context=context)
    elif request.method == "POST":
        form = request.POST
        print(form)

        if has_role(user, ['teacher']):
            feedback2student = Feedback2Student.objects.create(student_id=student_id, feedback=form["feedback"])
            feedback2student.save()

            student = User.objects.get(id=student_id)
            student.score = form["score"]
            student.user_phase_id = 12
            student.save()
            return redirect(reverse("score_feedback:waiting_for_score"))

        elif has_role(user, ["student"]):
            print(form["feedback"])
            print("haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaajdsvkajbdskvjbadsk")
            topic2student = Topic2Student.objects.get(student_id=user.id)
            topic = topic2student.topic
            topic2teacher = Topic2Teacher.objects.get(topic=topic)
            teacher = topic2teacher.teacher
            feedback2teacher = Feedback2Teacher.objects.create(teacher=teacher, feedback=form["feedback"])
            feedback2teacher.save()
            print(feedback2teacher.feedback)
            return redirect(reverse("topic:all_topic"))


@login_required
def my_feedback(request):
    user = User.objects.get(id=request.user.id)
    # 获取教师得到的评价
    feedback2teacher = Feedback2Teacher.objects.filter(teacher=user)
    feedback_list = list()
    for f2t in feedback2teacher:
        feedback_list.append(f2t.feedback)

    for feedback in feedback_list:
        print("!!!!!!!!!")
        print(feedback)
    context = {
        "result_list": feedback_list,
    }
    return render(request, "score_feedback/my_feedback.html", context=context)

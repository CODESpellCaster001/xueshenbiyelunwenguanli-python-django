from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from apps.user.models import User
from django.contrib.auth import authenticate, login, logout
from rolepermissions.roles import assign_role


# /register/
class RegisterView(View):
    @staticmethod
    def get(request):
        # 显示注册页面
        return render(request, 'register.html')

    @staticmethod
    def post(request):
        name = request.POST.get('registerName', None)
        username = request.POST.get('registerUsername', None)
        password = request.POST.get('registerPassword', None)
        school = request.POST.get('registerSchool', None)
        department = request.POST.get('registerDepartment', None)
        email = request.POST.get('registerEmail', None)

        if not all([username, password]):
            print("数据不完整")

        user = User.objects.create_user(
            name=name,
            username=username,
            password=password,
            school=school,
            department=department,
            email=email
        )
        user.save()

        # 默认角色为学生
        assign_role(user, 'student')
        return redirect(reverse('login'))


# /login/
class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, 'login.html')

    @staticmethod
    def post(request):
        username = request.POST.get('userName', None)
        password = request.POST.get('passWord', None)
        print(username)
        print(password)

        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', reverse('topic:all_topic'))
            response = redirect(next_url)
            return response
        else:
            return render(request, 'login.html')


class LogoutView(View):
    '''退出登录'''

    def get(self, request):
        '''退出登录'''
        # 清除用户session信息
        logout(request)
        # 跳转到首页
        return redirect(reverse('login'))


def user_center(request):
    user = User.objects.get(id=request.user.id)
    context = {
        "name": user.name,
        "school": user.school,
        "department": user.department,
        "memo": user.memo,
        "email": user.email
    }
    return render(request, "user/user_center.html", context=context)


def edit_user_profile(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "GET":
        department = user.department
        email = user.email
        memo = user.memo
        context = {
            "department": department,
            "email": email,
            "memo": memo,
        }
        return render(request, "user/edit_user_profile.html", context=context)
    else:
        print("!!!")
        form = request.POST
        print(form)
        user.department = form['department']
        user.email = form['email']
        user.memo = form['memo']
        user.save()
        return render(request, "user/edit_user_profile.html")


def change_pwd(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == "GET":
        return render(request, "user/change_pwd.html")
    else:
        form = request.POST
        print(form)
        pwd = form['registerPassword']
        pwd_confirm = form['registerPasswords']
        if pwd == pwd_confirm:
            print(pwd)
            user.set_password(pwd)
            user.save()
            return redirect(reverse("login"))
        else:
            return redirect(reverse("topic:all_topic"))


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def page_error(request):
    return render(request, '500.html', status=500)

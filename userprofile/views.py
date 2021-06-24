from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import UserLoginForm


# Create your views here.
# def index(request):
#     return render(request, 'userprofile/index.html')


def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)

        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)  # 实现用户登录，将用户数据保存在session中
                return redirect("blog:index")
            else:
                return HttpResponse("账号或密码输入有误!请重新输入!")
        else:
            return HttpResponse("账号或密码输入不合法!")
    elif request.method == "GET":
        user_login_form = UserLoginForm()
        return render(request, "userprofile/login.html", context={'form': user_login_form})
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_logout(request):
    logout(request)
    return redirect("blog:index")

"""untitled1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse,render,redirect
# def login(request):#函数用于
#     """
#     处理用户请求并返回结果
#     :param request: 用户请求相关的所有信息（对象）--django已经写成了对象
#     :return:b'login'在django里更改了规则所以不可以，要改变方法,yongHttpResponse
#     """
#     #return HttpResponse(login.html)这个是错误的，这里只放字符串，应用render
#     print(request.method)
#     if request.method == "GET":
#         return render(request,'login.html')#只需写文件名即可，在配置里已经设定了它在templates中，如果templates改名，也应该到setting中改名--这个有时能自动更改
#     else:
#         #用户POST提交的数据
#         print(request.POST)
#         print("POST");
#         user = request.POST.get('user')
#         pwd=request.POST.get('pwd')
#         if user=='root' and pwd=='123123':
#             #登陆成功
#             return redirect('/index')#可以写相对路径
#         else:
#             #登录失败
#             return render(request, 'login.html',{'msg':'用户名或密码错误'})


from app import index,user,good

urlpatterns = [
    path('admin/', admin.site.urls),

    # 模板
    path('start/',index.start),
    path('layout/',index.layout),
    path('good/',index.good),
    path('user/',index.user),

#     首页



#     商品
    path('collect/',good.collect),
    #首页商品列表
    path('index/',good.index),
    path('goodlist/',good.goodlist),
    path('good_detail/',good.good_detail),

#     user
    #商品书藏页
    path('user_collectlist/',user.user_collectlist),
    # 个人信息
    path('user_personal/', user.user_personal),
    path('update_user/', user.update_user),
    path('update_img/', user.update_img),
    #用户登录注册逻辑
    path('login/', user.login),
    path('logout/', user.logout),
    path('register/', user.register),

]

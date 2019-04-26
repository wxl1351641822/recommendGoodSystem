from app import sql,good
from django.shortcuts import HttpResponse,render,redirect
import traceback
import json
import time
# user-collect
def user_collectlist(request):
    # 先去cookie中找凭证
    id = request.COOKIES.get('userid')
    print(id)
    login_flag = id;
    if (not id):
        login_flag = 0;
        return redirect('/index/')
    login_flag=int(login_flag)

    page = request.GET.get('page')
    print(page)

    if not page:
        page = 1;
        sqlstr = "select count(*) from collect where userid=%d"%(login_flag)
        count = sql.select(sqlstr)
        if (count['error'] == 0):
            count = count['data'][0]['count(*)']
        else:
            count = 0;
        max_page = int(count / 16) + 1
    else:
        page = int(page)
        max_page = request.GET.get('max_page')
        max_page = int(max_page)

    start = page - 5
    end = page + 5
    if (start <= 0):
        start = 1;
        end = 10;
    if (end > max_page):
        end = max_page;
        if (end - 9 > 0):
            start = end - 9;




    # 找不到再显示
    sqlstr = "select * from goodlist,collect where goodlist.id=collect.goodid and collect.userid='%d' order by collect_num desc limit %d,16" % (
    login_flag, (page-1)*16)
    message = sql.select(sqlstr)
    # print(message)
    if (message['error'] == 0):
        goodlist = message['data']
    else:
        goodlist = []
    for good0 in goodlist:
        good.good_tag(good0)
    print(start, end)
    count_lis = list(range(start, end + 1))
    print('/collect/')
    print(count_lis)
    return render(request, 'user/collect.html',
                  {'error': 0, 'goodlist': goodlist, 'login_flag': login_flag, 'count_lis': count_lis, 'page': page,
                   'max_page': max_page,'goto':'/user_collectlist/?'})
    #
    # return render(request, 'user/collect.html')


# login-登录
def login(request):
    re={'error': 0, 'data': ()}
    try:
        # print(request)
        print(request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        sqlstr = ("select id,name,password from user where name='%s';" % username)
        # print(sqlstr)
        user=sql.select(sqlstr);
        print(user)
        re=user
        response = HttpResponse(json.dumps(re))
        if(re['error']==0):
            if(len(user['data'])==0):
                re['error'] = 1
                re['data'] = '用户名错误'
                response = HttpResponse(json.dumps(re))
            elif(user['data'][0]['password']!=pwd):
                re['error']=1
                re['data']='密码错误'
                response = HttpResponse(json.dumps(re))
            else:#登陆成功
                response.set_cookie('userid',re['data'][0]['id'])

    except Exception as e:
        re['error']=1
        re['data']='后台错误'
        response = HttpResponse(json.dumps(re))
        print(e)
        traceback.print_exc()
    return response
# 注册
def register(request):
    re={'error': 0, 'data': ()}
    try:
        # print(request)
        print(request.POST)
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        sqlstr = ("select id,name,password from user where name='%s';" % username)
        # print(sqlstr)
        user=sql.select(sqlstr);

        re=user
        response=HttpResponse(json.dumps(re))
        if(re['error']==0):
            if(len(user['data'])==0):
                sqlstr="insert into user(name,password) values('%s','%s')"%(username,pwd)
                re=sql.insert(sqlstr)
                response = HttpResponse(json.dumps(re))
                if(re['error']==0):
                    sqlstr = ("select id,name,password from user where name='%s';" % username)
                    # print(sqlstr)
                    re = sql.select(sqlstr);
                    # obj.set_cookie()
                    response.set_cookie('userid', re['data'][0]['id'])
            else:
                re['error']=1
                re['data']='该用户名已存在'
                response = HttpResponse(json.dumps(re))
    except Exception as e:
        re['error']=1
        re['data']='后台错误'
        print(e)
        traceback.print_exc()
        response = HttpResponse(json.dumps(re))

    return HttpResponse(json.dumps(re))

def logout(request):
    response = HttpResponse('ok')
    response.delete_cookie('userid')
    return response

# 个人信息
def user_personal(request):
    id = request.COOKIES.get('userid')
    if(id):
        print(id)
        id=int(id)

        sqlstr="select * from user where id='%d'"%(id)
        user=sql.selectone(sqlstr)
        print(user)
        user=user['data']

        return render(request,'user/personal.html',{'user':user})
    else:
        return redirect('/index/')

def update_user(request):
    id = request.COOKIES.get('userid')
    if (id):
        print(id)
        id = int(id)
        print('POST',request.POST)
        name=request.POST.get('name')
        password=request.POST.get('password')
        phone = request.POST.get('phone')
        addr = request.POST.get('addr')
        date = request.POST.get('date')
        sex = request.POST.get('sex')
        sqlstr = "UPDATE `user` SET `name`='%s',`addr`='%s',`sex`='%s',`age`='%s',`password`='%s',`phone`='%s' WHERE id='%d'" % (name,addr,sex,date,password,phone,id)
        kk = sql.update(sqlstr)
        print(kk)
        return HttpResponse(kk)
    else:
        redirect('/index/')


def update_img(request):
    data=''
    try:
        id = request.COOKIES.get('userid')
        if (id):
            print(id)
            id = int(id)
            print('POST_img',request.POST)
            print('POST_img1',request.FILES)
            print('PO',request.FILES['upload.jpg'].name)
            filename=request.FILES['upload.jpg'].name
            # 在项目目录下新建一个文件
            filename1="./static/img/user/"+filename
            with open(filename1, "wb") as f:
                # 从上传的文件对象中一点一点读
                for chunk in request.FILES["upload.jpg"].chunks():
                    # 写入本地文件
                    f.write(chunk)
            filename="/static/img/user/"+filename
            sqlstr="UPDATE `user` SET `avatarurl`='%s' WHERE id='%d'"%(filename,id)
            kk=sql.update(sqlstr)
            if(kk['error']==0):

                data='ok'
            else:
                data='数据库错误'
        else:
            return redirect('/index/')
    except Exception as e:
        print(e)
        traceback.print_exc()
        data = '文件错误'
    print(data)

    return HttpResponse(data)

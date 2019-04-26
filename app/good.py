from app import sql
from django.shortcuts import HttpResponse,render,redirect
import traceback
import json
import time
from app import tag_recommend

# 收藏商品
def collect(request):
    re = {'error': 0, 'data': ()}
    try:
        # 先去cookie中找凭证
        id = request.COOKIES.get('userid')
        goto = request.GET.get('goto')
        page = request.GET.get('page')
        max_page = request.GET.get('max_page')
        print(id)

        if not id:
            re={'error':1,'data':'1请登录！'}
            response = HttpResponse(json.dumps(re))
            goto='/index/?'
        else:
            flag = request.GET.get('del')
            goodid = request.GET.get('goodid')
            if (flag == '0'):

                if not goodid:
                    re = {'error': 1, 'data': '2收藏失败_goodid'}
                    response = HttpResponse(json.dumps(re))
                else:
                    date=time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    # print('当前日期'+date)
                    sqlstr="insert into collect(userid,goodid,date) values('%d','%s','%s')"%(int(id),goodid,date)
                    re=sql.insert(sqlstr)
                    response = HttpResponse(json.dumps(re))
                    # response.set_cookie(goodid+'-'+id,'1')
            else:
                if not goodid:
                    re = {'error': 1, 'data': '2删除收藏失败_goodid'}
                    response = HttpResponse(json.dumps(re))
                else:
                    sqlstr="delete from collect where userid='%d' and goodid='%s'"%(int(id),goodid)
                    re=sql.delete(sqlstr)
                # 决定刷新到哪里
        if not goto:
            goto = '/index/?'
        if max_page:
            if not page:
                goto = goto + 'page=1&max_page=' + max_page
            else:
                goto = goto + 'page=' + page+'&max_page='+max_page

        print(goto,page,max_page)

        if goto=='good_detail':
            goto="http://127.0.0.1:8000/good_detail/?goodid=%s"%(goodid)

    except Exception as e:
        re['error']=1
        re['data']='3后台错误'
        response = HttpResponse(json.dumps(re))
        print(e)
        traceback.print_exc()
    print(re)
    return redirect(goto)

def freq(request):
    # 先去cookie中找凭证
    id = request.COOKIES.get('userid')
    # print(id)
    login_flag = id;
    page = request.GET.get('page')
    # print(page)
    keyword = request.GET.get('keyword')
    tag=request.GET.get('tag')
    max_page = request.GET.get('max_page')

    goodlist, login_flag, count_lis, page, max_page = get_goodlist(id, login_flag, keyword, page, max_page, 1,tag)
    goto = '/freq/?'
    if keyword:
        goto = goto + 'keyword=' + keyword+'&'
    if tag:
        goto = goto + 'tag=' + tag+'&'
    return render(request, 'good/index.html',
                  {'error': 0, 'goodlist': goodlist, 'login_flag': login_flag, 'count_lis': count_lis, 'page': page,
                   'max_page': max_page, 'goto': goto,'key':1,'freq_tag':tag_recommend.get_freqtag()})

def sim_user(request):
    # 先去cookie中找凭证
    id = request.COOKIES.get('userid')
    # print(id)
    login_flag = id;
    page = request.GET.get('page')
    # print(page)
    keyword = request.GET.get('keyword')
    tag = request.GET.get('tag')
    max_page = request.GET.get('max_page')

    goodlist, login_flag, count_lis, page, max_page = get_goodlist(id, login_flag, keyword, page, max_page, 2,tag)
    goto='/sim_user/?'
    if keyword:
        goto=goto+'keyword='+keyword+'&'
    if tag:
        goto = goto+'tag=' + tag+'&'
    return render(request, 'good/index.html',
                  {'error': 0, 'goodlist': goodlist, 'login_flag': login_flag, 'count_lis': count_lis, 'page': page,
                   'max_page': max_page, 'goto': goto, 'key': 2,'freq_tag':tag_recommend.get_freqtag()})


def index(request):#函数用于
    #先去cookie中找凭证
    id=request.COOKIES.get('userid')
    # print(id)
    login_flag = id;
    page = request.GET.get('page')
    # print(page)
    keyword=request.GET.get('keyword')

    max_page = request.GET.get('max_page')
    tag = request.GET.get('tag')
    goodlist,login_flag,count_lis,page,max_page=get_goodlist(id,login_flag,keyword,page,max_page,0,tag)
    goto='/index/?'
    if keyword:
        goto=goto+'keyword='+keyword+'&'
    if tag:
        goto = goto+'tag=' + tag+'&'
    return render(request, 'good/index.html',{'error':0,'goodlist':goodlist,'login_flag':login_flag,'count_lis':count_lis,'page':page,'max_page':max_page,'goto':goto,'key':0,'freq_tag':tag_recommend.get_freqtag()})

def good_detail(request):
    goodid=request.GET.get('goodid')
    id = request.COOKIES.get('userid')
    # print(id)
    login_flag = id;
    if (not id):
        login_flag = 0;
    else:
        login_flag = int(id)
        try:
            sqlstr="select * from collect where goodid='%s' and userid='%d'"%(goodid,login_flag)
            collect=sql.select(sqlstr)
            if len(collect['data'])<=0:
                login_flag=-1;

        except Exception as e:
            print(e)
            traceback.print_exc()
    if not goodid:
        return render(request, 'good/index.html')
    else:
        try:
            # print(goodid)
            # sqlstr="select * from goodlist where goodlist.id='%s'"%(goodid)
            # goodlist=sql.select(sqlstr)
            # print(goodlist)
            sqlstr="select * from sim_good_recommend_list,goodlist where goodlist.id=goodid2 and goodid1='%s' order by sum desc limit 0,16"%(goodid)
            goodlist=sql.select(sqlstr)
            for good in goodlist['data']:
                good_tag(good)
            # print("goodlist0",goodlist0)
            # if(goodlist0['error']==0):
            #     if(goodlist['error']!=0):
            #         goodlist=goodlist0
                # else:
                #     goodlist['data']=goodlist0['data']+goodlist['data']


            sqlstr = "select * from gooddetaillist where gooddetaillist.id='%s'" % (goodid)
            good_detail = sql.select(sqlstr)
            print(good_detail)
            sqlstr = "select goodcomments.id,name,avatarurl,comments,name from goodcomments,user where goodcomments.goodid='%s' and user.id=goodcomments.userid" % (goodid)
            good_comments = sql.select(sqlstr)
            print(good_comments)
        except Exception as e:
            print(e)
            traceback.print_exc()
        qq=render(request,'good/good_detail.html',{'goodlist':goodlist['data'],'good_detail':good_detail['data'],'good_comments':good_comments['data'],'login_flag':login_flag})
        # str=qq.serialize()
        #
        #
        # str.replace('<b/>','')
        # str.replace('<i class="sprite-size"/>','')
        with open("./11.html",'wb') as f:
            f.write(qq.content)
        str=qq.content.decode('utf-8')
        str=str.replace('<b/>','')
        str = str.replace('<i ', '<text')
        str = str.replace('i>', 'text>')

        return HttpResponse(str)

def get_goodlist(id,login_flag,keyword,page,max_page,key,tag):
    if not page:
        page=1;
        if not keyword:
            sqlstr = "select count(*) from goodlist"
        else:
            sqlstr="select count(*) from goodlist where keyword='%s'"%(keyword)
        count = sql.select(sqlstr)
        if (count['error'] == 0):
            count = count['data'][0]['count(*)']
        else:
            count = 0;
        max_page = int((count-1) / 16) + 1

    page = int(page)
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
    print(start, end)
    count_lis = list(range(start, end + 1))
    print(count_lis)

    if((not id) or key==1):
        if(key==0):
            login_flag=0;
        if(not keyword):
            sqlstr = "select * from goodlist order by collect_num desc limit %d,16"%((page-1)*16)
        else:
            sqlstr = "select * from goodlist where keyword='%s' order by collect_num desc limit %d,16" % (
            keyword, (page - 1) * 16)
        message = sql.select(sqlstr)
    else:
        login_flag=int(id)
        if(not keyword):
            keyword=0
        if(key==2):
            message=tag_recommend.sim_user_good_recommend(login_flag,page,keyword)
        else:
             message = tag_recommend.Recommend_db(login_flag, page, keyword)
        if not page:
            max_page=message['max_page']
    #找不到再显示
        # sqlstr="select * from goodlist left join collect on goodlist.id=collect.goodid and collect.userid='%d' order by collect_num desc limit %d,16"%(login_flag,(page-1)*16)
    # print(sqlstr)

    print(message)
    if(message['error']==0):
        goodlist=message['data']
        for good in goodlist:
            # print(good)
            if(good['img_url'].find("http")<0):
                good['img_url']="/static/img/shoucang.png"
    else:
        goodlist=[]
    for good in goodlist:
        good_tag(good)
    return goodlist,login_flag,count_lis,page,max_page


def good_tag(good):
    sqlstr = "select goodid,tag from recommend_good_tag_count where goodid='%s' and tag not in (select keyword from goodlist where recommend_good_tag_count.goodid=goodlist.id) order by tag desc limit 0,3" % (
    good['id'])
    taglist = sql.select(sqlstr)
    if (len(taglist['data']) >= 3):
        good.update(
            {'tag1': taglist['data'][0]['tag'], 'tag2': taglist['data'][1]['tag'], 'tag3': taglist['data'][2]['tag']})
    elif ((len(taglist['data']) == 2)):
        good.update({'tag1': taglist['data'][0]['tag'], 'tag2': taglist['data'][1]['tag'], 'tag3': "没有标签"})
    elif ((len(taglist['data']) == 1)):
        good.update({'tag1': taglist['data'][0]['tag'], 'tag2': "没有标签", 'tag3': "没有标签"})
    else:
        good.update({'tag1': "没有标签", 'tag2': "没有标签", 'tag3': "没有标签"})




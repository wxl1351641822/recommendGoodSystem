from app import sql
import traceback
def Recommend_db(userid,page,keyword):
    recommend_list={'error':0,'data':[],'max_page':1}
    count={'error':1,'data':0}
    try:
        if(keyword==0):
            if (page == 1):
                sqlstr = "select count(*) from goodlist  left join recommend_list on goodlist.id=recommend_list.goodid left join collect on goodlist.id=collect.goodid and collect.userid='%d' where recommend_list.userid='%d' order by recommend_list.sum desc" % (
                    userid,userid)
                count = sql.select(sqlstr)
            sqlstr="select goodlist.id,title,url,img_url,price,keyword,page,collect_num,comment_num,click_num,collect.userid userid from goodlist  left join recommend_list on goodlist.id=recommend_list.goodid left join collect on goodlist.id=collect.goodid and collect.userid='%d' where recommend_list.userid='%d' order by recommend_list.sum desc limit %d,16"%(userid,userid,(page-1)*16)

        else:
            if (page == 1):
                sqlstr = "select count(*) from goodlist  left join recommend_list on goodlist.id=recommend_list.goodid left join collect on goodlist.id=collect.goodid and collect.userid='%d' where recommend_list.userid='%d' and keyword='%s' order by recommend_list.sum desc" % (
                    userid,userid,keyword)
                count = sql.select(sqlstr)
            sqlstr = "select goodlist.id,title,url,img_url,price,keyword,page,collect_num,comment_num,click_num,collect.userid userid from goodlist  left join recommend_list on goodlist.id=recommend_list.goodid left join collect on goodlist.id=collect.goodid and collect.userid='%d' where recommend_list.userid='%d' and keyword='%s' order by recommend_list.sum desc limit %d,16" % (
            userid,userid, keyword,(page - 1) * 16)


        list = sql.select(sqlstr)


        recommend_list['error']=list['error']
        recommend_list['data'] = list['data']
        if (count['error'] == 0):
            count = count['data'][0]['count(*)']
        else:
            count = 0;
        recommend_list['max_page'] = int((count-1)/16)+1
        print(recommend_list['max_page'])
    except Exception as e:
        traceback.print_exc()
    # print(recommend_list)
    return recommend_list

def get_freqtag():
    sqlstr="select * from tagfreq order by count desc limit 0,100"
    freqtag_list=sql.select(sqlstr)
    print(freqtag_list)
    return freqtag_list['data']

def tag_CosineSim(tag):
    sqlstr="select * from cos where tag1='%s' order by cosine desc"%(tag)
    sim_list=sql.select(sqlstr)
    print(sim_list)
    return sim_list
# Recommend_db(20,1)
# get_freqtag()
# tag_CosineSim("上身效果佳")

def sim_user_good_recommend(login_flag,page,keyword):
    recommend_list = {'error': 0, 'data': [], 'max_page': 1}

    try:
        sqlstr="select userid2,sum from sim_user_recommend_list where userid1='%d'"%(login_flag)
        user_list=sql.select(sqlstr)
        recommend_list['max_page'] = len(user_list['data'])
        # print(user_list)
        if(page<recommend_list['max_page']):
            list=Recommend_db(user_list['data'][page]['userid2'] , 1 , keyword)
        # print(list)
        #
    except Exception as e:
        traceback.print_exc()

    recommend_list['data']=list['data']
    # print(user_list)
    return recommend_list

def get_goodlist_by_freqtag(page,tag):
    recommend_list = {'error': 0, 'data': [], 'max_page': 1}
    count = {'error': 1, 'data': 0}
    try:
        if(page==1):
            sqlstr="select count(*) from recommend_good_tag_count where tag='%s' order by count desc"
            count=sql.select(sqlstr)
        if (count['error'] == 0):
            count = count['data'][0]['count(*)']
        else:
            count = 0;


        sqlstr="select goodlist.* from recommend_good_tag_count,goodlist where goodlist.id=recommend_good_tag_count.goodid and tag='%s' order by count desc limit %d,16)"%(tag,(page-1)*16)
        list=sql.select(sqlstr)
    except Exception as e:
        traceback.print_exc()
    recommend_list['data']=list['data']
    recommend_list['max_page'] = int((count - 1) / 16) + 1
    return recommend_list

def recommend_tag_good(tag_list,page,keyword):
    k=0;
    recommend_list = {'error': 0, 'data': [], 'max_page': 1}
    count = {'error': 1, 'data': 0}
    tagstr=''

    for tag in tag_list:
        k=1
        tagstr=tagstr+" tag='"+tag+"' or"
    print(tagstr[0:-3])
    page=int(page)

    if(k==1):
        try:
            if (keyword == 0):
                if (page == 1):
                    sqlstr = "select count(*) from recommend_good_tag_count where " + tagstr[0:-3] + " group by goodid ORDER BY sum(count/log(count+1)) desc"
                    count = sql.select(sqlstr)
                    print('count1', count)
                sqlstr = "select goodlist.* from recommend_good_tag_count,goodlist where goodlist.id=recommend_good_tag_count.goodid and (" + tagstr[0:-3] + ") group by goodid ORDER BY sum(count/log(count+1)) desc limit %d,16" % ((page-1)*16)
            else:
                if (page == 1):
                        sqlstr = "select count(*) from recommend_good_tag_count,goodlist where goodlist.id=recommend_good_tag_count.goodid and (" + tagstr[0:-3] + ") and keyword='%s' group by goodid ORDER BY sum(count/log(count+1)) desc"%(keyword)
                        count = sql.select(sqlstr)
                        print('count2', count)
                sqlstr = "select goodlist.* from recommend_good_tag_count,goodlist where goodlist.id=recommend_good_tag_count.goodid and (" + tagstr[0:-3] + ") and keyword='%s' group by goodid ORDER BY sum(count/log(count+1)) desc limit %d,16" % (
                                         keyword,(page - 1) * 16)

            list = sql.select(sqlstr)

            recommend_list['error'] = list['error']
            recommend_list['data'] = list['data']
            print('count',count)
            if (count['error'] == 0):
                count = count['data'][0]['count(*)']
            else:
                count = 0;
            recommend_list['max_page'] = int((count - 1) / 16) + 1
            print(recommend_list['max_page'])
        except Exception as e:
            traceback.print_exc()
        # print(recommend_list)
    return recommend_list
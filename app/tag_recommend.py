from app import sql
import traceback
def Recommend_db(userid,page,keyword):
    recommend_list={'error':0,'data':[],'max_page':1}
    count={'error':0,'data':0}
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
        recommend_list['max_page'] = int(count/16)+1
        print(recommend_list['max_page'])
    except Exception as e:
        traceback.print_exc()
    # print(recommend_list)
    return recommend_list

def get_freqtag():
    sqlstr="select * from tagfreq order by count desc"
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
from app import sql
import random
import traceback
sqlstr="select * from goodtag";
taglists=sql.select(sqlstr)
for taglist in taglists['data']:
    print(taglist)
    taglist_spilt=taglist['taglist'].split(')')
    print(taglist_spilt)
    sqlstr = "select userid from goodcomments where goodid='%s'" % (taglist['id'])
    s = sql.select(sqlstr)
    print(s)
    for tag in taglist_spilt:
        try:
            print(tag)
            tag0=tag.split('(')
            print(tag0)
            tag=tag0[0]
            num=tag0[1]
            for i in range(0,int(num)):
                userid=random.choice(s['data'])
                userid=int(userid['userid'])
                print(userid)
                sqlstr="insert into recommend_tag(goodid,userid,tag) values('%s','%d','%s')"%(taglist['id'],userid,tag)
                sql.insert(sqlstr)
        except Exception as e:
            print(e.__traceback__)
            traceback.print_exc()
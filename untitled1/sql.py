import pymysql

conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='',db='t1')

cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
print('root')
#effect_row=cursor.execute("select id,name from table")
#user_list=cursor.fechall()
sqlstr="""
        insert
        into user(id,name,email)
        values(2,'alex2','1235@qq.com')
"""
cursor.execute(sqlstr)
#user_list=cursor.fetchall()

conn.commit()
cursor.close()
conn.close()
#print(user_list)
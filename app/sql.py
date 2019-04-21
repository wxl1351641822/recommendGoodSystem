import pymysql
import traceback

def select(sqlstr):
    message = {'error': 0,
               'data': -1}
    try:
        conn = pymysql.connect(host='123.206.33.15', port=3306, user='username', passwd='password', db='jd',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sqlstr)
        list = cursor.fetchall()
        # conn.commit()
        cursor.close()
        conn.close()
        message['data'] = list
    except Exception as e:
        print(e)
        traceback.print_exc()
        print('查询数据有问题')
        message['error'] = 1
        message['data'] = '查询数据有问题'
    finally:
        return message


def selectone(sqlstr):
    message={'error':0,
             'data':-1}
    try:
        conn = pymysql.connect(host='123.206.33.15', port=3306, user='username', passwd='password', db='jd',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sqlstr)
        one = cursor.fetchone()
        # conn.commit()
        cursor.close()
        conn.close()
        message['data']=one
    except Exception as e:
        print(e)
        traceback.print_exc()
        print('插入数据有问题')
        message['error']=1
        message['data']=e
    finally:
        return message


def insert(sqlstr):
    message = {'error': 0,
               'data': -1}
    try:
        conn = pymysql.connect(host='123.206.33.15', port=3306, user='username', passwd='password', db='jd',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sqlstr)
        conn.commit()
        cursor.close()
        conn.close()
        message['data'] = '插入成功：'+sqlstr
    except Exception as e:
        print(e)
        traceback.print_exc()
        print('插入数据有问题'+sqlstr)
        message['error'] = 1
        message['data'] = '该用户名已存在'
    finally:
        return message


def delete(sqlstr):

    message = {'error': 0,
               'data': -1}
    try:
        conn = pymysql.connect(host='123.206.33.15', port=3306, user='username', passwd='password', db='jd',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sqlstr)
        # cursor.execute("insert into class(cname) values(%s);", [v,])
        # class_list = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        message['data'] = '删除成功！'
    except Exception as e:
        print(e)
        traceback.print_exc()
        print('删除数据有问题'+sqlstr)
        message['error'] = 1
        message['data'] = '删除数据有问题'+sqlstr
    finally:
        return message

def update(sqlstr):
    message = {'error': 0,
               'data': -1}
    try:
        conn = pymysql.connect(host='123.206.33.15', port=3306, user='username', passwd='password', db='jd',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sqlstr)
        # cursor.execute("insert into class(cname) values(%s);", [v,])
        # class0 = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        message['data'] = '更新成功：'+sqlstr
    except Exception as e:
        print(e)
        traceback.print_exc()
        print('插入数据有问题')
        message['error'] = 1
        message['data'] = e
    finally:
        return message

if __name__=='__main__':
    sqlstr = "select * from goodlist order by collect_num desc limit 15"
    print(select(sqlstr))
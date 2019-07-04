# -*- coding: utf-8 -*-

"""
WFACatPro.fixed
~~~~~~~~~~~~~~~~~~~
This is a fixed module.
"""


import pymysql

import settings


# 判断表是否存在
def table_exists(cur_param, table_name_param):
    sql = "show tables;"
    cur_param.execute(sql)
    tables = str(cur_param.fetchall())
    if table_name_param in tables:
        return True       #存在返回1
    else:
        return False      #不存在返回0


if __name__ == '__main__':
    DB_NAME = input("Enter database name that your created to fixed bug ：p")
    print("fixing !")
    db = pymysql.connect(
        host=settings.DB_HOST,
        port=int(settings.DB_PORT),
        user=settings.DB_USER,
        passwd=settings.DB_USER_PASSWORD,
        charset=settings.DB_CHARSET,
        db=DB_NAME)

    cur = db.cursor()

    """
    debug
    某个一度好友可能认识的另外一度好友原理：
    其中用他们的圈内二度好友列表（对研究对象来说的）取交集，
    交集部分连接的两个节点，一个节点是主节点，另一个节点是可能认识的另外的一度好友（对研究对象来说的），

    bug 原因：交集部分连接的两个节点，这两个节点不一定只通过交集部分连接，他们两个自己也可能能直接连接。
    解决：删掉可能认识的一度好友中已经互关的一度人脉。删掉 uxxxxxx 表中 uid 存在于他的 connect_to_my_friends 中的
    """
    # 遍历研究对象一度人脉
    cur.execute("SELECT uid, connect_to_my_friends FROM %s.peopleinfo WHERE rel_me = \'1\' " % (DB_NAME))
    result = cur.fetchall()

    for row in result:
        connect_to_my_friends_str = str(row[1])
        table_name = str(row[0])

        if table_exists(cur, table_name):
            cur.execute("SELECT uid FROM %s.u%s" % (DB_NAME, str(row[0])))
            u_table_result = cur.fetchall()
            for u_table_row in u_table_result:
                # 删掉 uxxxxx 表（可能认识的人表）中 uid 存在于他（peopleinfo 表）的 connect_to_my_friends 中的条目
                if str(u_table_row[0]) in connect_to_my_friends_str:
                    cur.execute("DELETE FROM %s.u%s WHERE uid = \'%s\'" % (DB_NAME, str(row[0]), str(u_table_row[0])))
                    db.commit()

    print("completed !")
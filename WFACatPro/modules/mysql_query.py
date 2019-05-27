# -*- coding: utf-8 -*-

"""
WFACatPro.mysql_query
~~~~~~~~~~~~~~~~~~~
This is a mysql query module.
"""


import traceback

import pymysql

import settings


global DB_NAME_QUERY


"""
查询
"""
# 通过微博用户名查某用户基本信息
def query_basic_info_by_name():
    name_params = input('Enter name: ')

    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE name = \'%s\'" % (DB_NAME_QUERY, name_params))
        result = cur.fetchone()
        row = result

        uid = str(row[0])
        name = str(row[1])
        rel_me = str(row[2])
        connect_to_my_friends = str(row[3])
        if row[4] is None:
            connect_to_my_friends_count = '0'
        else:
            connect_to_my_friends_count = str(row[4])
        location = str(row[9])
        description = str(row[10])
        url = str(row[11])
        domain = str(row[14])
        gender = str(row[15])
        followers_count = str(row[16])
        friends_count = str(row[17])
        statuses_count = str(row[18])
        favourites_count = str(row[20])
        created_at = str(row[21])
        verified = str(row[22])
        total_number = str(row[23])
        status_source = str(row[24])

        # 把 connect_to_my_friends_count 的 uid 列表中的每个查出 name，组成 has_one_level_friends 名字列表
        if connect_to_my_friends_count != '0':
            if connect_to_my_friends_count == '1':
                user_uid = connect_to_my_friends
                cur.execute("SELECT name FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, str(user_uid)))
                user_name_row = cur.fetchone()
                has_one_level_friends = str(user_name_row[0])
            else:
                temp_has_one_level_friends = []
                for user_uid in connect_to_my_friends.split(', '):
                    cur.execute("SELECT name FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, str(user_uid)))
                    user_name_row = cur.fetchone()
                    temp_has_one_level_friends.append(str(user_name_row[0]))
                has_one_level_friends = ', '.join(temp_has_one_level_friends)
        elif connect_to_my_friends_count == '0':
            has_one_level_friends = ''

        print("# uid: %s / name: %s / rel me: %s / has one level friends: %s / has one level friends count: %s "
              "/ location: %s / description: %s / url: %s / domain: %s / gender: %s / fans count: %s "
              "/ follow count: %s / statuses_count: %s / favourites_count: %s / created_at: %s / verified: %s "
              "/ total friends number: %s / client: %s"
              % (uid, name, rel_me, has_one_level_friends, connect_to_my_friends_count, location,
                 description, url, domain, gender, followers_count, friends_count, statuses_count,
                 favourites_count, created_at, verified, total_number, status_source))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 通过 uid 查某用户基本信息
# SELECT * FROM DB_NAME_QUERY.peopleinfo WHERE uid = 'uid_params';
def query_basic_info_by_uid():
    uid_params = input('Enter uid: ')

    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, uid_params))
        result = cur.fetchone()
        row = result

        uid = str(row[0])
        name = str(row[1])
        rel_me = str(row[2])
        connect_to_my_friends = str(row[3])
        if row[4] is None:
            connect_to_my_friends_count = '0'
        else:
            connect_to_my_friends_count = str(row[4])
        location = str(row[9])
        description = str(row[10])
        url = str(row[11])
        domain = str(row[14])
        gender = str(row[15])
        followers_count = str(row[16])
        friends_count = str(row[17])
        statuses_count = str(row[18])
        favourites_count = str(row[20])
        created_at = str(row[21])
        verified = str(row[22])
        total_number = str(row[23])
        status_source = str(row[24])

        # 把 connect_to_my_friends_count 的 uid 列表中的每个查出 name，组成 has_one_level_friends 名字列表
        if connect_to_my_friends_count != '0':
            if connect_to_my_friends_count == '1':
                user_uid = connect_to_my_friends
                cur.execute("SELECT name FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, str(user_uid)))
                user_name_row = cur.fetchone()
                has_one_level_friends = str(user_name_row[0])
            else:
                temp_has_one_level_friends = []
                for user_uid in connect_to_my_friends.split(', '):
                    cur.execute("SELECT name FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, str(user_uid)))
                    user_name_row = cur.fetchone()
                    temp_has_one_level_friends.append(str(user_name_row[0]))
                has_one_level_friends = ', '.join(temp_has_one_level_friends)
        elif connect_to_my_friends_count == '0':
            has_one_level_friends = ''

        print("# uid: %s / name: %s / rel me: %s / has one level friends: %s / has one level friends count: %s "
              "/ location: %s / description: %s / url: %s / domain: %s / gender: %s / fans count: %s "
              "/ follow count: %s / statuses_count: %s / favourites_count: %s / created_at: %s / verified: %s "
              "/ total friends number: %s / client: %s"
              % (uid, name, rel_me, has_one_level_friends, connect_to_my_friends_count, location,
                 description, url, domain, gender, followers_count, friends_count, statuses_count,
                 favourites_count, created_at, verified, total_number, status_source))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 通过微博用户名查某用户的互关好友列表及其好友信息


# 通过微博用户名查某一度好友能通过圈内二度好友认识的一度好友

# 所有一度好友信息

"""
统计
"""
# 总体概况：总人数、一度好友数、圈内二度好友数、二度好友数

# 能关联最多一度好友的圈内二度好友（取 10 条排序），能关联谁

# 一度好友中与其他一度好友互关最多的人（排序）、与圈内二度好友互关最多的人；分别是哪些人

# 一度好友/圈内二度好友/二度好友中认证情况统计

# 一度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端

# 圈内二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端

# 二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端


"""
推测
"""
# 某微博用户（研究对象）成长的城市、呆过的城市


if __name__ == '__main__':
    print('= mysql query =')

    db = pymysql.connect(
        host=settings.DB_HOST,
        port=int(settings.DB_PORT),
        user=settings.DB_USER,
        passwd=settings.DB_USER_PASSWORD,
        charset=settings.DB_CHARSET)
    cur = db.cursor()

    cur.execute('SHOW DATABASES;')
    # 这里列表得到的是一个个元组，每个元组由字符串和字符串后一个逗号构成
    db_list = list(cur.fetchall())
    print(db_list)
    DB_NAME_QUERY = input('Please enter DB name your created: ')

    print('= 查询 =')
    print('1 通过微博用户名查某用户基本信息')
    print('2 通过 uid 查某用户基本信息')
    print('3 通过微博用户名查某用户的互关好友列表及其好友信息')
    print('4 通过微博用户名查某一度好友能通过圈内二度好友认识的一度好友')
    print('5 所有一度好友信息')
    print('= 统计 =')
    print('6 总体概况：总人数、一度好友数、圈内二度好友数、二度好友数')
    print('7 能关联最多一度好友的圈内二度好友（取 10 条排序），能关联谁')
    print('8 一度好友中与其他一度好友互关最多的人（排序）、与圈内二度好友互关最多的人；分别是哪些人')
    print('9 一度好友/圈内二度好友/二度好友中认证情况统计')
    print('10 一度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端')
    print('11 圈内二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端')
    print('12 二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端')
    print('= 推测 =')
    print('q quit mysql query module')

    while True:
        value = input('Enter number to select function: ')
        if value not in ('1', '2', '3', '4', '5'):
            value = input('Enter number to select function: ')

        if value == '1':
            query_basic_info_by_name()

        if value == '2':
            query_basic_info_by_uid()

        if value == 'q':
            cur.close()
            db.close()
            exit()

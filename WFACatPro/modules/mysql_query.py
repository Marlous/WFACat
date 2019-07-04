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


# 通过微博用户名查某用户的互关好友列表
def query_friend_mutual_user():
    name_params = input('Enter name: ')

    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE name = \'%s\'" % (DB_NAME_QUERY, name_params))
        result = cur.fetchone()
        row = result

        uid_params = str(row[0])

        cur.execute("SELECT * FROM %s.mutualinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, uid_params))
        result = cur.fetchone()
        row = result

        temp_mutual_follow = []
        for user_uid in row[1].split(', '):
            cur.execute("SELECT name FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, str(user_uid)))
            row = cur.fetchone()
            temp_mutual_follow.append(str(row)[2:][:-3])

        mutual_follow_name = ', '.join(temp_mutual_follow)

        print("%s" % (mutual_follow_name))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 通过微博用户名查某一度好友能通过圈内二度好友认识的一度好友
def query_one_level_friend_probably_one_level():
    name_params = input('Enter name: ')

    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE name = \'%s\'" % (DB_NAME_QUERY, name_params))
        result = cur.fetchone()
        row = result

        uid_params = str(row[0])

        cur.execute("SELECT * FROM %s.u%s" % (DB_NAME_QUERY, uid_params))
        result = cur.fetchall()

        for row in result:
            cur.execute("SELECT * FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, str(row[0])))
            row_people = cur.fetchone()
            people_name = row_people[1]

            friend_people_list = []
            for by_friend_uid in row[1].split(', '):
                cur.execute("SELECT * FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, by_friend_uid))
                row_friend_people = cur.fetchone()
                each_people_name = row_friend_people[1]
                friend_people_list.append(str(each_people_name))
            friend_people_name = ', '.join(friend_people_list)

            print("Probably people: %s via: %s count %d" % (people_name, friend_people_name, row[2]))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 所有一度好友信息
def query_all_one_level_friend():
    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE rel_me = \'1\'" % (DB_NAME_QUERY))
        result = cur.fetchall()

        for row in result:
            people_name_my_friend = ""
            people_name_two_level_friend = ""

            uid = str(row[0])
            name = str(row[1])

            connect_to_my_friends_count = row[4]
            connect_to_my_friends = str(row[3])
            if connect_to_my_friends_count >= 2:
                people_uid_to_name_my_friend_list = []
                for people_uid_my_friend in connect_to_my_friends.split(", "):
                    cur.execute(
                        "SELECT * FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, people_uid_my_friend))
                    row_temp = cur.fetchone()
                    each_people_name = row_temp[1]
                    people_uid_to_name_my_friend_list.append(str(each_people_name))
                    people_name_my_friend = ', '.join(people_uid_to_name_my_friend_list)
            elif connect_to_my_friends_count == 1:
                cur.execute("SELECT * FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, connect_to_my_friends))
                row_temp = cur.fetchone()
                one_people_name = row_temp[1]
                people_name_my_friend = one_people_name

            connect_to_two_level_friends_count = row[6]
            connect_to_two_level_friends = str(row[5])
            if connect_to_two_level_friends_count >= 2:
                people_uid_to_name_two_level_friend_list = []
                for people_uid_two_level_friend in connect_to_two_level_friends.split(", "):
                    cur.execute(
                        "SELECT * FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, people_uid_two_level_friend))
                    row_temp_2 = cur.fetchone()
                    each_people_name_2 = row_temp_2[1]
                    people_uid_to_name_two_level_friend_list.append(str(each_people_name_2))
                    people_name_two_level_friend = ', '.join(people_uid_to_name_two_level_friend_list)
            elif connect_to_my_friends_count == 1:
                cur.execute("SELECT * FROM %s.peopleinfo WHERE uid = \'%s\'" % (DB_NAME_QUERY, connect_to_two_level_friends))
                row_temp_2 = cur.fetchone()
                one_people_name_2 = row_temp_2[1]
                people_name_two_level_friend = one_people_name_2

            location = str(row[9])
            description = str(row[10])
            gender = str(row[15])
            followers_count = str(row[16])
            friends_count = str(row[17])
            statuses_count = str(row[18])
            favourites_count = str(row[20])
            created_at = str(row[21])
            verified = str(row[22])
            total_number = str(row[23])
            status_source = str(row[24])

            print("-----------------------------------------------------------------------------")
            print("uid: %s / name: %s / acquire one level people: %s / acquire one level people count: %d / \
            acquire two level people: %s / acquire two level people count: %d / \
            location: %s / description: %s / gender: %s / followers count: %s / friends count: %s / \
            statuses count: %s / favourites count: %s / created at: %s / verified: %s / \
            total friends number: %s / client: %s"
                  % (uid, name, people_name_my_friend, connect_to_my_friends_count,
                     people_name_two_level_friend, connect_to_two_level_friends_count,
                     location, description, gender, followers_count, friends_count,
                     statuses_count, favourites_count, created_at, verified,
                     total_number, status_source))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


"""
统计
"""
# 总体概况：总人数、一度好友数、圈内二度好友数、圈外二度好友数、二度好友数
def statistic_person_count():
    try:
        cur.execute("SELECT COUNT(rel_me) FROM %s.peopleinfo" % (DB_NAME_QUERY))
        row = cur.fetchone()
        total_people = row[0]
        print("总人数: %d" % (total_people))

        cur.execute("SELECT COUNT(rel_me) FROM %s.peopleinfo WHERE rel_me = \'1\'" % (DB_NAME_QUERY))
        row = cur.fetchone()
        one_level_people = row[0]
        one_level_people_proportion = (one_level_people / total_people) * 100
        print("一度好友数: %d / 占比: %.2f%%" % (one_level_people, one_level_people_proportion))

        cur.execute("SELECT COUNT(rel_me) FROM %s.peopleinfo WHERE rel_me = \'2\'" % (DB_NAME_QUERY))
        row = cur.fetchone()
        two_level_in_people = row[0]
        two_level_in_people_proportion = (two_level_in_people / total_people) * 100
        print("圈内二度好友数（与研究对象一度好友相关的二度好友）: %d / 占比: %.2f%%"
              % (two_level_in_people, two_level_in_people_proportion))

        two_level_out_people = total_people - two_level_in_people
        two_level_out_people_proportion = (two_level_out_people / total_people) * 100
        print("圈外二度好友数（与研究对象一度好友无关的二度好友）: %d / 占比: %.2f%%"
              % (two_level_out_people, two_level_out_people_proportion))

        two_level_people = total_people - one_level_people
        two_level_people_proportion = two_level_people / total_people
        print("二度好友数: %d / 占比: %.2f%%"
              % (two_level_people, two_level_people_proportion))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 一度好友中与其他一度好友互关最多的人（排序）、与圈内二度好友互关最多的人
def mutual_follow_count_sort():
    try:
        print("一度好友中与其他一度好友互关最多的人:")
        cur.execute("SELECT uid, name, connect_to_my_friends_count FROM %s.peopleinfo WHERE rel_me = \'1\' "
                    "ORDER BY connect_to_my_friends_count DESC;"
                    % (DB_NAME_QUERY))
        result = cur.fetchall()
        for row in result:
            uid = row[0]
            name = row[1]
            connect_to_my_friends_count = row[2]
            print("uid: %s / name: %s / connect to one level count: %d"
                  % (str(uid), str(name), connect_to_my_friends_count))

        print("----------------------------------")
        print("一度好友中与其他圈内二度好友互关最多的人:")
        cur.execute("SELECT uid, name, connect_to_two_level_friends_count FROM %s.peopleinfo WHERE rel_me = \'1\' "
                    "ORDER BY connect_to_two_level_friends_count DESC;"
                    % (DB_NAME_QUERY))
        result = cur.fetchall()
        for row in result:
            uid = row[0]
            name = row[1]
            connect_to_two_level_friends_count = row[2]
            print("uid: %s / name: %s / connect to two level count: %d"
                  % (str(uid), str(name), connect_to_two_level_friends_count))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 一度好友/圈内二度好友/二度好友中认证情况统计
def statistic_verified():
    try:
        cur.execute("SELECT COUNT(verified = \'True\') FROM %s.peopleinfo WHERE rel_me = \'1\' " % (DB_NAME_QUERY))
        row = cur.fetchone()
        print("一度好友认证数量：%d" % (row[0]))

        cur.execute("SELECT COUNT(verified = \'True\') FROM %s.peopleinfo WHERE rel_me = \'2\' " % (DB_NAME_QUERY))
        row = cur.fetchone()
        print("圈内二度好友认证数量：%d" % (row[0]))

        cur.execute("SELECT COUNT(verified = \'True\') FROM %s.peopleinfo WHERE rel_me = \'2.1\' " % (DB_NAME_QUERY))
        row = cur.fetchone()
        print("圈外二度好友认证数量：%d" % (row[0]))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 一度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、客户端
def statistic_one_level():
    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE rel_me = \'1\' " % (DB_NAME_QUERY))
        result = cur.fetchall()

        location_dict = {}
        gender_dict = {}
        created_dict = {}
        client_dict = {}

        for row in result:
            # 地理位置
            if row[9] in location_dict.keys():
                location_dict[row[9]] = location_dict[row[9]] + 1
            else:
                location_dict[row[9]] = 1

            # 性别
            if row[15] in gender_dict.keys():
                gender_dict[row[15]] = int(gender_dict[row[15]]) + 1
            else:
                gender_dict[row[15]] = 1

            # 微博创建时间
            created = row[21][-4:]
            if created in created_dict.keys():
                created_dict[created] = int(created_dict[created]) + 1
            else:
                created_dict[created] = 1

            # 客户端
            if row[24] is not None:
                if row[24] in client_dict.keys():
                    client_dict[row[24]] = int(client_dict[row[24]]) + 1
                else:
                    client_dict[row[24]] = 1

        location_top_key = max(location_dict, key=lambda x: location_dict[x])
        created_top_key = max(created_dict, key=lambda x: created_dict[x])
        client_top_key = max(client_dict, key=lambda x: client_dict[x])

        # 关注数
        cur.execute("SELECT name, followers_count FROM %s.peopleinfo WHERE rel_me = \'1\' "
                    "ORDER BY followers_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_followers_count = row[0]
        followers_count = row[1]

        # 粉丝数
        cur.execute("SELECT name, friends_count FROM %s.peopleinfo WHERE rel_me = \'1\' "
                    "ORDER BY friends_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_friends_count = row[0]
        friends_count = row[1]

        # 状态数
        cur.execute("SELECT name, statuses_count FROM %s.peopleinfo WHERE rel_me = \'1\' "
                    "ORDER BY statuses_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_statuses_count = row[0]
        statuses_count = row[1]

        # 点赞数
        cur.execute("SELECT name, favourites_count FROM %s.peopleinfo WHERE rel_me = \'1\' "
                    "ORDER BY favourites_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_favourites_count = row[0]
        favourites_count = row[1]

        # 互关好友总数
        cur.execute("SELECT name, total_number FROM %s.peopleinfo WHERE rel_me = \'1\' "
                    "ORDER BY total_number DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_total_number = row[0]
        total_number = row[1]

        print("------ 一度好友 -------")
        print("地理位置最多的：%s / 性别统计：男 %d 人，女 %d 人 / "
              "关注数最多的：%s %d / 粉丝数最多的：%s %d / "
              "状态数最多的：%s %d / 点赞数最多的：%s %d / "
              "微博创建时间统计：%s / "
              "互关好友总数最多的：%s %d / 客户端最多的：%s"
              % (str(location_top_key), int(gender_dict['f']), int(gender_dict['m']),
                 str(name_followers_count), int(followers_count), str(name_friends_count), int(friends_count),
                 str(name_statuses_count), int(statuses_count), str(name_favourites_count), int(favourites_count),
                 str(created_top_key),
                 str(name_total_number), int(total_number), str(client_top_key)))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 圈内二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、客户端
def statistic_inner_two_level():
    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE rel_me = \'2\' " % (DB_NAME_QUERY))
        result = cur.fetchall()

        location_dict = {}
        gender_dict = {}
        created_dict = {}
        client_dict = {}

        for row in result:
            # 地理位置
            if row[9] in location_dict.keys():
                location_dict[row[9]] = location_dict[row[9]] + 1
            else:
                location_dict[row[9]] = 1

            # 性别
            if row[15] in gender_dict.keys():
                gender_dict[row[15]] = int(gender_dict[row[15]]) + 1
            else:
                gender_dict[row[15]] = 1

            # 微博创建时间
            created = row[21][-4:]
            if created in created_dict.keys():
                created_dict[created] = int(created_dict[created]) + 1
            else:
                created_dict[created] = 1

            # 客户端
            if row[24] is not None:
                if row[24] in client_dict.keys():
                    client_dict[row[24]] = int(client_dict[row[24]]) + 1
                else:
                    client_dict[row[24]] = 1

        location_top_key = max(location_dict, key=lambda x: location_dict[x])
        created_top_key = max(created_dict, key=lambda x: created_dict[x])
        client_top_key = max(client_dict, key=lambda x: client_dict[x])

        # 关注数
        cur.execute("SELECT name, followers_count FROM %s.peopleinfo WHERE rel_me = \'2\' "
                    "ORDER BY followers_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_followers_count = row[0]
        followers_count = row[1]

        # 粉丝数
        cur.execute("SELECT name, friends_count FROM %s.peopleinfo WHERE rel_me = \'2\' "
                    "ORDER BY friends_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_friends_count = row[0]
        friends_count = row[1]

        # 状态数
        cur.execute("SELECT name, statuses_count FROM %s.peopleinfo WHERE rel_me = \'2\' "
                    "ORDER BY statuses_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_statuses_count = row[0]
        statuses_count = row[1]

        # 点赞数
        cur.execute("SELECT name, favourites_count FROM %s.peopleinfo WHERE rel_me = \'2\' "
                    "ORDER BY favourites_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_favourites_count = row[0]
        favourites_count = row[1]

        print("------ 圈内二度好友 -------")
        print("地理位置最多的：%s / 性别统计：男 %d 人，女 %d 人 / "
              "关注数最多的：%s %d / 粉丝数最多的：%s %d / "
              "状态数最多的：%s %d / 点赞数最多的：%s %d / "
              "微博创建时间统计：%s / "
              "客户端最多的：%s"
              % (str(location_top_key), int(gender_dict['f']), int(gender_dict['m']),
                 str(name_followers_count), int(followers_count), str(name_friends_count), int(friends_count),
                 str(name_statuses_count), int(statuses_count), str(name_favourites_count), int(favourites_count),
                 str(created_top_key),
                 str(client_top_key)))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端
def statistic_three_level():
    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE rel_me = \'2.1\' " % (DB_NAME_QUERY))
        result = cur.fetchall()

        location_dict = {}
        gender_dict = {}
        created_dict = {}
        client_dict = {}

        for row in result:
            # 地理位置
            if row[9] in location_dict.keys():
                location_dict[row[9]] = location_dict[row[9]] + 1
            else:
                location_dict[row[9]] = 1

            # 性别
            if row[15] in gender_dict.keys():
                gender_dict[row[15]] = int(gender_dict[row[15]]) + 1
            else:
                gender_dict[row[15]] = 1

            # 微博创建时间
            created = row[21][-4:]
            if created in created_dict.keys():
                created_dict[created] = int(created_dict[created]) + 1
            else:
                created_dict[created] = 1

            # 客户端
            if row[24] is not None:
                if row[24] in client_dict.keys():
                    client_dict[row[24]] = int(client_dict[row[24]]) + 1
                else:
                    client_dict[row[24]] = 1

        location_top_key = max(location_dict, key=lambda x: location_dict[x])
        created_top_key = max(created_dict, key=lambda x: created_dict[x])
        client_top_key = max(client_dict, key=lambda x: client_dict[x])

        # 关注数
        cur.execute("SELECT name, followers_count FROM %s.peopleinfo WHERE rel_me = \'2.1\' "
                    "ORDER BY followers_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_followers_count = row[0]
        followers_count = row[1]

        # 粉丝数
        cur.execute("SELECT name, friends_count FROM %s.peopleinfo WHERE rel_me = \'2.1\' "
                    "ORDER BY friends_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_friends_count = row[0]
        friends_count = row[1]

        # 状态数
        cur.execute("SELECT name, statuses_count FROM %s.peopleinfo WHERE rel_me = \'2.1\' "
                    "ORDER BY statuses_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_statuses_count = row[0]
        statuses_count = row[1]

        # 点赞数
        cur.execute("SELECT name, favourites_count FROM %s.peopleinfo WHERE rel_me = \'2.1\' "
                    "ORDER BY favourites_count DESC;"
                    % (DB_NAME_QUERY))
        row = cur.fetchone()
        name_favourites_count = row[0]
        favourites_count = row[1]

        print("------ 二度好友 -------")
        print("地理位置最多的：%s / 性别统计：男 %d 人，女 %d 人 / "
              "关注数最多的：%s %d / 粉丝数最多的：%s %d / "
              "状态数最多的：%s %d / 点赞数最多的：%s %d / "
              "微博创建时间统计：%s / "
              "客户端最多的：%s"
              % (str(location_top_key), int(gender_dict['f']), int(gender_dict['m']),
                 str(name_followers_count), int(followers_count), str(name_friends_count), int(friends_count),
                 str(name_statuses_count), int(statuses_count), str(name_favourites_count), int(favourites_count),
                 str(created_top_key),
                 str(client_top_key)))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


# 所有用户微博创建时间统计
def statistic_created():
    try:
        cur.execute("SELECT created_at FROM %s.peopleinfo" % (DB_NAME_QUERY))
        result = cur.fetchall()

        created_at_dict = {}

        for row in result:
            if str(row[0])[26:] in created_at_dict.keys():
                created_at_dict[str(row[0])[26:]] = created_at_dict[str(row[0])[26:]] + 1
            else:
                created_at_dict[str(row[0])[26:]] = 1

        created_at_sorted_list = sorted(created_at_dict, key=created_at_dict.get, reverse=True)

        for item in created_at_sorted_list:
            print("创建时间：%s 数量：%d" % (str(item), created_at_dict[item]))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


"""
推测
"""
# 某微博用户（研究对象）成长的城市、久居的城市
def location_probably():
    try:
        cur.execute("SELECT * FROM %s.peopleinfo WHERE rel_me = \'1\' " % (DB_NAME_QUERY))
        result = cur.fetchall()

        location_dict = {}

        for row in result:
            # 地理位置
            if row[9] in location_dict.keys():
                location_dict[row[9]] = location_dict[row[9]] + 1
            else:
                location_dict[row[9]] = 1

        location_list_sorted = sorted(location_dict, key=location_dict.get, reverse=True)

        location_list = []
        count = 0
        for item in location_list_sorted:
            location_list.append(item)
            count = count + 1
            if count == 7:
                break
                
        print("可能的出生成长、久居的城市，按可能性排序: %s" % (', '.join(location_list)))

    except Exception:
        print('ERROR! Unable to fetch data')
        traceback.print_exc()


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
    # 这里列表得到的是一个个元组，先遍历列表，再遍历列表中每项的元组
    db_list_raw = list(cur.fetchall())
    db_list_handle = []
    for list_item in db_list_raw:
        for item in list_item:
            db_list_handle.append(item)
    db_list = ', '.join(db_list_handle)
    print(db_list)
    DB_NAME_QUERY = input('Please enter DB name your created: ')

    print('= 注释 =')
    print('分为一度好友（直接与研究对象互关的）；'
          '圈内二度好友（二度好友中能关联至少互关两个一度好友的）；圈外二度好友（二度好友中只互关一个一度好友的）')
    print('= 查询 =')
    print('1 通过微博用户名查某用户基本信息')
    print('2 通过 uid 查某用户基本信息')
    print('3 通过微博用户名查某用户的互关好友列表')
    print('4 通过微博用户名查某一度好友能通过圈内二度好友认识的一度好友')
    print('5 所有一度好友信息')
    print('= 统计 =')
    print('6 总体概况：总人数、一度好友数、圈内二度好友数、圈外二度好友数、二度好友数')
    print('7 一度好友中与其他一度好友互关最多的人（排序）、与圈内二度好友互关最多的人')
    print('8 一度好友/圈内二度好友/二度好友中认证情况统计')
    print('9 一度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、互关好友总数、客户端')
    print('10 圈内二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、客户端')
    print('11 二度好友地理位置统计、性别统计、关注数、粉丝数、状态数、点赞数、微博创建时间、客户端')
    print('12 所有用户微博创建时间统计')
    print('= 推测 =')
    print('13 可能的出生成长、久居的城市，按可能性排序。/ '
          '研究对象年龄较小的，排名靠最前的为出生成长的城市可能性最大；'
          '研究对象年龄较大的，排名靠最前的为久居的城市可能性最大）')
    print('= 退出 =')
    print('q quit mysql query module')

    while True:
        value = input('Enter number to select function: ')
        if value not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'):
            value = input('Enter number to select function: ')

        if value == '1':
            query_basic_info_by_name()

        if value == '2':
            query_basic_info_by_uid()

        if value == '3':
            query_friend_mutual_user()

        if value == '4':
            query_one_level_friend_probably_one_level()

        if value == '5':
            query_all_one_level_friend()

        if value == '6':
            statistic_person_count()

        if value == '7':
            mutual_follow_count_sort()

        if value == '8':
            statistic_verified()

        if value == '9':
            statistic_one_level()

        if value == '10':
            statistic_inner_two_level()

        if value == '11':
            statistic_three_level()

        if value == '12':
            statistic_created()

        if value == '13':
            location_probably()

        if value == 'q':
            cur.close()
            db.close()
            exit()

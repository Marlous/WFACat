# -*- coding: utf-8 -*-

"""
WFACatPro.analysis_to_mysql
~~~~~~~~~~~~~~~~~~~
This is a analysis to mysql module.
"""


import settings

import pymysql
import os
import json
import re
import warnings


def judge_and_create_db(db_name_params):
    """
    :param db_name_params:
    :return: 无返回值。判断是否存在此名字的数据库，存在则询问是否删除，不存在则创建。
    """
    db_try = pymysql.connect(
        host=settings.DB_HOST,
        port=int(settings.DB_PORT),
        user=settings.DB_USER,
        passwd=settings.DB_USER_PASSWORD,
        charset=settings.DB_CHARSET)
    cur_try = db_try.cursor()

    cur_try.execute('SHOW DATABASES;')
    # 这里列表得到的是一个个元组，每个元组由字符串和字符串后一个逗号构成
    db_list = list(cur_try.fetchall())

    if (db_name_params,) in db_list:
        values = input('Database name exist! Delete this database? [Y/N]')
        while values not in ('Y', 'N'):
            values = input('Please enter Y or N !')

        if values == 'Y':
            cur_try.execute('drop database ' + db_name_params + ';')
            print('%s database deleted success!' % db_name_params)
            cur_try.execute('create database ' + db_name_params + ';')
            print('%s database created success!' % db_name_params)
        elif values == 'N':
            exit('Noting occured!')

    else:
        cur_try.execute('create database ' + db_name_params + ' CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
        print('%s database created success!' % db_name_params)

    cur_try.close()
    db_try.close()


def create_db_table(db_name_params):
    """
    创建相关的表
    """
    db = pymysql.connect(
        host=settings.DB_HOST,
        port=int(settings.DB_PORT),
        user=settings.DB_USER,
        passwd=settings.DB_USER_PASSWORD,
        charset=settings.DB_CHARSET,
        db=db_name_params)

    cur = db.cursor()

    cur.execute('USE ' + db_name_params + ';')

    sql_create_table = "CREATE TABLE " + "`" + db_name_params + "`.`peopleinfo` (" \
        "`uid` CHAR(10) NOT NULL," \
        "`name` VARCHAR(45) NULL," \
        "`rel_me` VARCHAR(5) NULL," \
        "`connect_to_my_friends` VARCHAR(5000) NULL," \
        "`connect_to_two_level_friends` VARCHAR(5000) NULL," \
        "`province` VARCHAR(5) NULL," \
        "`city` VARCHAR(5) NULL," \
        "`location` VARCHAR(20) NULL," \
        "`description` VARCHAR(1000) NULL," \
        "`url` VARCHAR(100) NULL," \
        "`profile_image_url` VARCHAR(120) NULL," \
        "`profile_url` VARCHAR(45) NULL," \
        "`domain` VARCHAR(45) NULL," \
        "`gender` VARCHAR(1) NULL," \
        "`followers_count` INT NULL," \
        "`friends_count` INT NULL," \
        "`statuses_count` INT NULL," \
        "`video_status_count` INT NULL," \
        "`favourites_count` INT NULL," \
        "`created_at` VARCHAR(45) NULL," \
        "`verified` VARCHAR(10) NULL," \
        "`total_number` INT NULL," \
        "`status_source` VARCHAR(50) NULL,PRIMARY KEY (`uid`)" \
        ");"
    cur.execute(sql_create_table)
    db.commit()

    cur.close()
    db.close()


def produce_my_friendinfo_dict():
    """
    :return: 无参数。返回一个字典，字典键是研究对象的 uid，值分别是其互关好友列表
    """
    # 用一个字典存储研究对象的好友信息，研究对象每个好友的好友信息（一个列表）
    my_friends_info_dict = {}

    file_list = os.listdir('./temp/1')
    file_name = './temp/1/' + file_list[0]  # 文件夹下的 json 文件

    temp_save_friends_info_list = []

    with open(file_name, 'r', encoding='utf-8') as one_json_file:  # 提取遍历 json 中每个用户的 uid
        # 将 json 文件内容转为字典，注意字典的索引可以是字符串或整数
        handle_json_file = json.loads(one_json_file.read())

        user_num = 0
        for user_item in handle_json_file['users']:
            # 提取用户的 uid
            user_uid = str(handle_json_file['users'][user_num]['id'])
            temp_save_friends_info_list.append(user_uid)
            user_num = user_num + 1
    one_json_file.close()

    # 添加进字典，键是 json 文件名，值是其好友列表
    my_friends_info_dict[file_list[0][0:10]] = temp_save_friends_info_list
    return my_friends_info_dict


def produce_friends_friendinfo_dict():
    """
    :return: 无参数。返回一个字典。研究对象的好友的好友信息写入字典。遍历 2 度人脉文件夹中所有 json 文件
    """
    everybody_friends_info_dict = {}

    file_list = os.listdir('./temp/2')

    # 遍历 2 度文件夹下的 json 文件
    for json_file_num in range(0, len(file_list)):
        file_name = './temp/2/' + file_list[json_file_num]  # 文件夹下的每一个 json 文件
        temp_save_friends_info_list = []

        with open(file_name, 'r', encoding='utf-8') as one_json_file:  # 提取遍历 json 中每个用户的 uid
            # 将 json 文件内容转为字典，注意字典的索引可以是字符串或整数
            handle_json_file = json.loads(one_json_file.read())

            user_num = 0
            for user_item in handle_json_file['users']:
                # 提取用户的 uid
                user_uid = str(handle_json_file['users'][user_num]['id'])
                temp_save_friends_info_list.append(user_uid)
                user_num = user_num + 1
        one_json_file.close()

        everybody_friends_info_dict[file_list[json_file_num]
                                    [0:10]] = temp_save_friends_info_list
        del temp_save_friends_info_list

    return everybody_friends_info_dict


def write_all_person_info_in_mysql(db_name_params):
    db = pymysql.connect(
        host=settings.DB_HOST,
        port=int(settings.DB_PORT),
        user=settings.DB_USER,
        passwd=settings.DB_USER_PASSWORD,
        charset=settings.DB_CHARSET,
        db=db_name_params)

    cur = db.cursor()
    cur.execute('USE ' + db_name_params + ';')

    person_writed_list = []
    # 因为自己的信息不需要写入数据库
    my_friends_json_name = os.listdir('./temp/1')[0][0:10]
    person_writed_list.append(my_friends_json_name)

    """
    遍历 n 度（n 个）人脉文件夹中所有。此处只遍历 2 次，遍历文件夹 1、2
    """
    level_local = 1

    while level_local <= 2:
        file_path = './temp/' + str(level_local)
        file_list = os.listdir(file_path)  # 第 n 度文件夹路径

        """
        遍历 n 度文件夹下的 json 文件
        """
        for json_file_num in range(0, len(file_list)):
            file_name = file_path + '/' + \
                file_list[json_file_num]  # 文件夹下的每一个 json 文件

            """
            提取遍历 json 中每个用户的 uid
            """
            with open(file_name, 'r', encoding='utf-8') as one_json_file:
                # 将 json 文件内容转为字典，注意字典的索引可以是字符串或整数
                handle_json_file = json.loads(one_json_file.read())

                user_num = 0
                for user_item in handle_json_file['users']:
                    # 提取用户的 uid 等信息
                    uid = handle_json_file['users'][user_num]['id']
                    name = handle_json_file['users'][user_num]['name']
                    province = handle_json_file['users'][user_num]['province']
                    city = handle_json_file['users'][user_num]['city']
                    location = handle_json_file['users'][user_num]['location']
                    description = handle_json_file['users'][user_num]['description']
                    url = handle_json_file['users'][user_num]['url']
                    profile_image_url = handle_json_file['users'][user_num]['profile_image_url']
                    profile_url = handle_json_file['users'][user_num]['profile_url']
                    domain = handle_json_file['users'][user_num]['domain']
                    gender = handle_json_file['users'][user_num]['gender']
                    followers_count = handle_json_file['users'][user_num]['followers_count']
                    friends_count = handle_json_file['users'][user_num]['friends_count']
                    statuses_count = handle_json_file['users'][user_num]['statuses_count']
                    video_status_count = handle_json_file['users'][user_num]['video_status_count']
                    favourites_count = handle_json_file['users'][user_num]['favourites_count']
                    created_at = handle_json_file['users'][user_num]['created_at']
                    verified = handle_json_file['users'][user_num]['verified']

                    """
                    存入 status_source 属性值
                    判断 status 这个字段书否存在（debug 时显示不存在），说明可能不存在
                    """
                    if 'status' in handle_json_file['users'][user_num]:
                        if 'source' in handle_json_file['users'][user_num]['status']:
                            temp_status_source = handle_json_file['users'][user_num]['status']['source']
                            # 正则表达式提取出 <a> 标签中的手机客户端型号
                            ######
                            print('1 temp_status_source :' + str(temp_status_source))
                            pattern_html = re.compile(">(.*?)<")
                            pattern_txt = re.compile("[a-zA-Z0-9\u4e00-\u9fa5]+")
                            # 先把 json 中 html 标签中的内容匹配出来，放进 temp_two_status_source（是一个列表）
                            temp_two_status_source = pattern_html.findall(str(temp_status_source))
                            #######
                            print('2 temp_two_status_source :' + str(temp_two_status_source))
                            if list(temp_two_status_source):
                                # json 中取出的匹配出变成列表。此处（不为空的话）将其再次匹配，只要数字、字母、中文。过滤掉特殊字符
                                temp_three_status_source = temp_two_status_source[0]
                                # 将再次匹配得到的列表连接起来，变成字符串
                                status_source = " ".join(pattern_txt.findall(str(temp_three_status_source)))
                                #######
                                print(str(status_source))
                                cur.execute("UPDATE " + db_name_params + ".peopleinfo SET status_source = '" +
                                            str(status_source) + "' WHERE uid = '" + str(uid) + "';")

                    """
                    存入 verified 属性值
                    """
                    if str(verified) != 'False':
                        cur.execute("UPDATE " + db_name_params + ".peopleinfo SET verified = '" + str(verified) +
                                    "' WHERE uid = '" + str(uid) + "';")

                    """
                    将提取的信息剩下的属性值写入数据库
                    """
                    sql_write = "UPDATE " + db_name_params + ".peopleinfo SET name = '" + str(name) + \
                                "', province = '" + str(province) + \
                                "', city = '" + str(city) + \
                                "', location = '" + str(location) + \
                                "', description = \"" + str(description) + \
                                "\", url = '" + str(url) + \
                                "', profile_image_url = '" + str(profile_image_url) + \
                                "', profile_url = '" + str(profile_url) + \
                                "', domain = '" + str(domain) + \
                                "', gender = '" + str(gender) + \
                                "', followers_count = '" + str(followers_count) + \
                                "', friends_count = '" + str(friends_count) + \
                                "', statuses_count = '" + str(statuses_count) + \
                                "', video_status_count = '" + str(video_status_count) + \
                                "', favourites_count = '" + str(favourites_count) + \
                                "', created_at = '" + str(created_at) + \
                                "' WHERE uid = '" + str(uid) + "';"

                    cur.execute(sql_write)
                    db.commit()

                    user_num = user_num + 1

                    if str(uid) not in person_writed_list:
                        person_writed_list.append(str(uid))

                """
                写入此好友互关的好友数
                """
                if level_local == 2:
                    total_number = handle_json_file['total_number']
                    cur.execute("UPDATE " + db_name_params + ".peopleinfo SET total_number = '" + str(total_number) +
                                "' WHERE uid = '" + file_name[9:-5] + "';")
                    db.commit()

            one_json_file.close()

        level_local = int(level_local) + 1

    cur.close()
    db.close()


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    print('= MySQL analysis =')
    print('Make sure mysql service started! Then input database name ~')
    DB_NAME = input(
        'Enter database name (weibo user who you want to analysis):')

    judge_and_create_db(DB_NAME)
    create_db_table(DB_NAME)

    print('Analysizing, wait...')

    """
    对数据处理，得到两个基本集合
    """
    print('log: basic data...')
    my_friendinfo_dict = produce_my_friendinfo_dict()
    friends_friendinfo_dict = produce_friends_friendinfo_dict()

    """
    将每个好友的好友信息列表取出放进一个列表
    """
    friends_friendinfo_dict_values_list = []
    for value in friends_friendinfo_dict.values():  # 遍历字典中的值（多个列表）
        friends_friendinfo_dict_values_list.append(value)

    """
    每个好友信息列表逐个取交集（两两取交集）。结果减去自己和自己的好友（一度好友）即是除度为 1 的二度好友
    得到第三个基本集合
    总算法复杂度（比较次数）为排列组合算出来的次数 C n 2 次，n 是一度好友数量
    """
    print('log: two level friends...')
    file_list = os.listdir('./temp/1')
    my_uid = file_list[0][0:10]  # 文件夹 1 下的 json 文件名
    temp_two_level_useful_friends_list = []

    count = 1
    for person in my_friendinfo_dict[my_uid][0:-1]:
        for temp_person in my_friendinfo_dict[my_uid][count:]:
            temp_set = set(friends_friendinfo_dict[person]) & set(friends_friendinfo_dict[temp_person])
            for item in list(temp_set):
                temp_two_level_useful_friends_list.append(item)
        count =count + 1

    # 用元组去掉重复的
    two_level_useful_friends_list = list(set(temp_two_level_useful_friends_list))
    two_level_useful_friends_list.remove(my_uid)
    # 注意，如果某个一度好友与自己的朋友圈无任何关系，那么他就已经不在其中，不需要再移出一次
    for item in my_friendinfo_dict[my_uid]:
        if item in two_level_useful_friends_list:
            two_level_useful_friends_list.remove(item)

    """
    连接进入数据库
    """
    print('log: connecting to mysql...')
    db = pymysql.connect(
        host=settings.DB_HOST,
        port=int(settings.DB_PORT),
        user=settings.DB_USER,
        passwd=settings.DB_USER_PASSWORD,
        charset=settings.DB_CHARSET,
        db=DB_NAME)

    cur = db.cursor()
    cur.execute('USE ' + DB_NAME + ';')

    """
    # 写入每个好友（一度、二度，全部）uid 信息
    """
    print('log: every user uid to mysql, may be long time, wait...')
    cur.execute('USE ' + DB_NAME + ';')

    uid_saved = []
    # 不记录自己
    uid_saved.append(my_uid)

    for item in my_friendinfo_dict[my_uid]:
        # 一度人脉，标记为 1
        cur.execute("INSERT INTO " + DB_NAME +
                    ".peopleinfo (uid, rel_me) VALUES ('" + item + "', '1');")
        db.commit()
        uid_saved.append(item)

    for data in friends_friendinfo_dict:
        for item in friends_friendinfo_dict[data]:
            if item not in uid_saved:
                if item in two_level_useful_friends_list:
                    # 节点度不为 1 的二度人脉，标记为 2
                    cur.execute("INSERT INTO " + DB_NAME +
                                ".peopleinfo (uid, rel_me) VALUES ('" + item + "', '2');")
                    db.commit()
                    uid_saved.append(item)
                else:
                    # 节点度为 1 的二度人脉，标记为 2.1
                    cur.execute("INSERT INTO " + DB_NAME +
                                ".peopleinfo (uid, rel_me) VALUES ('" + item + "', '2.1');")
                    db.commit()
                    uid_saved.append(item)


    """
    计算每个一度好友 connect_to_my_friends 写入数据库
    某个好友的好友信息列表与自己的信息列表取交集
    """
    print('log: connect_to_my_friends...')
    for data in my_friendinfo_dict[my_uid]:
        # 好友的好友列表和我的好友列表取交集
        connect_to_my_friends = set(
            friends_friendinfo_dict[data]) & set(
            my_friendinfo_dict[my_uid])
        temp_content = ", ".join(list(connect_to_my_friends))

        cur.execute(
            "UPDATE " + DB_NAME +
            ".peopleinfo SET connect_to_my_friends = '" + temp_content +
            "' WHERE uid = '" + data + "';")
        db.commit()
        del temp_content

    """
    计算每个一度好友 connect_to_two_level_friends 写入数据库
    某个好友信息列表与 two_level_useful_friends_list 集合取交集
    two_level_useful_friends_list 是所有除去节点度为一的二度好友
    """
    print('log: connect_to_two_level_friends...')
    # 初始化一个字典，记下每个一度好友的二度好友列表（除去节点的度为一的）
    friends_two_level_friendinfo_dict = {}

    for data in my_friendinfo_dict[my_uid]:
        # 好友的好友列表和二度人脉 two_level_useful_friends_list 取交集
        connect_to_two_level_friends = set(
            friends_friendinfo_dict[data]) & set(
            two_level_useful_friends_list)
        temp_content = ", ".join(list(connect_to_two_level_friends))
        # 记下每个一度好友的二度好友列表（除去节点的度为一的）
        friends_two_level_friendinfo_dict[data] = list(
            connect_to_two_level_friends)

        cur.execute(
            "UPDATE " + DB_NAME +
            ".peopleinfo SET connect_to_two_level_friends = '" + temp_content +
            "' WHERE uid = '" + data + "';")
        db.commit()
        del temp_content

    """
    计算每个一度好友可以间接认识哪些其它一度好友，为其建立一张表，表属性分别是可以间接认识的人、通过谁，写入数据库
    每个好友的二度人脉好友信息列表（通过字典查到）与其它好友的二度人脉好友信息列表取交集
    集合不为空，表示可以通过集合里的人建立联系。
    总算法复杂度（比较次数）为排列组合算出来的次数 C n 2 次，n 是一度好友数量
    """
    print('log: maybe_connect_to_friends...')
    count = 1
    for person in my_friendinfo_dict[my_uid][0:-1]:
        for temp_person in my_friendinfo_dict[my_uid][count:]:
            two_level_friends_inter_have = set(
                friends_two_level_friendinfo_dict[person]) & set(
                friends_two_level_friendinfo_dict[temp_person])

            if two_level_friends_inter_have:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS " + DB_NAME +
                    ".u" + person +
                    "( uid CHAR(10) PRIMARY KEY, interfriends VARCHAR(5000)" + ")"
                )
                db.commit()
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS " + DB_NAME +
                    ".u" + temp_person +
                    "( uid CHAR(10) PRIMARY KEY, interfriends VARCHAR(5000)" + ")"
                )
                db.commit()

                temp_content = ", ".join(list(two_level_friends_inter_have))
                cur.execute("INSERT INTO " + DB_NAME +
                            ".u" + person +
                            " VALUES ('" + temp_person + "', '" + temp_content + "');")
                db.commit()
                cur.execute("INSERT INTO " + DB_NAME +
                            ".u" + temp_person +
                            " VALUES ('" + person + "', '" + temp_content + "');")
                db.commit()
                del temp_content

        count = count + 1

    del my_friendinfo_dict
    del friends_friendinfo_dict
    del two_level_useful_friends_list
    cur.close()
    db.close()

    """
    写入所有人的详细信息，除了上面计算的三个属性（因为已经写入）
    """
    print('log: every user info detail, may be long time, wait...')
    write_all_person_info_in_mysql(DB_NAME)

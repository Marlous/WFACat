# -*- coding: utf-8 -*-

"""
WFACatPro.get_data
~~~~~~~~~~~~~~~~~~~
This is a get_data module.
"""


import settings

import json
import os
import shutil
import random
import time
import requests
import urllib
from urllib.parse import urlparse


# 创建一个列表，用来保存已经下载过的人的好友信息
global uid_json_file_downloaded


def get_person_uid(person_name_params):
    """
    :param: 某个微博用户的用户名
    :return: 返回微博用户对应的 uid
    """
    """
    下载并保存自己的好友信息 person.json 文件（一度人脉）
    """
    person_info_json_file = requests.get(
        get_person_info_json_file_url(person_name_params))
    if person_info_json_file.status_code == requests.codes.ok:
        file_size = (len(person_info_json_file.content) / 1024)  # 计算文件大小并输出
        print('%s %.1f KB downloaded OK!' % ('person.json', file_size))
    else:
        person_info_json_file.raise_for_status()

    with open('./WFACat_data/temp/person.json', 'wb') as person_json_file_saved:  # 保存下载的文件到硬盘
        person_json_file_saved.write(person_info_json_file.content)
        person_json_file_saved.close()

    """
    提取 person 的 uid
    """
    with open('./WFACat_data/temp/person.json', 'r', encoding='utf-8') as person_json_file:
        json_file_trans = json.loads(
            person_json_file.read())  # 将 json 文件内容转为字典
        # 注意字典的索引可以是字符串或整数
        person_uid_local = json_file_trans['cards'][1]['card_group'][0]['user']['id']
        person_json_file.close()

    return person_uid_local


def get_person_info_json_file_url(person_name_params):
    """
    :param: 某个微博用户名称，在 settings 中的 person_name
    :return: 返回获取某个用户信息 json 文件的下载 url
    """

    # 需要研究的用户微博名字，经过两次编码，以便能在参数中使用
    temp_person_name = urllib.parse.quote(person_name_params)
    encoded_person_name = urllib.parse.quote(temp_person_name)

    # 拼接出 url
    url_local = 'https://api.weibo.cn/2/cardlist?' + \
                'aid=' + str(params['aid'])[2:-2] + \
                '&c=' + str(params['c'])[2:-2] + \
                '&containerid=100103type%253D3%2526q%253D' + encoded_person_name + \
                '&count=10' + \
                '&from=' + str(params['from'])[2:-2] + \
                '&gsid=' + str(params['gsid'])[2:-2] + \
                '&i=' + str(params['i'])[2:-2] + \
                '&lang=' + str(params['lang'])[2:-2] + \
                '&page=' + str(params['page'])[2:-2] + \
                '&s=' + str(params['s'])[2:-2] + \
                '&ua=' + str(params['ua'])[2:-2] + \
                '&v_p=' + str(params['v_p'])[2:-2]

    return url_local


def get_data_url(uid_params, page_params):
    """
    :param uid_params: 某个微博用户的 uid
    :param page_params: 页数。通过循环增加页数，下载到全部互关好友 json 文件
    :return: 返回获取某个用户的互关好友列表 json 文件的下载 url
    """

    params['count'] = settings.EACH_FOLLOWER_COUNT
    params['uid'] = uid_params
    params['page'] = page_params

    # 拼接出 url
    url_local = 'https://api.weibo.cn/2/friendships/bilateral?' + \
                'aid=' + str(params['aid'])[2:-2] + \
                '&c=' + str(params['c'])[2:-2] + \
                '&count=' + str(params['count']) + \
                '&from=' + str(params['from'])[2:-2] + \
                '&gsid=' + str(params['gsid'])[2:-2] + \
                '&i=' + str(params['i'])[2:-2] + \
                '&lang=' + str(params['lang'])[2:-2] + \
                '&page=' + str(params['page']) + \
                '&real_relationships=' + str(params['real_relationships'])[2:-2] + \
                '&s=' + str(params['s'])[2:-2] + \
                '&trim_status' + str(params['trim_status'])[2:-2] + \
                '&ua=' + str(params['ua'])[2:-2] + \
                '&uid=' + str(params['uid']) + \
                '&v_p=' + str(params['v_p'])[2:-2]
    return url_local


def download_user_json_file(user_uid_params, user_json_file_saved_path_params):
    """
    :param user_uid_params: 某一个用户的 uid
    :param user_json_file_saved_path_params: 将下载的此用户好友所有 json 文件保存的位置
    :return: 无返回值
    """
    user_uid = user_uid_params
    user_json_file_saved_path = user_json_file_saved_path_params

    page_count = 1
    while True:
        friends_info_json_file = requests.get(
            get_data_url(user_uid, page_count)
        )

        if friends_info_json_file.status_code == requests.codes.ok:
            file_size = (len(friends_info_json_file.content) / 1024)  # 计算文件大小并输出
            print('%s/%s.json %.1f KB downloaded OK!' % (
                user_json_file_saved_path, str(page_count), file_size))
        else:
            friends_info_json_file.raise_for_status()

        user_json_file_name = user_json_file_saved_path + '/' + str(page_count) + '.json'

        with open(user_json_file_name, 'wb') as f:  # 保存下载的文件到硬盘
            f.write(friends_info_json_file.content)

        with open(user_json_file_name, 'r', encoding='utf8') as f:  # 如果不含有用户信息，则这个 json 文件是最后一个不要的
            json_file_to_dict = json.loads(f.read())

        if json_file_to_dict['users']:  # 判断如果 users 下有用户信息则下载下一页，没有就跳出不下载下一页的 json 文件
            page_count = page_count + 1
            time.sleep(random.randint(1, 3))  # 随机停几秒，请求下一页的 json 文件
            continue
        else:
            break

    user_json_file_name_last = user_json_file_saved_path + '/' + str(page_count) + '.json'
    os.remove(user_json_file_name_last)  # 删除最后一个下载的用户信息为空的 json 文件
    print(user_json_file_name_last + ' deleted ~')

    # 记录此用户的好友信息 json 文件已下载
    uid_json_file_downloaded.append(user_uid)


def download_over_one_level_user_json_file():
    """
    :return: 无返回值。下载 n 度人脉全部用户的好友信息的 json 文件（默认一度人脉的信息文件已下载好）
    """
    if not os.path.exists('./WFACat_data/temp/1'):
        print('ERROR! ./WFACat_data/temp/1 not exists!')

    # 初始化人脉深度为 1，因为获得第一层人脉信息（以自己为种子）是预先下载，不使用此下载函数下载
    level_local = 1

    """
    遍历 n 个人脉文件夹
    想要继续遍历下一层，在本层给出下层遍历需要的本层文件列表
    """
    while level_local < settings.SET_LEVEL:
        next_level = int(level_local) + 1  # 创建下一度人脉文件夹，从文件夹 2 开始创建
        next_level_file_path = './WFACat_data/temp/' + str(next_level)
        if not os.path.exists(next_level_file_path):
            os.makedirs(next_level_file_path)

        level_file_path = './WFACat_data/temp/' + str(level_local)  # 某度人脉文件夹
        file_list = os.listdir(level_file_path)  # 某度文件夹中每个用户文件夹列表

        """
        遍历 n 度文件夹下的每个用户文件夹
        """
        for user_file_num in range(0, len(file_list)):
            user_file_name_path = './WFACat_data/temp/' + str(level_local) + '/' + file_list[user_file_num]  # 某用户文件夹
            user_file_list = os.listdir(user_file_name_path)  # 某用户文件夹中 json 列表

            """
            遍历每个用户文件夹中的每个以数字命名的 json 文件
            """
            for json_file_num in range(0, len(user_file_list)):
                json_file_name = user_file_name_path + '/' + user_file_list[json_file_num]

                """
                遍历每个 json 文件中的每个用户 uid，并下载其好友信息的 json 文件
                """
                with open(json_file_name, 'r', encoding='utf-8') as f:  # 打开一个 json 文件
                    # 将 json 文件内容转为字典，注意字典的索引可以是字符串或整数
                    json_file_to_dict = json.loads(f.read())

                    user_num_count = 0
                    # 开始提取遍历 json 中每个用户的 uid
                    for user_item in json_file_to_dict['users']:
                        user_uid = json_file_to_dict['users'][user_num_count]['id']
                        user_num_count = user_num_count + 1

                        # 判断是否已下载过该用户好友 json 文件
                        if user_uid not in uid_json_file_downloaded:
                            time.sleep(random.randint(5, settings.TIME_PAUSE_MAX))  # 随机暂停几秒，数字越大越安全
                            # 拼好用于存放其好友 json 文件的文件夹，以其 uid 命名
                            user_json_file_saved_path = next_level_file_path + '/' + str(user_uid)
                            os.makedirs(user_json_file_saved_path)

                            download_user_json_file(user_uid, user_json_file_saved_path)

        level_local = int(level_local) + 1  # 完成第 n 度人脉 json 文件下载


if __name__ == '__main__':
    # 创建一个列表，用来保存已经下载过的人的好友信息
    uid_json_file_downloaded = []

    print('= get data =')

    # 拆解设置的 privacy_url
    parsed = urlparse(settings.PRIVACY_URL)
    # 拆解请求参数
    params = urllib.parse.parse_qs(parsed.query)

    # 创建存放每个以用户 uid 命名的文件夹
    if os.path.exists('./WFACat_data/temp'):
        shutil.rmtree('./WFACat_data/temp')
        os.makedirs('./WFACat_data/temp')
    else:
        os.makedirs('./WFACat_data/temp')

    # 获取到 settings 中 person_name 微博用户对应的 uid
    person_uid = get_person_uid(settings.PERSON_NAME)
    print("%s\'s uid: %s" % (settings.PERSON_NAME, str(person_uid)))

    """
    根据 settings 中 person_name 微博用户对应的 uid
    下载并保存一度人脉信息的 json 文件。
    文件夹 1 中以其 uid 命名的文件夹，其中以数字 1 开始，若干个 json 文件（互关好友数多需要请求几个 page）
    """
    if not os.path.exists('./WFACat_data/temp/1'):
        os.makedirs('./WFACat_data/temp/1')

    # 创建研究对象用户文件夹，用于存放互关好友信息的 json 文件（json 以数字命名）
    user_json_file_saved_path = './WFACat_data/temp/1/' + str(person_uid)
    os.makedirs(user_json_file_saved_path)

    if person_uid not in uid_json_file_downloaded:
        download_user_json_file(person_uid, user_json_file_saved_path)

    # 下载 n 度人脉全部用户的好友信息的 json 文件，一度人脉的文件已下载好
    download_over_one_level_user_json_file()

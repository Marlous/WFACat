# -*- coding: utf-8 -*-

"""
WFACatPro.get_data
~~~~~~~~~~~~~~~~~~~
This is a get_data module.
"""


import json
import os
import shutil
import random
import time
import requests
import urllib
from urllib.parse import urlparse

import settings


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

    with open('./temp/person.json', 'wb') as person_json_file_saved:  # 保存下载的文件到硬盘
        person_json_file_saved.write(person_info_json_file.content)
        person_json_file_saved.close()

    """
    提取 person 的 uid
    """
    with open('./temp/person.json', 'r', encoding='utf-8') as person_json_file:
        json_file_trans = json.loads(
            person_json_file.read())  # 将 json 文件内容转为字典
        # 注意字典的索引可以是字符串或整数
        person_uid_local = json_file_trans['cards'][1]['card_group'][0]['user']['id']
        person_json_file.close()

    return person_uid_local


def get_data_url(uid_params):
    """
    :param: 某个微博用户的 uid
    :return: 返回获取某个用户的互关好友列表 json 文件的下载 url
    """

    params['count'] = settings.EACH_FOLLOWER_COUNT
    params['uid'] = uid_params

    # 拼接出 url
    url_local = 'https://api.weibo.cn/2/friendships/bilateral?' + \
                'aid=' + str(params['aid'])[2:-2] + \
                '&c=' + str(params['c'])[2:-2] + \
                '&count=' + str(params['count']) + \
                '&from=' + str(params['from'])[2:-2] + \
                '&gsid=' + str(params['gsid'])[2:-2] + \
                '&i=' + str(params['i'])[2:-2] + \
                '&lang=' + str(params['lang'])[2:-2] + \
                '&page=' + str(params['page'])[2:-2] + \
                '&real_relationships=' + str(params['real_relationships'])[2:-2] + \
                '&s=' + str(params['s'])[2:-2] + \
                '&trim_status' + str(params['trim_status'])[2:-2] + \
                '&ua=' + str(params['ua'])[2:-2] + \
                '&uid=' + str(params['uid']) + \
                '&v_p=' + str(params['v_p'])[2:-2]

    return url_local


def download_over_one_level_person_info_json_file():
    """
    :return: 无返回值。下载 n 度人脉全部用户的好友信息的 json 文件（默认一度人脉的信息文件已下载好）
    """
    if not os.path.exists('./temp/1'):
        print('ERROR! ./temp/1 not exists!')

    # 初始化人脉深度为 1，因为获得第一层人脉信息（以自己为种子）是预先下载，不使用此下载函数下载
    level_local = 1

    """
    遍历 n 个人脉文件夹（数字为几的文件夹存放几度人脉的 json 文件）
    """
    while level_local < settings.SET_LEVEL:
        file_path = './temp/' + str(level_local)  # 是已存在的一度人脉文件夹 1
        file_list = os.listdir(file_path)

        next_level = int(level_local) + 1  # 创建下一度人脉文件夹，从文件夹 2 开始
        next_file_path = './temp/' + str(next_level)
        if not os.path.exists(next_file_path):
            os.makedirs(next_file_path)

        for json_file_num in range(0, len(file_list)):  # 遍历 n 度文件夹下的 json 文件
            file_name = file_path + '/' + file_list[json_file_num]

            with open(file_name, 'r', encoding='utf-8') as one_json_file:  # 打开一个 json 文件
                # 将 json 文件内容转为字典，注意字典的索引可以是字符串或整数
                handle_json_file = json.loads(one_json_file.read())

                user_num_count = 0
                # 提取遍历 json 中每个用户的 uid
                for user_item in handle_json_file['users']:
                    user_uid = handle_json_file['users'][user_num_count]['id']
                    user_num_count = user_num_count + 1

                    # 判断是否已下载过该用户好友 json 文件
                    if user_uid not in uid_friends_info_json_file_downloaded:
                        time.sleep(random.randint(1, 10))  # 随机暂停几秒，数字越大越安全，但时间可能很长
                        time.sleep(random.randint(5, 10))

                        # 拼好将要下载的某用户好友信息文件要命名的名字（该用户 uid.json）
                        next_file_name = next_file_path + \
                            '/' + str(user_uid) + '.json'

                        friends_info_json_file = requests.get(
                            get_data_url(user_uid))
                        if friends_info_json_file.status_code == requests.codes.ok:
                            # 计算文件大小并输出
                            file_size = (
                                len(friends_info_json_file.content) / 1024)
                            print(
                                '%s %.1f KB downloaded OK!' %
                                (next_file_name, file_size))
                        else:
                            friends_info_json_file.raise_for_status()

                        with open(next_file_name, 'wb') as saved_file:  # 保存下载的文件到硬盘
                            saved_file.write(friends_info_json_file.content)
                        saved_file.close()

                        uid_friends_info_json_file_downloaded.append(
                            user_uid)  # 记录此 uid 已获取其好友关系

            one_json_file.close()

        level_local = int(level_local) + 1  # 完成第n度人脉 json 文件下载


if __name__ == '__main__':
    # 创建一个列表，用来保存已经下载过的人的好友信息
    uid_friends_info_json_file_downloaded = []

    # 拆解设置的 privacy_url
    parsed = urlparse(settings.PRIVACY_URL)
    # 拆解请求参数
    params = urllib.parse.parse_qs(parsed.query)
    # params['count'] = settings.each_follower_count
    #  将参数请求 count 设置为 settings 中的数值。好像不需要设置也可以获取到某个用户所有的互关好友信息

    # 创建存放好友信息 json 文件的文件夹
    if os.path.exists('./temp'):
        shutil.rmtree('./temp')
        os.makedirs('./temp')
    else:
        os.makedirs('./temp')

    # 获取到 settings 中 person_name 微博用户对应的 uid
    person_uid = get_person_uid(settings.PERSON_NAME)
    print("%s\'s uid: %s" % (settings.PERSON_NAME, str(person_uid)))

    """
    根据 settings 中 person_name 微博用户对应的 uid
    下载并保存一度人脉信息的 json 文件
    """
    if not os.path.exists('./temp/1'):
        os.makedirs('./temp/1')

    friends_info_json_file = requests.get(get_data_url(person_uid))
    if friends_info_json_file.status_code == requests.codes.ok:
        file_size = (len(friends_info_json_file.content) / 1024)  # 计算文件大小并输出
        print(
            './temp/1/%s.json %.1f KB downloaded OK!' %
            (str(person_uid), file_size))
    else:
        friends_info_json_file.raise_for_status()

    with open('./temp/1/' + str(person_uid) + '.json', 'wb') as f:  # 保存下载的文件到硬盘
        f.write(friends_info_json_file.content)
    f.close()

    # 记录此用户（配置中的微博用户，如自己）的好友信息 json 文件已下载
    uid_friends_info_json_file_downloaded.append(person_uid)

    # 下载 n 度人脉全部用户的好友信息的 json 文件，一度人脉的文件已下载好
    download_over_one_level_person_info_json_file()

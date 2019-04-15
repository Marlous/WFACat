# -*- coding: utf-8 -*-

"""
WFACatPro.tools
~~~~~~~~~~~~~~~~~~~
This is a tools module.
"""


from modules import settings

import json
import os
import shutil
import random
import time
import requests
import urllib
from urllib.parse import urlparse


def get_person_uid(person_name_params):
    """
    :param: 某个微博用户的用户名
    :return: 返回微博用户对应的 uid
    """
    """
    下载并保存研究对象的好友信息 person.json 文件（一度人脉）
    """
    person_info_json_file = requests.get(
        get_person_info_json_file_url(person_name_params))
    if person_info_json_file.status_code == requests.codes.ok:
        pass
    else:
        person_info_json_file.raise_for_status()

    with open('./WFACat_data/tools_query/person.json', 'wb') as person_json_file_saved:  # 保存下载的文件到硬盘
        person_json_file_saved.write(person_info_json_file.content)

    """
    提取 person 的 uid
    """
    with open('./WFACat_data/tools_query/person.json', 'r', encoding='utf-8') as person_json_file:
        json_file_trans = json.loads(
            person_json_file.read())  # 将 json 文件内容转为字典
        # 注意字典的索引可以是字符串或整数
        person_uid_local = json_file_trans['cards'][1]['card_group'][0]['user']['id']

    return person_uid_local


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


def get_person_detail_info_json_file_url(person_uid_params):
    """
    :param: 某个微博用户名称，在 settings 中的 person_name
    :return: 返回获取某个用户信息 json 文件的下载 url
    """

    # 拼接出 url
    url_local = 'https://api.weibo.cn/2/users/show?' + \
                'aid=' + str(params['aid'])[2:-2] + \
                '&c=' + str(params['c'])[2:-2] + \
                '&from=' + str(params['from'])[2:-2] + \
                '&gsid=' + str(params['gsid'])[2:-2] + \
                '&has_extend=1&has_profile=1' + \
                '&i=' + str(params['i'])[2:-2] + \
                '&lang=' + str(params['lang'])[2:-2] + \
                '&s=' + str(params['s'])[2:-2] + \
                '&ua=' + str(params['ua'])[2:-2] + \
                '&uid=' + str(person_uid_params) + \
                '&v_p=' + str(params['v_p'])[2:-2]

    return url_local


def download_user_json_file(person_uid_params):
    """
    :param: 某个微博用户的用户名
    :return: 返回微博用户对应的 uid
    """
    """
    下载并保存研究对象的好友信息 person.json 文件（一度人脉）
    """
    person_info_json_file = requests.get(
        get_person_detail_info_json_file_url(person_uid_params))
    if person_info_json_file.status_code == requests.codes.ok:
        pass
    else:
        person_info_json_file.raise_for_status()

    with open('./WFACat_data/tools_query/person.json', 'wb') as person_json_file_saved:  # 保存下载的文件到硬盘
        person_json_file_saved.write(person_info_json_file.content)


def download_user_friend_json_file(user_uid_params, user_json_file_saved_path_params):
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
            pass
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


def read_and_print_person_info():
    """
    所要查询的用户详细信息输出
    """
    ability_tags = ' '
    birthday = ' '
    email = ' '

    with open('./WFACat_data/tools_query/person.json', 'r', encoding='utf-8') as f:
        json_to_dict = json.loads(f.read())  # 将 json 文件内容转为字典
        # 注意字典的索引可以是字符串或整数
        uid = json_to_dict['id']
        name = json_to_dict['name']
        location = json_to_dict['location']
        description = json_to_dict['description']
        gender = json_to_dict['gender']
        followers_count = json_to_dict['followers_count']
        friends_count = json_to_dict['friends_count']
        statuses_count = json_to_dict['statuses_count']
        favourites_count = json_to_dict['favourites_count']
        created_at = json_to_dict['created_at']
        constellation = json_to_dict['constellation']
        verified_reason = json_to_dict['verified_reason']
        if 'ability_tags' in json_to_dict:
            ability_tags = json_to_dict['ability_tags']
        if 'birthday' in json_to_dict:
            birthday = json_to_dict['birthday']
        if 'email' in json_to_dict:
            email = json_to_dict['email']

    print('======== person info ========')
    print(person_name + ':')
    print('- uid: ' + str(uid))
    print('- name: ' + str(name))
    print('- location: ' + str(location))
    print('- description: ' + str(description))
    print('- gender: ' + str(gender))
    print('- followers_count: ' + str(followers_count))
    print('- friends_count: ' + str(friends_count))
    print('- statuses_count: ' + str(statuses_count))
    print('- favourites_count: ' + str(favourites_count))
    print('- created_at: ' + str(created_at))
    if verified_reason:
        print('- verified_reason: ' + str(verified_reason))
    if constellation:
        print('- constellation: ' + str(constellation))
    if ability_tags != ' ':
        print('- ability_tags: ' + str(ability_tags))
    if birthday != ' ':
        print('- birthday: ' + str(birthday))
    if email != ' ':
        print('- email: ' + str(email))


def read_and_print_person_mutual_info(person_uid_params):
    print('======== person mutual list ========')

    count = 0

    for item in os.listdir(user_json_file_saved_path):
        with open('./WFACat_data/tools_query/' + str(person_uid_params) + '/' + item, 'r', encoding='utf8') as f:
            json_to_dict = json.loads(f.read())

            user_num = 0
            for user_item in json_to_dict['users']:
                uid = json_to_dict['users'][user_num]['id']
                name = json_to_dict['users'][user_num]['name']
                location = json_to_dict['users'][user_num]['location']
                description = json_to_dict['users'][user_num]['description']
                gender = json_to_dict['users'][user_num]['gender']
                followers_count = json_to_dict['users'][user_num]['followers_count']
                friends_count = json_to_dict['users'][user_num]['friends_count']
                statuses_count = json_to_dict['users'][user_num]['statuses_count']
                created_at = json_to_dict['users'][user_num]['created_at'][-4:]

                user_num = user_num + 1

                print('uid: ' + str(uid) + ' / name: ' + str(name) + ' / location: ' + str(location) +
                      ' / description: ' + str(description) + ' / gender : ' + str(gender) +
                      ' / followers_count: ' + str(followers_count) + ' / friends_count: ' + str(friends_count) +
                      ' / statuses_count: ' + str(statuses_count) + ' / created_at: ' + str(created_at))
                print('')

                count = count + 1

    print('Friends sum count: ' + str(count))


if __name__ == '__main__':
    print('= tools =')

    # 拆解设置的 privacy_url
    parsed = urlparse(settings.PRIVACY_URL)
    # 拆解请求参数
    params = urllib.parse.parse_qs(parsed.query)

    # 创建存放每个以用户 uid 命名的文件夹
    if os.path.exists('./WFACat_data/tools_query'):
        shutil.rmtree('./WFACat_data/tools_query')
        os.makedirs('./WFACat_data/tools_query')
    else:
        os.makedirs('./WFACat_data/tools_query')

    # 用户输入所要查的微博用户名，得到其用户基本信息，并得到 uid
    person_name = input('Enter weibo user name that you want find: ')
    print('log: wait...')
    person_uid = get_person_uid(person_name)

    # 下载查询的某用户详细信息的 json 文件
    download_user_json_file(person_uid)

    # 创建研究对象用户文件夹，用于存放互关好友信息的 json 文件（json 以数字命名），并下载相关文件
    user_json_file_saved_path = './WFACat_data/tools_query/' + str(person_uid)
    os.makedirs(user_json_file_saved_path)

    download_user_friend_json_file(person_uid, user_json_file_saved_path)

    print('1 person info detail')
    print('2 person mutual friends info list')
    print('q exit tools module')

    while True:
        cmd = input('Enter to select:')
        if cmd == '1':
            read_and_print_person_info()
        elif cmd == '2':
            read_and_print_person_mutual_info(person_uid)
        elif cmd == 'q':
            exit()

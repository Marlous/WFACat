# -*- coding: utf-8 -*-

"""
WFACat Pro.settings
~~~~~~~~~~~~~~~~~~~
This is a setting module.
"""


import json
import os


"""
登陆手机微博客户端，打开抓包软件，点击所要查的用户的主页，点击粉丝 -> 点击相互关注，关闭抓包软件，
找出 含有 friendships 关键字的数据包，导出原始连接填入 privacy_url 后的值。
"""
global PRIVACY_URL

"""
所要研究的微博用户名
"""
global PERSON_NAME

"""
设置要获取的最大相互关注好友数量。根据新浪官方开发者手册：官方默认为 50，返回 30% 的互关好友，上限为 500。
不建议修改。
"""
global EACH_FOLLOWER_COUNT

"""
设置所要分析的人脉深度，建议研究二度人脉。深度增加，请求数据次数增加。
不建议修改。
"""
global SET_LEVEL


def print_config_info():
    with open('./config.json', 'r', encoding='utf-8') as config_file:
        config_file_handle = json.loads(config_file.read())
        privacy_url_local = config_file_handle['PRIVACY_URL']
        person_name_local = config_file_handle['PERSON_NAME']
        each_follower_count_local = config_file_handle['EACH_FOLLOWER_COUNT']
        set_level_local = config_file_handle['SET_LEVEL']

    print('= Settings =')
    print('PRIVACY_URL: ' + privacy_url_local)
    print('PERSON_NAME: ' + person_name_local)
    print('EACH_FOLLOWER_COUNT: ' + str(each_follower_count_local))
    print('SET_LEVEL: ' + str(set_level_local))


def write_config_file_privacy_url(privacy_url_params):
    if os.path.exists('./config.json'):
        config_file_in = open('./config.json', 'r', encoding='utf-8')
        config_file_handle_one = json.loads(config_file_in.read())
        config_file_in.close()

        config_file_handle_one['PRIVACY_URL'] = privacy_url_params
        config_file_handle_two = json.dumps(config_file_handle_one)

        config_file_out = open('./config.json', 'w', encoding='utf-8')
        config_file_out.write(config_file_handle_two)
        config_file_out.close()
    else:
        print('config.json not found!')


def write_config_file_person_name(person_name_params):
    if os.path.exists('./config.json'):
        config_file_in = open('./config.json', 'r', encoding='utf-8')
        config_file_handle_one = json.loads(config_file_in.read())
        config_file_in.close()

        config_file_handle_one['PERSON_NAME'] = person_name_params
        config_file_handle_two = json.dumps(config_file_handle_one)

        config_file_out = open('./config.json', 'w', encoding='utf-8')
        config_file_out.write(config_file_handle_two)
        config_file_out.close()
    else:
        print('config.json not found!')


"""
读取配置文件
"""
with open('config.json', 'r', encoding='utf-8') as config_file:
    config_file_handle = json.loads(config_file.read())
    PRIVACY_URL = config_file_handle['PRIVACY_URL']
    PERSON_NAME = config_file_handle['PERSON_NAME']
    EACH_FOLLOWER_COUNT = int(config_file_handle['EACH_FOLLOWER_COUNT'])
    SET_LEVEL = config_file_handle['SET_LEVEL']


if __name__ == '__main__':
    print_config_info()

    values = input('Do you want to modify settings ?[Y/N]')
    while values not in ('Y', 'N'):
        values = input('Please enter Y or N:')

    if values == 'Y':
        select_one = input('Setting privacy url (should use weibo account to analysis data packages on your mobile phone.[Y/N])')
        while select_one not in ('Y', 'N'):
            select_one = input('Please enter Y or N:')
        if select_one == 'Y':
            privacy_url_local = input('Enter:')
            write_config_file_privacy_url(privacy_url_local)

        select_two = input('Setting weibo name (who you want to analysis).[Y/N]')
        while select_two not in ('Y', 'N'):
            select_two = input('Please enter Y or N:')
        if select_two == 'Y':
            person_name_local = input('Enter:')
            write_config_file_person_name(person_name_local)

        print_config_info()
        exit()
    elif values == 'N':
        print('Settings no changed !')
        exit()

# -*- coding: utf-8 -*-

"""
WFACatPro.settings
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
设置要获取的最大相互关注好友数量。
单页只能获得 200，（json 文件），可以通过构造参数的页数来请求全部的
如果某个好友（研究对象的好友）的互关数超过 200 人，那么会导致此好友的相关分析信息可能会不准确！
不建议修改。
"""
global EACH_FOLLOWER_COUNT

"""
设置所要分析的人脉深度，建议研究二度人脉。深度增加，请求数据次数增加。
不建议修改。
"""
global SET_LEVEL


"""
MySQL 相关参数
"""
global DB_HOST
global DB_PORT
global DB_USER
global DB_USER_PASSWORD
global DB_CHARSET


"""
在 get_data.py 中下载某用户好友信息的随机最大的暂停时间（范围从 5 到设置的秒数）
"""
global TIME_PAUSE_MAX
TIME_PAUSE_MAX = 15


def print_config_info():
    with open('./WFACat_data/config.json', 'r', encoding='utf-8') as config_file:
        config_file_handle = json.loads(config_file.read())
        privacy_url_local = config_file_handle['PRIVACY_URL']
        person_name_local = config_file_handle['PERSON_NAME']
        each_follower_count_local = config_file_handle['EACH_FOLLOWER_COUNT']
        set_level_local = config_file_handle['SET_LEVEL']
        db_host_local = config_file_handle['DB_HOST']
        db_port_local = config_file_handle['DB_PORT']
        db_user_local = config_file_handle['DB_USER']
        db_user_password_local = config_file_handle['DB_USER_PASSWORD']
        db_charset_local = config_file_handle['DB_CHARSET']

    print('= Settings =')
    print('PRIVACY_URL: ' + privacy_url_local)
    print('PERSON_NAME: ' + person_name_local)
    print('EACH_FOLLOWER_COUNT: ' + str(each_follower_count_local))
    print('SET_LEVEL: ' + str(set_level_local))
    print('DB_HOST: ' + db_host_local)
    print('DB_PORT: ' + str(db_port_local))
    print('DB_USER: ' + db_user_local)
    print('DB_USER_PASSWORD: ' + db_user_password_local)
    print('DB_CHARSET: ' + db_charset_local)


def write_config_file_privacy_url(privacy_url_params):
    if os.path.isfile('./WFACat_data/config.json'):
        config_file_in = open('./WFACat_data/config.json', 'r', encoding='utf-8')
        config_file_handle_one = json.loads(config_file_in.read())
        config_file_in.close()

        config_file_handle_one['PRIVACY_URL'] = privacy_url_params
        config_file_handle_two = json.dumps(config_file_handle_one)

        config_file_out = open('./WFACat_data/config.json', 'w', encoding='utf-8')
        config_file_out.write(config_file_handle_two)
        config_file_out.close()
    else:
        print('config.json not found!')


def write_config_file_person_name(person_name_params):
    if os.path.isfile('./WFACat_data/config.json'):
        config_file_in = open('./WFACat_data/config.json', 'r', encoding='utf-8')
        config_file_handle_one = json.loads(config_file_in.read())
        config_file_in.close()

        config_file_handle_one['PERSON_NAME'] = person_name_params
        config_file_handle_two = json.dumps(config_file_handle_one)

        config_file_out = open('./WFACat_data/config.json', 'w', encoding='utf-8')
        config_file_out.write(config_file_handle_two)
        config_file_out.close()
    else:
        print('config.json not found!')


def write_config_file_db_info(db_host_params, db_port_params, db_user_params, db_charset_params):
    if os.path.isfile('./WFACat_data/config.json'):
        config_file_in = open('./WFACat_data/config.json', 'r', encoding='utf-8')
        config_file_handle_one = json.loads(config_file_in.read())
        config_file_in.close()

        config_file_handle_one['DB_HOST'] = db_host_params
        config_file_handle_one['DB_PORT'] = db_port_params
        config_file_handle_one['DB_USER'] = db_user_params
        config_file_handle_one['DB_CHARSET'] = db_charset_params
        config_file_handle_two = json.dumps(config_file_handle_one)

        config_file_out = open('./WFACat_data/config.json', 'w', encoding='utf-8')
        config_file_out.write(config_file_handle_two)
        config_file_out.close()
    else:
        print('config.json not found!')


def write_config_file_db_passwd(db_user_password_params):
    if os.path.isfile('./WFACat_data/config.json'):
        config_file_in = open('./WFACat_data/config.json', 'r', encoding='utf-8')
        config_file_handle_one = json.loads(config_file_in.read())
        config_file_in.close()

        config_file_handle_one['DB_USER_PASSWORD'] = db_user_password_params
        config_file_handle_two = json.dumps(config_file_handle_one)

        config_file_out = open('./WFACat_data/config.json', 'w', encoding='utf-8')
        config_file_out.write(config_file_handle_two)
        config_file_out.close()
    else:
        print('config.json not found!')


"""
读取配置文件
"""
if os.path.isfile('./WFACat_data/config.json'):
    with open('./WFACat_data/config.json', 'r', encoding='utf-8') as config_file:
        config_file_handle = json.loads(config_file.read())
        PRIVACY_URL = config_file_handle['PRIVACY_URL']
        PERSON_NAME = config_file_handle['PERSON_NAME']
        EACH_FOLLOWER_COUNT = int(config_file_handle['EACH_FOLLOWER_COUNT'])
        SET_LEVEL = config_file_handle['SET_LEVEL']
        DB_HOST = config_file_handle['DB_HOST']
        DB_PORT = int(config_file_handle['DB_PORT'])
        DB_USER = config_file_handle['DB_USER']
        DB_USER_PASSWORD = config_file_handle['DB_USER_PASSWORD']
        DB_CHARSET = config_file_handle['DB_CHARSET']


if __name__ == '__main__':
    print_config_info()

    values = input('Do you want to modify settings ?[Y/N]')
    while values not in ('Y', 'N'):
        values = input('Please enter Y or N:')

    if values == 'Y':
        select_one = input(
            'Setting privacy url (should use weibo account to analysis data packages on your mobile phone.[Y/N])')
        while select_one not in ('Y', 'N'):
            select_one = input('Please enter Y or N:')
        if select_one == 'Y':
            privacy_url_local = input('Enter privacy url: ')
            write_config_file_privacy_url(privacy_url_local)

        select_two = input(
            'Setting weibo name (who you want to analysis).[Y/N]')
        while select_two not in ('Y', 'N'):
            select_two = input('Please enter Y or N:')
        if select_two == 'Y':
            person_name_local = input('Enter weibo name: ')
            write_config_file_person_name(person_name_local)

        select_three = input(
            'Setting DB host, port, user, charset (Default: localhost, 3306, root, utf8mb4).[Y/N]')
        while select_three not in ('Y', 'N'):
            select_three = input('Please enter Y or N:')
        if select_three == 'Y':
            db_host_local = input('Enter host: ')
            db_port_local = input('Enter port: ')
            db_user_local = input('Enter user: ')
            db_charset_local = input('Enter charset:')
            write_config_file_db_info(
                db_host_local,
                db_port_local,
                db_user_local,
                db_charset_local)

        select_four = input('Setting DB user password).[Y/N]')
        while select_four not in ('Y', 'N'):
            select_four = input('Please enter Y or N:')
        if select_four == 'Y':
            db_user_password_local = input('Enter user password: ')
            write_config_file_db_passwd(db_user_password_local)

        print_config_info()
        exit()

    elif values == 'N':
        print('Settings no changed !')
        exit()

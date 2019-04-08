# -*- coding: utf-8 -*-

"""
WFACatPro.main
~~~~~~~~~~~~~~~~~~~
This is a main module.
"""


import json
import os

import settings
import version


if __name__ == '__main__':
    version.print_version_info()
    print('You could use \'help\' command to get help!')
    print('If appear Python ERROR, please config correct configuration!')

    """
    第一次运行没有配置文件，会自动初始化一个 config.json
    """
    if not os.path.exists('config.json'):
        with open('config.json', 'w', encoding='utf-8') as init_config_info_json_file:
            privacy_url_local = ' '
            person_name_local = ' '
            each_follower_count_local = 200
            set_level_local = 2

            init_config_info = {
                'PRIVACY_URL': privacy_url_local,
                'PERSON_NAME': person_name_local,
                'EACH_FOLLOWER_COUNT': each_follower_count_local,
                'SET_LEVEL': set_level_local}
            init_config_info_handle = json.dumps(init_config_info)
            init_config_info_json_file.write(init_config_info_handle)

    """
    每次运行，判断是否进行了配置
    """
    if settings.PRIVACY_URL == ' ':
        print('No configuration! Please setting! using command \'conf\' !')
    elif settings.PERSON_NAME == ' ':
        print('No configuration! Please setting! using command \'conf\' !')

    """
    接受命令并运行对应的模块
    """
    while True:
        cmd = input('> ')
        if cmd == 'help':
            os.system('help.py')
        elif cmd == 'conf':
            os.system('settings.py')
        elif cmd == 'get':
            os.system('get_data.py')
        elif cmd == 'store':
            os.system('analysis_to_csv.py')
        elif cmd == 'quit':
            exit('Bye ~')

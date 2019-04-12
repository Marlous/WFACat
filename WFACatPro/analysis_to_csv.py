# -*- coding: utf-8 -*-

"""
WFACatPro.analysis_store_data
~~~~~~~~~~~~~~~~~~~
This is a analysis store data module.
"""


import settings

import csv
import json
import os


def save_all_person_info_json_file_as_csv():
    level_local = 1

    """
    遍历 n 个人脉文件夹
    想要继续遍历下一层，在本层给出下层遍历需要的本层文件列表
    """
    while level_local <= settings.SET_LEVEL:
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

            document_file_name = file_list[user_file_num]  # file_name 是存用户好友信息 json 的文件夹名，即其 uid

            """
            遍历每个用户文件夹中的每个以数字命名的 json 文件
            """
            for json_file_num in range(0, len(user_file_list)):
                json_file_name = user_file_name_path + '/' + user_file_list[json_file_num]

                """
                遍历每个 json 文件中的每个用户 uid，将信息写入 csv 文件
                """
                with open(json_file_name, 'r', encoding='utf-8') as f:  # 打开一个 json 文件
                    # 将 json 文件内容转为字典，注意字典的索引可以是字符串或整数
                    json_file_to_dict = json.loads(f.read())

                    user_num_count = 0
                    # 开始提取遍历 json 中每个用户的 uid、name
                    for user_item in json_file_to_dict['users']:
                        user_uid = json_file_to_dict['users'][user_num_count]['id']
                        user_name = json_file_to_dict['users'][user_num_count]['name']
                        user_num_count = user_num_count + 1

                        # 判断是否已记录过该用户
                        if user_uid not in node_list:
                            with open('./WFACat_data/data/node.csv', 'a', newline='') as f_node:
                                node_csv_file = csv.writer(f_node)
                                node_one_data = []  # 将两个变量数据组成列表
                                node_one_data.append(user_uid)
                                node_one_data.append(user_name)
                                node_csv_file.writerow(node_one_data)
                            node_list.append(user_uid)
                            print('node: ' + str(user_uid) + ': ' + user_name)

                        with open('./WFACat_data/data/edge.csv', 'a', newline='') as f_edge:
                            edge_csv_file = csv.writer(f_edge)
                            edge_one_data = []
                            edge_one_data.append(document_file_name)  # 存 json 的文件夹名
                            edge_one_data.append(user_uid)
                            edge_one_data.append(level_local)
                            edge_csv_file.writerow(edge_one_data)

                        print('edge: ' + file_list[json_file_num][0:10] +
                              ' -> ' + str(user_uid) +
                              '( ' + user_name + ' )')

        level_local = int(level_local) + 1  # 完成第 n 度人脉 json 文件信息写入

    print('')
    print('Congratulations! All data analysis completed!')
    print('node.csv and edge.csv you had now ~ You can find it in ./WFACat_data/data')
    print('Thanks!')


if __name__ == '__main__':
    print('= Data analysis =')
    values = input('Do you want to start or restart data analysis ?[Y/N]')
    while values not in ('Y', 'N'):
        values = input('Please enter Y or N:')

    if values == 'Y':
        if not os.path.exists('./WFACat_data/temp'):
            print('ERROR! Please use \' get \' command to get data first!')

        # 记录已经写入 csv 的节点，避免重复写入
        global node_list
        node_list = []

        if os.path.exists('./WFACat_data/data'):
            os.remove('./WFACat_data/data/node.csv')
            os.remove('./WFACat_data/data/edge.csv')
        else:
            # 创建用于存放 csv 文件的 data 目录（存放节点、边文件供 Gephi 数据可视化软件分析）
            os.makedirs('./WFACat_data/data')

        """
        创建节点、边的文件给可视化软件分析（初始化文件，接下来会这两个文件中写数据）
        """
        with open('./WFACat_data/data/node.csv', 'a', newline='') as f:
            csv_file = csv.writer(f)
            csv_file.writerow(['id', 'label'])

        with open('./WFACat_data/data/edge.csv', 'a', newline='') as f:
            csv_file = csv.writer(f)
            csv_file.writerow(['source', 'target', 'weight'])

        """
        先将研究对象的节点写入 node.csv
        """
        with open('./WFACat_data/temp/person.json', 'r', encoding='utf-8') as person_json_file:
            json_file_trans = json.loads(person_json_file.read())
            person_uid_local = json_file_trans['cards'][1]['card_group'][0]['user']['id']
        person_uid = person_uid_local

        with open('./WFACat_data/data/node.csv', 'a', newline='') as f_node:
            node_csv_file = csv.writer(f_node)
            node_one_data = []  # 将两个变量数据组成列表
            node_one_data.append(person_uid)
            node_one_data.append(settings.PERSON_NAME)
            node_csv_file.writerow(node_one_data)
        node_list.append(person_uid)
        print('node: ' + str(person_uid) + ': ' + settings.PERSON_NAME)

        """
        遍历保存所有 json 文件中需要的信息到 csv 文件
        """
        save_all_person_info_json_file_as_csv()

    elif values == 'N':
        print('Thanks!')

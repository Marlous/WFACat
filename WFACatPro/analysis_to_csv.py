# -*- coding: utf-8 -*-

"""
WFACat Pro.analysis_store_data
~~~~~~~~~~~~~~~~~~~
This is a analysis_store_data module.
"""


import csv
import json
import os

import settings


def save_all_person_info_json_file_as_csv():
    # 遍历 n 度（n 个）人脉文件夹中所有
    level_local = 1

    while level_local <= settings.SET_LEVEL:
        file_path = './temp/' + str(level_local)
        file_list = os.listdir(file_path)  # 第 n 度文件夹路径

        # 遍历 n 度文件夹下的 json 文件
        for json_file_num in range(0, len(file_list)):
            file_name = file_path + '/' + \
                file_list[json_file_num]  # 文件夹下的每一个 json 文件

            with open(file_name, 'r', encoding='utf-8') as one_json_file:  # 提取遍历 json 中每个用户的 uid
                # 将 json 文件内容转为字典，注意字典的索引可以是字符串或整数
                handle_json_file = json.loads(one_json_file.read())

                user_num = 0
                for user_item in handle_json_file['users']:
                    # 提取用户的 uid
                    user_uid = str(handle_json_file['users'][user_num]['id'])
                    user_name = handle_json_file['users'][user_num]['name']
                    user_num = user_num + 1

                    if user_uid not in node_list:
                        with open('./data/node.csv', 'a', newline='') as f1:
                            node_csv_file = csv.writer(f1)
                            node_one_data = []  # 将两个变量数据组成列表
                            node_one_data.append(user_uid)
                            node_one_data.append(user_name)
                            node_csv_file.writerow(node_one_data)
                        node_list.append(user_uid)
                        print('node: ' + str(user_uid) + ': ' + user_name)

                    with open('./data/edge.csv', 'a', newline='') as f2:
                        edge_csv_file = csv.writer(f2)
                        edge_one_data = []
                        edge_one_data.append(
                            file_list[json_file_num][0:10])  # 文件名
                        edge_one_data.append(user_uid)
                        edge_one_data.append(level_local)
                        edge_csv_file.writerow(edge_one_data)

                    print('edge: ' +
                          file_list[json_file_num][0:10] +
                          ' -> ' +
                          str(user_uid) +
                          '( ' +
                          user_name +
                          ' )')

            one_json_file.close()

        level_local = int(level_local) + 1

    print('')
    print('Congratulations! All data analysis completed!')
    print('node.csv and edge.csv you had now ~ You can find it in ./data')
    print('Thanks!')


if __name__ == '__main__':
    print('= Data analysis =')
    values = input('Do you want to start or restart data analysis ?[Y/N]')
    while values not in ('Y', 'N'):
        values = input('Please enter Y or N:')

    if values == 'Y':
        if not os.path.exists('./temp'):
            print('ERROR! Please use \' get \' command to get data first!')

        # 记录已经写入 csv 的节点，避免重复写入
        node_list = []

        if os.path.exists('./data'):
            os.remove('./data/node.csv')
            os.remove('./data/edge.csv')
        else:
            # 创建用于存放 csv 文件的 data 目录（存放节点、边文件供 Gephi 数据可视化软件分析）
            os.makedirs('./data')

        """
        创建节点、边的文件给可视化软件分析
        """
        with open('./data/node.csv', 'a', newline='') as f:
            csv_file = csv.writer(f)
            csv_file.writerow(['id', 'label'])

        with open('./data/edge.csv', 'a', newline='') as f:
            csv_file = csv.writer(f)
            csv_file.writerow(['source', 'target', 'weight'])

        """
        将 settings 中的 person_name 用户的 uid 和 微博名写入节点文件
        """
        person_json_file_path = os.listdir('./temp/1')
        # 即取一度人脉的文件名。uid 全部处理为字符串
        person_uid_local = str(person_json_file_path[0][0:10])

        with open('./data/node.csv', 'a', newline='') as f:
            node_csv_file = csv.writer(f)
            node_one_data = []  # 将两个变量数据组成列表
            node_one_data.append(person_uid_local)
            node_one_data.append(settings.PERSON_NAME)
            print(node_one_data)
            node_csv_file.writerow(node_one_data)

        print('node: ' + str(person_uid_local) + settings.PERSON_NAME)

        node_list.append(person_uid_local)

        # 遍历保存所有 json 文件中需要的信息到 csv 文件
        save_all_person_info_json_file_as_csv()

    elif values == 'N':
        print('Thanks!')

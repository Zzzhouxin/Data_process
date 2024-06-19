import json
import os
import re
import pickle

import nltk
from nltk import word_tokenize

from utils import get_part_1, get_part_2, get_part_3
from bs4 import BeautifulSoup


def reduce_banner_list(probe_data):
    """
    读取pure_dscan_result.json数据
    返回未处理的响应特征和标签
    """
    dscan_list = []
    product = probe_data["product"]

    if len(probe_data["banner_list"]) > 1:
        dscan_list = []
        for banner_num in probe_data["banner_list"]:
            dscan_list.append(banner_num)
            # print(banner_num["req_name"])

    return dscan_list, product


def process_data(dscan_list, type=None):
    """
    输入为一条深度探测数据
    返回值
    """
    attribute = []

    for i in range(len(dscan_list)):
        part1_data = get_part_1(dscan_list[i])
        part2_data = get_part_2(dscan_list[i])
        part3_data = get_part_3(dscan_list[i])

        for j in range(len(part2_data)):
            if part2_data[j][:5] == "Date:":
                part2_data[j] = "Data: DATE"

        part3_data = BeautifulSoup(part3_data, 'html.parser')
        part3_data = word_tokenize(part3_data.get_text())
        part3_data = str(" ").join(part3_data)

        attribute.append({
            "part1": part1_data,
            "part2": part2_data,
            "part3": part3_data
        })

    return attribute


def get_status_code(dscan_list):
    """
    提取状态码
    """
    return dscan_list['part1'][9:12]


def bool_hasServer(dscan_list, product):
    """
    返回方法中是否存在Server服务器字段
    """
    flag1, flag2 = False, False

    # 检查关键字字段有没有出现过Server
    for i in range(len(dscan_list['part2'])):
        if dscan_list['part2'][i][:7] == 'Server:':
            flag1 = True
            break

    # 用正则去匹配html文本中有没有出现过Server字段 / 检查body字段有没有出现web容器名称
    # pattern = re.compile('(?<=\\r\\nServer: ).*?.(?=\\r\\n)')
    # result = pattern.search(dscan_list['part3'])
    # print(result)
    # if result:
    #     flag2 = True
    if dscan_list['part3'].find(product) != -1:
        flag2 = True

    return flag1 or flag2


def bool_hasVersion(dscan_list, version):
    flag1, flag2 = False, False
    if version == 'no_version':
        return False

    for item in dscan_list['part2']:
        if version in item:
            flag1 = True

    if dscan_list['part3'].find(version) != -1:
        flag2 = True

    return flag1 or flag2


if __name__ == "__main__":

    # 读取文件数据
    all_json = os.listdir('./process_pip/pure_data/')
    all_json.sort()
    for _ in all_json:
        if _[:4] != 'pure':
            all_json.remove(_)
    print(all_json)

    # 全局初始化一个三维的数组，数组的每一行为一种web容器（版本），每一列为探测载荷编号，每一个值为[status_code, 是否出现Server， 是否出现版本]
    array_3d = []
    # 全局初始化一个dict，保存product和行号直接的映射关系
    product_dict = dict()

    for json_file in all_json:
        print("@INFO：   正在处理：  " + json_file)
        pure_jsonData = open('./process_pip/pure_data/' + json_file, 'r', encoding='utf-8')
        for line in pure_jsonData:
            pure_jsonData = json.loads(line)
            version = pure_jsonData['version']

            # 数据预处理
            dscan_list, product = reduce_banner_list(pure_jsonData)
            dscan_list = process_data(dscan_list)  # 把数据用正则表达式拆分，去掉网页上现实的html文本标签

            # 更新product_dict索引
            if product not in product_dict.keys():
                val = len(product_dict)
                product_dict[product] = val

            # 声明一个空的容器
            container = []
            container.append(product)

            # num_rows表示每个容器中的行数
            for j in range(len(dscan_list)):
                # 替换为实际的状态码、server和version值
                row = {
                    'status_code': get_status_code(dscan_list[j]),
                    'hasServer': bool_hasServer(dscan_list[j], product),
                    'hasVersion': bool_hasVersion(dscan_list[j], version)
                }
                container.append(row)

            # 将容器添加到三维数组中
            array_3d.append(container)

            # 保存数组结果到本地

    with open('./process_pip/select_probe_temp/array_3d.pkl', 'wb') as file:
        pickle.dump(array_3d, file)
    print("数组保存成功！")

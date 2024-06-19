"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2023/12/5 16:49
# @Author  : zhouxin
# @FileName: test2.py
# @Software: PyCharm
===========================
"""
import json

from utils import get_part_1, get_part_2, get_part_3

with open('./pure_data.json', 'r', encoding='utf-8') as f1:
    with open('./train_text2.json', 'a+', encoding='utf-8') as f2:

        for line in f1:
            attribute = []
            line_data = json.loads(line)
            for i in range(len(line_data["banner_list"])):
                attribute.append({
                    # str(line_data["banner_list"][i]["req_name"]): {
                    'part1': get_part_1(line_data["banner_list"][i]),
                    'part2': get_part_2(line_data["banner_list"][i]),
                    'part3': get_part_3(line_data["banner_list"][i])
                    # }
                })

            att_data = {
                'ip': line_data["ip"],
                'attribute': attribute,
                'production': line_data['product'],
                'version': line_data['version']
            }
            f2.write(json.dumps(att_data, ensure_ascii=False))
            f2.write('\n')
        f2.close()
    f1.close()
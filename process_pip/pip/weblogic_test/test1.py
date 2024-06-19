"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2023/12/5 16:44
# @Author  : zhouxin
# @FileName: test1.py
# @Software: PyCharm
===========================
"""
import json

with open("dscan_output.json", mode='r', encoding='utf-8') as f1:
    for line in f1:
        line_data = json.loads(line)

        # 检查有没有http_server_detect_list字段
        try:
            banner_count = len(line_data['port_list'][0]['dscan_data']['http_server_detect_list'])
        except:
            continue

        if banner_count > 1:
            try:
                """
                用for循环判断端口和嵌套太麻烦了
                先用原来写的这个方法偷懒一下
                有时间把这里重写成用正则匹配指定的字段结构
                参考链接：https://juejin.cn/post/6994404313380421669
                """
                if len(line_data['port_list']) == 1:
                    http_server_detect_list_data = line_data['port_list'][0]['dscan_data']['http_server_detect_list']
                    for i in range(len(line_data['port_list'][0]['app_list'])):
                        _type = line_data['port_list'][0]['app_list'][i]['type']
                        _product = line_data['port_list'][0]['app_list'][i]['product']

                        if line_data['port_list'][0]['app_list'][i]["version_start"] != "":
                            _version = line_data['port_list'][0]['app_list'][i]["version_start"]
                        else:
                            _version = "no_version"

                        if _type == "WebContainer":
                            break

                elif len(line_data['port_list']) == 2:
                    http_server_detect_list_data = line_data['port_list'][1]['dscan_data'][
                        'http_server_detect_list']

                    for i in range(len(line_data['port_list'][0]['app_list'])):
                        _type = line_data['port_list'][0]['app_list'][i]['type']
                        _product = line_data['port_list'][0]['app_list'][i]['product']

                        if line_data['port_list'][0]['app_list'][i]["version_start"] != "":
                            _version = line_data['port_list'][0]['app_list'][i]["version_start"]
                        else:
                            _version = "no_version"

                        if _type == "WebContainer":
                            break
            except:
                print('@INFO: dscan_list不存在')
                pass

            data_lines = {
                'ip': line_data['ip'],
                'banner_list': http_server_detect_list_data,
                'product': _product,
                'version': _version
            }

            with open("pure_data.json", mode='a+', encoding='utf-8') as f2:
                f2.write(json.dumps(data_lines, ensure_ascii=False))
                f2.write('\n')
    f1.close()
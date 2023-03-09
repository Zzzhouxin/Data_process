import json

with open('/data/zhouxin/Data_process/process_pip/pure_data/http_server.json', mode='r', encoding='utf-8') as f1:
# with open(dscan_file, mode='r', encoding='utf-8') as f1:
    for line in f1:
        line_data = json.loads(line)
        banner_list = []

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
                    for j in range(len(line_data['port_list'][0]['dscan_data']['http_server_detect_list'])):
                        for k in range(len(line_data['port_list'][0]['app_list'])):
                            _type = line_data['port_list'][0]['app_list'][k]['type']
                            _product = line_data['port_list'][0]['app_list'][k]['product']
                            if line_data['port_list'][0]['app_list'][k]["version_start"] != "":
                                _version = line_data['port_list'][0]['app_list'][k]["version_start"]
                            else:
                                _version = "no_version"

                            if _type == "WebContainer":
                                banner_list.append(line_data['port_list'][0]['dscan_data']
                                                   ['http_server_detect_list'][j])

                elif len(line_data['port_list']) == 2:
                    for j in range(len(line_data['port_list'][1]['dscan_data']['http_server_detect_list'])):
                        for k in range(len(line_data['port_list'][0]['app_list'])):
                            _type = line_data['port_list'][0]['app_list'][k]['type']

                            if _type == "WebContainer":
                                banner_list.append(line_data['port_list'][1]['dscan_data']
                                                   ['http_server_detect_list'][j])

            except:
                print('@INFO: dscan_list不存在')
                pass

            data_lines = {
                'ip': line_data['ip'],
                'banner_list': banner_list,
                'product': _product,
                'version': _version
            }

            with open('./process_pip/pip/pure_httpserver.json', mode='a+', encoding='utf-8') as f2:
            # with open('./process_pip/pure_data/pure.json', mode='a+', encoding='utf-8') as f2:
                f2.write(json.dumps(data_lines, ensure_ascii=False))
                f2.write('\n')
f1.close()
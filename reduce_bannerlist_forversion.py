import os

import json

data_dir = '/data/zhouxin/database/'


def reduce_bannerlist_forversion(product):
    """
    选取某一种web容器进行分类
    :return:
    """

    data_collletlist = []
    item = dict()

    for filename in os.listdir(data_dir):
        data_collletlist.append(data_dir + filename)

    data_collletlist.sort()
    print(data_collletlist)

    for data_path in data_collletlist:
        with open(data_path, 'r', encoding='utf-8') as f1:
            for line in f1:
                line_data = json.loads(line)
                try:
                    if line_data['port_list'][0]['app_list']:
                        for i in range(len(line_data['port_list'][0]['app_list'])):
                            _type = line_data['port_list'][0]['app_list'][i]['type']
                            _product = line_data['port_list'][0]['app_list'][i]['product']
                            if line_data['port_list'][0]['app_list'][i]["version_start"] != "":
                                _version = line_data['port_list'][0]['app_list'][i]["version_start"]
                            else:
                                _version = "no_version"

                            if 'WebContainer' == _type and product == _product:
                                with open("./process_pip/pure_data/http_server.json", mode="a+", encoding='utf-8') as f2:
                                    f2.write(json.dumps(line_data))
                                    f2.write('\n')
                                f2.close()

                                if _version not in item:
                                    item[_version] = 1
                                else:
                                    item[_version] += 1

                except:
                    pass

            f1.close()

    print("### bannrlist整理结束 ###")
    print(json.dumps(item, indent=4))


if __name__ == '__main__':

    reduce_bannerlist_forversion("http server")
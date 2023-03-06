import os

import json

pure_data_dir = './process_pip/pure_data/'


def reduce_bannerlist():
    """
    筛选我们需要的深度探索特征，去掉其他无用的数据字段
    :return:
    """

    data_collletlist = []
    item = dict()
    input_items = ["http server", "nginx", 'iis', "lighttpd", 'micro httpd', 'boa', 'rompager', 'jetty']

    for filename in os.listdir(pure_data_dir):
        if filename[:4] == "pure":
            data_collletlist.append(pure_data_dir + filename)

    data_collletlist.sort()
    print(data_collletlist)

    for data_path in data_collletlist:
        with open(data_path, mode='r', encoding='utf-8') as f1:
            print("正在处理: " + data_path)
            with open("./process_pip/pip/train_text.json", 'a+', encoding='utf-8') as f2:
                for line in f1:
                    data = json.loads(line)
                    _product = data["product"]

                    if _product in input_items:
                        if _product not in item.keys():
                            item[_product] = 0
                        elif item[_product] < 30000:
                            dscan_list = []
                            banner_list = [0, 6, 19, 21, 40, 72, 87, 261, 272]
                            for banner_num in banner_list:
                                try:
                                    dscan_list.append(data["banner_list"][banner_num])
                                except:
                                    print("dscan数据为空")
                            data_line = {
                                'ip': data['ip'],
                                'banner_list': dscan_list,
                                'product': data['product']
                            }

                            f2.write(json.dumps(data_line, ensure_ascii=False))
                            item[_product] += 1
                            f2.write('\n')
                        else:
                            pass
                    else:
                        pass
                f2.close()
            f1.close()

    print("### bannrlist整理结束 ###")
    print(json.dumps(item, indent=4))


if __name__ == '__main__':

    reduce_bannerlist()
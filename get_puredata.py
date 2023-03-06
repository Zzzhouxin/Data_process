import json
import os
import shutil

from utils import iter_count, wc_count

base_dir = '/home/zhouxin/'
database_dir = base_dir + 'Kafka/database/'
process_pip_dir = base_dir + 'Data_process/process_pip'

database_list = os.listdir(database_dir)

# database_list = ['/Users/zhouxin/所有文件/研一下/KafkaOutput/dscan_result.json']
database_list.sort()


def list_database():
    """
    返回数据库中每次探测结果有多少条值
    :return:
    """
    dscan_sum = 0

    for dscan_file in database_list:
        sum = wc_count(database_dir + dscan_file)
        print('"文件名为："{filename}， 数据条数为： {data}'.format(filename=dscan_file, data=sum))
        dscan_sum += sum
    print('数据总数为：{sum}'.format(sum=dscan_sum))


def get_puredata():
    """
    将深度探测模型扫描完成的数据去掉无关字段
    按照IP + banner_list + product的格式储存为新的pure_data
    :return:
    """
    if len(os.listdir('/data/zhouxin/Data_process/process_pip/pure_data')) != 0:
        """
        判断pure_data文件夹是否为空，如果不为空，删除原pure_data
        重新生成pure_data
        """
        shutil.rmtree('/data/zhouxin/Data_process/process_pip/pure_data', ignore_errors=True)
        print('pure_data文件夹已被清空')
        os.mkdir('/data/zhouxin/Data_process/process_pip/pure_data')
    else:
        print("pure_data文件夹为空")

    for dscan_file in database_list:
        with open(database_dir + dscan_file, mode='r', encoding='utf-8') as f1:
        # with open(dscan_file, mode='r', encoding='utf-8') as f1:
            print("@正在处理 " + dscan_file + " 文件！")
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

                                    if _type == "WebContainer":
                                        banner_list.append(line_data['port_list'][0]['dscan_data']
                                                           ['http_server_detect_list'][j])

#                                     if line_data['port_list'][0]['app_list'][k]["version_start"] != "":
#                                         _version = line_data['port_list'][0]['app_list'][k]["version_start"]
#                                     else:
#                                         _version = "no_version"

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
                        'product': _product
                    }

                    with open(process_pip_dir + '/pure_data/pure_' + dscan_file, mode='a+', encoding='utf-8') as f2:
                    # with open('./process_pip/pure_data/pure.json', mode='a+', encoding='utf-8') as f2:
                        f2.write(json.dumps(data_lines, ensure_ascii=False))
                        f2.write('\n')
        f1.close()


if __name__ == '__main__':

    # list_database()

    get_puredata()
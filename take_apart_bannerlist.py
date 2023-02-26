from utils import get_part_1, get_part_2, get_part_3
import json


def take_apart_bannerlist():
    """
    把每个bannerlist里的数据，根据正则表达式拆解成状态码，关键字，body字段三部分
    :return:
    """

    with open('./process_pip/pip/train_text.json', 'r', encoding='utf-8') as f1:
        with open('./process_pip/pip/train_text2.json', 'a+', encoding='utf-8') as f2:

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
                    'production': line_data['product']
                }
                f2.write(json.dumps(att_data, ensure_ascii=False))
                f2.write('\n')
            f2.close()
        f1.close()


if __name__ == '__main__':
    take_apart_bannerlist()
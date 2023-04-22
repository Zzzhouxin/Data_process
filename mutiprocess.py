import json
from multiprocessing import Pool


def count_labels(json_str):
    data = json.loads(json_str)
    return data['production']


def process_file(filename):
    with open(filename, encoding='utf-8') as f:
        json_list = list(f)

    with Pool() as p:
        labels = p.map(count_labels, json_list)

    label_dict = {}
    for label in labels:
        if label in label_dict:
            label_dict[label] += 1
        else:
            label_dict[label] = 1

    return label_dict


if __name__ == '__main__':
    filename = './process_pip/pip/train_text3.json'
    label_dict = process_file(filename)
    print(label_dict)

import pickle

with open('./process_pip/select_probe_temp/array_3d.pkl', "rb") as file:
    loaded_array = pickle.load(file)

product_dict = dict()

# 声明一个概率矩阵，用来计算出现Server的概率
probability_matrix = []

# 打印加载的数组
for row in loaded_array:
    product = row[0]

    # 更新product_dict 保存当前读取到了哪些类型的容器
    # 读到一个新web容器
    if product not in product_dict:
        _ = len(product_dict)
        product_dict[product] = _

        new_row = []
        new_row.append(row[0])
        for i in range(1, len(row)):
            dict_temp = {}
            if row[i]['hasServer']:
                dict_temp.update({'hasServer': 1})
            elif not row[i]['hasServer']:
                dict_temp.update({'hasServer': 0})

            if row[i]['hasVersion']:
                dict_temp.update({'hasVersion': 1})
            else:
                dict_temp.update({'hasVersion': 0})

            dict_temp.update({'sum': 1})
            new_row.append(dict_temp)

        probability_matrix.append(new_row)

    # 读取到一个已有的web容器
    else:
        for i in range(1, len(row)):
            if row[i]['hasServer']:
                probability_matrix[product_dict[product]][i]['hasServer'] += 1
            if row[i]['hasVersion']:
                probability_matrix[product_dict[product]][i]['hasVersion'] += 1

            probability_matrix[product_dict[product]][i]['sum'] += 1

print('@INFO:   数据统计结束')

for row in probability_matrix:
    for i in range(1, len(row)):
        Server_percentage = (row[i]['hasServer'] / row[i]['sum'] * 100)
        Version_percentage = (row[i]['hasVersion'] / row[i]['sum'] * 100)
        row[i] = {
            'hasServer_probability': f"{Server_percentage:.2f}%",
            'hasVersion_probability': f"{Version_percentage:.2f}%"
        }


with open('./process_pip/select_probe_temp/probability_matrix.pkl', 'wb') as file:
    pickle.dump(probability_matrix, file)

print('@INFO:   概率更新结束')
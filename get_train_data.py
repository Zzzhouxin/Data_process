import json


def get_train_txt():
    with open("./process_pip/pip/train_text3.json", 'r', encoding='utf-8') as f1:
        for line in f1:
            text = []

            line_data = json.loads(line)
            attribute_data = line_data["attribute"]
            for i in range(len(attribute_data)):
                # 添加part1
                text.append(attribute_data[i]["part1"])
                # 添加part2
                for j in range(len(attribute_data[i]["part2"])):
                    text.append(attribute_data[i]["part2"][j])

                text.append(attribute_data[i]["part3"])

            if str(text):
                """
                这里要判断特征是否为空
                """
                with open('./process_pip/pip/result.csv', 'a+', encoding='utf-8') as f2:
                    f2.write(" ".join(text).replace(',', " ") + ',' + line_data["version"] + '\n')
                f2.close()
            else:
                print("dscan特征为空")

        f1.close()


if __name__ == "__main__":
    get_train_txt()
# -*- coding: utf-8 -*-
import json
import re


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
                    f2.write(" ".join(text).replace(',', " ") + ',' + line_data["production"] + '\n')
                f2.close()
            else:
                print("dscan特征为空")

        f1.close()


def text_filter():
    text = "A  �A  .�A  P�A  u�A     \�A   �          �   ��� BaseException� @    �  �      �   ��� HelpContext\�A    �          �   ���InnerException� @    �  �      �    ��Message� @  �B           �    �� StackTrace  @    �          �   ��� StackInfo   ��A              �A     ��A     �A     4�A 0� @  8� @  ��B p� @  �� @  �� @  �� @  �� @  �� @  Ȃ @  ��B  ` �B �B      EArgumentException    �A EArgumentException��A \�A   System.SysUtils         ��A             ��A     ��A     ��A     ��"
    filtered_text = re.sub(r'[^\u4E00-\u9FA5\uF900-\uFA2D\u0020-\u007F\uFF00-\uFFEF\u2000-\u206F]', '', text)

    print(filtered_text)
    # 输出：Hello，world！你好，世界！12345 #@%$。


if __name__ == "__main__":
    # get_train_txt()
    text_filter()

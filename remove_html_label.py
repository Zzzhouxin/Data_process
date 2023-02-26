import json
from bs4 import BeautifulSoup
from nltk import word_tokenize


def remov_html_label():
    """
    将一些时间类型的数据写成通用宏定义
    去除part3中的html有关标签
    :return:
    """
    with open('./process_pip/pip/train_text2.json', 'r+', encoding='utf-8') as f1:
        with open('./process_pip/pip/train_text3.json', 'a+', encoding='utf-8') as f2:
            for line in f1:
                if line:
                    line_data = json.loads(line)
                    attribute_data = line_data["attribute"]
                    """
                    Date字段把值去掉
                    """
                    for i in range(len(attribute_data)):
                        part2_data = attribute_data[i]["part2"]
                        for j in range(len(part2_data)):
                            if part2_data[j][:5] == "Date:":
                                part2_data[j] = "Data: DATE"
                            if part2_data[j][:15] == "Content-Length:":
                                part2_data[j] = "Content-Length: CONTENT-LENGTH"
                            if part2_data[j][:14] == "Last-Modified:":
                                part2_data[j] = "Last-Modified: LAST-MODIFIED"
                            if part2_data[j][:5] == "ETag:":
                                part2_data[j] = "ETag: ETAG"
                            if part2_data[j][:14] == "Content-Range:":
                                part2_data[j] = "Content-Range: CONTENT-RANGE"

                    """         
                    去掉part3的html标签
                    """
                    for i in range(len(attribute_data)):
                        """
                            Todo 标记
                        """
                        part3_data = attribute_data[i]["part3"]
                        part3_data = BeautifulSoup(part3_data, 'html.parser')
                        part3_data = word_tokenize(part3_data.get_text())
                        attribute_data[i]["part3"] = str(" ").join(part3_data)

                    f2.write(json.dumps(line_data, ensure_ascii=False))
                    f2.write('\n')
            f2.close()
        f1.close()


if __name__ == '__main__':
    remov_html_label()
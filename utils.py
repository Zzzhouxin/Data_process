def iter_count(file_name):
    """
    高性能读取大文件的行数
    :param file_name:
    :return:
    """
    from itertools import (takewhile, repeat)
    buffer = 1024 * 1024
    with open(file_name, 'r', encoding='utf-8') as f:
        buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
        return sum(buf.count('\n') for buf in buf_gen)


def wc_count(file_name):
    """
    通过系统调用wc命令读取文件的行数
    :param file_name:
    :return:
    """
    import subprocess
    out = subprocess.getoutput("wc -l %s" % file_name)
    return int(out.split()[0])


def get_part_1(banner_data):
    try:
        s_test = banner_data["banner"].split("\r\n\r\n")[1]
        s = banner_data["banner"].split("\r\n\r\n")[0]
        s = s.split('\r\n')[0]
        if s[:4] == 'HTTP':
            return s
        else:
            return ''
    except:
        return ''


def get_part_2(banner_data):
    try:
        # 检测是否只有part3
        s_test = banner_data["banner"].split("\r\n\r\n")[1]
        # 将前两部分提取
        s1 = banner_data["banner"].split("\r\n\r\n")[0]
        s = s1.split('\r\n')[0]
        # 检测是否有第一部分
        if s[:4] == 'HTTP':
            return s1.split('\r\n')[1:]
        else:
            return s1.split('\r\n')
    except:
        return ''


def get_part_3(banner_data):
    try:
        s = banner_data["banner"].split("\r\n\r\n")[1]
        if s:
            return s
        else:
            return ''
    except:
        return banner_data["banner"]



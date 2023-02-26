from collections import Counter


def word_segmentation(strings):
    '''
        利用结巴工具对文本进行分词，并返回单词的权重.
    '''
    # 分词，返回一个单词列表
    # tokens = jieba.lcut(strings)
    tokens = strings.split(' ')

    # 计算每个单词的权值(使用词频)
    weights_dcit = dict(Counter(tokens))

    return tokens, weights_dcit


class Simhash(object):

    # 初始化函数
    def __init__(self, weights_dict, tokens='', hashbits=128):
        self.hashbits = hashbits
        self.hash = self.simhash_function(tokens, weights_dict)

    # toString函数
    def __str__(self):
        return str(self.hash)

    # 给每一个单词生成对应的hash值
    def _string_hash(self, source):
        if source == '':
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** self.hashbits - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            return x

    # 生成simhash值
    def simhash_function(self, tokens, weights_dict):
        v = [0] * self.hashbits
        for key, t in {x: self._string_hash(x) for x in tokens}.items():
            for i in range(self.hashbits):
                bitmask = 1 << i
                if t & bitmask:
                    v[i] += weights_dict[key]
                else:
                    v[i] -= weights_dict[key]

        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i
        return fingerprint

    # 求文档间的海明距离
    def hamming_distance(self, other):
        x = (self.hash ^ other.hash) & ((1 << self.hashbits) - 1)
        tot = 0
        while x:
            tot += 1
            x &= x - 1
        return tot

    # 求相似度
    def similarity(self, other):
        a = float(self.hash)
        b = float(other.hash)
        if a > b:
            return b / a
        else:
            return a / b


if __name__ == '__main__':
    # s1 = '404 Not Found 404 Not Found nginx HTTP/1.1 505 HTTP Version Not Supported Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 505 HTTP Version Not Supported 505 HTTP Version Not Supported nginx HTTP/1.1 200 OK Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Last-Modified: LAST-MODIFIED Connection: close Vary: Accept-Encoding ETag: ETAG Accept-Ranges: bytes 没有找到站点 没有找到站点 您的请求在Web服务器中没有找到对应的站点！ 可能原因： 您没有将此域名或IP绑定到对应站点 ! 配置文件未生效 ! 如何解决： 检查是否已经绑定到对应站点，若确认已绑定，请尝试重载Web服务； 检查端口是否正确； 若您使用了CDN产品，请尝试清除CDN缓存； 普通网站访客，请联系网站管理员； HTTP/1.1 416 Requested Range Not Satisfiable Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close Vary: Accept-Encoding Content-Range: CONTENT-RANGE 416 Requested Range Not Satisfiable 416 Requested Range Not Satisfiable nginx HTTP/1.1 400 Bad Request Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close  HTTP/1.1 404 Not Found Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close  HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed nginx HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed nginx HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed nginx,nginx'
    # tokens1, weights_dcit1 = word_segmentation(s1)
    # hash1 = Simhash(weights_dict=weights_dcit1, tokens=tokens1)
    #
    # s2 = '301 Moved Permanently 301 Moved Permanently nginx HTTP/1.1 505 HTTP Version Not Supported Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close X-Default-Vhost: 1 505 HTTP Version Not Supported 505 HTTP Version Not Supported nginx HTTP/1.1 301 Moved Permanently Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close Location: https:/// X-Default-Vhost: 1 301 Moved Permanently 301 Moved Permanently nginx HTTP/1.1 301 Moved Permanently Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close Location: https:/// X-Default-Vhost: 1 301 Moved Permanently 301 Moved Permanently nginx HTTP/1.1 400 Bad Request Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close X-Default-Vhost: 1  HTTP/1.1 301 Moved Permanently Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close Location: https:///asdfg.hjkl X-Default-Vhost: 1  HTTP/1.1 301 Moved Permanently Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close Location: https:/// X-Default-Vhost: 1 301 Moved Permanently 301 Moved Permanently nginx HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close X-Default-Vhost: 1 405 Not Allowed 405 Not Allowed nginx HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close X-Default-Vhost: 1 405 Not Allowed 405 Not Allowed nginx,'
    # tokens2, weights_dcit2 = word_segmentation(s2)
    # hash2 = Simhash(weights_dict=weights_dcit2, tokens=tokens2)
    #
    # s3 = '404 Not Found 404 Not Found nginx HTTP/1.1 505 HTTP Version Not Supported Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 505 HTTP Version Not Supported 505 HTTP Version Not Supported nginx HTTP/1.1 200 OK Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Last-Modified: LAST-MODIFIED Connection: close Vary: Accept-Encoding ETag: ETAG Accept-Ranges: bytes 没有找到站点 没有找到站点 您的请求在Web服务器中没有找到对应的站点！ 可能原因： 您没有将此域名或IP绑定到对应站点 ! 配置文件未生效 ! 如何解决： 检查是否已经绑定到对应站点，若确认已绑定，请尝试重载Web服务； 检查端口是否正确； 若您使用了CDN产品，请尝试清除CDN缓存； 普通网站访客，请联系网站管理员； HTTP/1.1 416 Requested Range Not Satisfiable Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close Vary: Accept-Encoding Content-Range: CONTENT-RANGE 416 Requested Range Not Satisfiable 416 Requested Range Not Satisfiable nginx HTTP/1.1 400 Bad Request Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close  HTTP/1.1 404 Not Found Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close  HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed nginx HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed nginx HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed nginx'
    # tokens3, weights_dcit3 = word_segmentation(s3)
    # hash3 = Simhash(weights_dict=weights_dcit3, tokens=tokens3)
    #
    # s4 = '416 Not Found 404 Not Found nginx HTTP/1.1 505 HTTP Version Not Supported Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 505 HTTP Version Not Supported 505 HTTP Version Not Supported nginx HTTP/1.1 200 OK Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Last-Modified: LAST-MODIFIED Connection: close Vary: Accept-Encoding ETag: ETAG Accept-Ranges: bytes 没有找到站点 没有找到站点 您的请求在Web服务器中没有找到对应的站点！ 可能原因： 您没有将此域名或IP绑定到对应站点 ! 配置文件未生效 ! 如何解决： 检查是否已经绑定到对应站点，若确认已绑定，请尝试重载Web服务； 检查端口是否正确； 若您使用了CDN产品，请尝试清除CDN缓存； 普通网站访客，请联系网站管理员； HTTP/1.1 416 Requested Range Not Satisfiable Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close Vary: Accept-Encoding Content-Range: CONTENT-RANGE 416 Requested Range Not Satisfiable 416 Requested Range Not Satisfiable nginx HTTP/1.1 400 Bad Request Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close  HTTP/1.1 404 Not Found Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close  HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed nginx HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed nginx HTTP/1.1 405 Not Allowed Server: nginx Data: DATE Content-Type: text/html Content-Length: CONTENT-LENGTH Connection: close 405 Not Allowed 405 Not Allowed iis'
    # tokens4, weights_dcit4 = word_segmentation(s4)
    # hash4 = Simhash(weights_dict=weights_dcit4, tokens=tokens4)
    #
    # print(hash1.hamming_distance(hash2), "   ", hash1.similarity(hash2))
    # print(hash1.hamming_distance(hash3), "   ", hash1.similarity(hash3))
    # print(hash3.hamming_distance(hash4), "   ", hash3.similarity(hash4))

    Golab_simHash_value = []
    with open('./process_pip/pip/result.csv', mode='r', encoding='utf-8') as f:
        for line in f:

            try:
                text, label = line.split(',')
            except:
                print(line)
            text = text.strip()
            label = label.replace("\n", "")
            _token, _weights_dict = word_segmentation(text)
            _hash = Simhash(weights_dict=_weights_dict, tokens=_token)

            if len(Golab_simHash_value) == 0:
                Golab_simHash_value.append(_hash)

            else:
                for i, item in enumerate(Golab_simHash_value):
                    if _hash.hamming_distance(item) <= 5:   # 重复的样本
                        print("重复的数据")
                        break
                    elif i == len(Golab_simHash_value)-1:
                        Golab_simHash_value.append(_hash)
                        print("待添加的数据")

                        with open('./process_pip/pip/sim_hash_result.csv', 'a+', encoding='utf-8') as f2:
                            f2.write(line.strip())
                            f2.write('\n')
                        f2.close()

        f.close()
# encoding=utf-8
import socket,re,urllib,zlib,requests,redis
import config.config as conf
import supermo.core.common as com
from bs4 import BeautifulSoup
from supermo.core.get_ua import UA
from supermo.core.mysqldb import mysqldb

redis = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT, password=conf.REDIS_PASSWORD, decode_responses=True)

flag = "创意新鲜事"  # 自定义要搜索的内容


class deepspider():
    def __init__(self,project_name, homepage):
        # 初始化当前抓取的深度
        self.crawl_deepth = conf.CRAWL_DEEPTH
        self.current_deepth = 1
        self.project_name = project_name
        self.homepage = homepage

        deepspider.redis_cralw = str(self.project_name + "cralw")
        deepspider.redis_queue = str(self.project_name + "queue")
        redis.sadd(deepspider.redis_queue,homepage)
        # print(self.homepage)
        self.crawling(self.homepage)

    # 抓取过程主函数
    def crawling(self,homepage):
        # 循环条件：抓取深度不超过crawl_deepth
        while self.current_deepth <= self.crawl_deepth:
            # 循环条件：待抓取的链接不空
            print(self.UrlsEnmpy())
            print(int(redis.scard(deepspider.redis_queue)))
            while self.UrlsEnmpy():
                # 队头url出队列
                visitUrl = redis.spop(deepspider.redis_queue)
                if visitUrl is None or visitUrl == "":
                    continue
                # 将url放入已访问的url中 redis_cralw 数据库
                redis.sadd(deepspider.redis_cralw, com.md5_url(visitUrl))
                print(visitUrl)
                print(self.current_deepth)
                # 获取超链接
                links = self.getHyperLinks(visitUrl, homepage)
            # 未访问的url入列
            for link in links:
                redis.sadd(deepspider.redis_cralw,link)
                # print(link)
            self.current_deepth += 1

    # 获取源码中得超链接
    def getHyperLinks(self, url, static_url):
        result = []
        r = requests.get(url)
        data = r.text
        # lines = data.split("\n")
        # for i in lines:
        #     if flag in i:
        #         print(url + "" + i)
        # 利用正则查找所有连接
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", data)
        for i in link_list:
            if "http" not in i:
                result.append(static_url + i)
            else:
                result.append(i)
        return result
    # 判断未访问的url队列是否为空
    def UrlsEnmpy(self):
        return int(redis.scard(deepspider.redis_queue)) > 0

    # 获取网页源码
    def getPageSource(self, url, timeout=100, coding=None):
        try:
            socket.setdefaulttimeout(timeout)
            req = urllib.request(url)
            req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
            response = urllib.urlopen(req)
            page = ''
            if response.headers.get('Content-Encoding') == 'gzip':
                page = zlib.decompress(page, 16 + zlib.MAX_WBITS)

            if coding is None:
                coding = response.headers.getparam("charset")
                # 如果获取的网站编码为None
            if coding is None:
                page = response.read()
                # 获取网站编码并转化为utf-8
            else:
                page = response.read()
                page = page.decode(coding).encode('utf-8')
            return ["200", page]
        except Exception as e:
            print(str(e))
            return [str(e), None]


# class linkQuence:
#     def __init__(self):
#         # 已访问的url集合
#         self.visted = []
#         # 待访问的url集合
#         self.unVisited = []
#
#     # 获取访问过的url队列
#     def getVisitedUrl(self):
#         return self.visted
#
#     # 获取未访问的url队列
#     def getUnvisitedUrl(self):
#         return self.unVisited
#
#     # 添加到访问过得url队列中
#     def addVisitedUrl(self, url):
#         self.visted.append(url)
#
#     # 移除访问过得url
#     def removeVisitedUrl(self, url):
#         self.visted.remove(url)
#
#     # 未访问过得url出队列
#     def unVisitedUrlDeQuence(self):
#         try:
#             return self.unVisited.pop()
#         except:
#             return None
#
#     # 保证每个url只被访问一次
#     def addUnvisitedUrl(self, url):
#         if url != "" and url not in self.visted and url not in self.unVisited:
#             self.unVisited.insert(0, url)
#
#     # 获得已访问的url数目
#     def getVisitedUrlCount(self):
#         return len(self.visted)
#
#     # 获得未访问的url数目
#     def getUnvistedUrlCount(self):
#         return len(self.unVisited)
#
#     # 判断未访问的url队列是否为空
#     def unVisitedUrlsEnmpy(self):
#         return len(self.unVisited) == 0


# def main(seeds, crawl_deepth, static_url):
#     # print(seeds)
#     # print(static_url)
#     craw = MyCrawler(seeds)
#     craw.crawling(seeds, crawl_deepth, static_url)
#
#
# if __name__ == "__main__":
#     for i in urls:
#         main([i], depth, i)
#     print("Done!")
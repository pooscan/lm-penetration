# encoding=utf-8
import socket,re,urllib,zlib,requests
import config.config as conf

from supermo.core.get_ua import UA
from supermo.core.mysqldb import mysqldb


flag = "创意新鲜事"  # 自定义要搜索的内容

# from supermo.core.domain_deep_spider import deepspider
# deepspider('iwithb','http://www.iwithb.com')

class deepspider():
    def __init__(self,project_name, homepage):
        # 初始化当前抓取的深度
        self.crawl_deepth = conf.CRAWL_DEEPTH
        self.current_deepth = 1
        self.homepage   =   homepage
        self.visted = []
        self.unVisited = []
        if isinstance(homepage, str):
            self.addUnvisitedUrl(homepage)
        if isinstance(homepage, list):
            for i in homepage:
                self.addUnvisitedUrl(i)
        # print(self.homepage)
        self.crawling(self.homepage)
    # 抓取过程主函数
    def crawling(self,homepage):
        # 循环条件：抓取深度不超过crawl_deepth
        while self.current_deepth <= self.crawl_deepth:
            # 循环条件：待抓取的链接不空
            print(self.unVisitedUrlsEnmpy())
            while not self.unVisitedUrlsEnmpy():
                # 队头url出队列
                visitUrl = self.unVisitedUrlDeQuence()
                if visitUrl is None or visitUrl == "":
                    continue
                links = self.getHyperLinks(visitUrl, homepage)
                print(visitUrl)
                print(self.current_deepth)
                self.addVisitedUrl(visitUrl)
            # 未访问的url入列
            for link in links:
                self.addUnvisitedUrl(link)
            self.current_deepth += 1

    # 获取源码中得超链接
    def getHyperLinks(self, url, static_url):
        result = []
        r = requests.get(url)
        data = r.text
        lines = data.split("\n")
        # for i in lines:
        #     if flag in i:
        #         print(url + "" + i)
        # 利用正则查找所有连接, 这里还差找相同的url
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", data)
        for i in link_list:
            if "http" not in i:
                result.append(static_url + i)
            else:
                result.append(i)
        return result


    # 获取网页源码
    def getPageSource(self, url, timeout=100, coding=None):
        try:
            socket.setdefaulttimeout(timeout)
            req = urllib.request(url)
            req.add_header('User-agent', UA().getPCUA())
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


    def getVisitedUrl(self):
        return self.visted

    def getUnvisitedUrl(self):
        return self.unVisited

    def addVisitedUrl(self, url):
        self.visted.append(url)

    def removeVisitedUrl(self, url):
        self.visted.remove(url)

    def unVisitedUrlDeQuence(self):
        try:
            return self.unVisited.pop()
        except:
            return None

    def addUnvisitedUrl(self, url):
        if url != "" and url not in self.visted and url not in self.unVisited:
            self.unVisited.insert(0, url)

    def getVisitedUrlCount(self):
        return len(self.visted)

    # 获得未访问的url数目
    def getUnvistedUrlCount(self):
        return len(self.unVisited)

    def unVisitedUrlsEnmpy(self):
        return len(self.unVisited) == 0
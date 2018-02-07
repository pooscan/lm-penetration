import requests,threading
import urllib.request,random
from supermo.core.get_agent import IPFactory as IPP
from supermo.core.get_ua import UA
from bs4 import BeautifulSoup
# import random
# http://1212.ip138.com/ic.asp
def _get(url,proxy):
    try:
        header = {'User-Agent':UA().getPCUA()}
        # proxy_support = urllib.request.ProxyHandler({'http': proxy})
        # opener = urllib.request.build_opener(proxy_support)
        # urllib.request.install_opener(opener)
        # req = urllib.request.Request(url=url, headers=header)
        # html = urllib.request.urlopen(req, timeout=5)
        # bsObj = BeautifulSoup(html, "lxml")
        # return bsObj.center
        p = {'http': 'http://' + proxy}
        return requests.get(url, headers=header, proxies=p, timeout=5).text
    except Exception as e:
        print(e)
# def html_parser()
def testip():
    useful_proxies = {}
    max_failure_times = 3
    try:
        # 获取代理IP数据
        for ip in IPP().get_proxies():
            useful_proxies[ip] = 0
        print("总共：" + str(len(useful_proxies)) + 'IP可用')
    except OSError:
        print ("获取代理ip时出错！")
    i = 0
    while i < 10:
        # 设置随机代理
        proxy = random.choice(list(useful_proxies.keys()))
        print("change proxies: " + proxy)
        content = ''
        try:
            content = _get("http://ip.chinaz.com/getip.aspx", proxy)
        except OSError:
            # 超过3次则删除此proxy
            useful_proxies[proxy] += 1
            if useful_proxies[proxy] > 3:
                useful_proxies.remove(proxy)
            # 再抓一次
            proxy = random.choice(useful_proxies.keys())
            content = _get("http://ip.chinaz.com/getip.aspx ", proxy)
        # raw_text = html_parser(content)
        print(content)
        i = i + 1
        print(i)
def word():
    time.sleep(1)
    print("123")
    print(time.time())
def create_workers():
    for _ in range(20):
        t = threading.Thread(target=word())
        t.daemon = True
        t.start()
# create_workers()
# testip()
IPP().start()
# IPP().create_workers()
# print(_get("http://1212.ip138.com/ic.asp", "153.36.131.188:808"))

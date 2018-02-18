#!/usr/bin/python
# coding:utf-8
# Author:se55i0n
# 目标tcp端口开放扫描及应用端口banner识别
# myscan = Scanner("www.iwithb.com", 1, 10000)
# myscan.check_target()


import sys
import socket
import logging
import requests
import dns.resolver
from time import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 线程池
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Lock

# reload(sys)
# sys.setdefaultencoding('utf-8')
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)


class portscan(object):
    def __init__(self, target, start, end):
        self.target = target
        self.start = start
        self.end = end
        self.W = '\033[0m'
        self.G = '\033[1;32m'
        self.O = '\033[1;33m'
        self.R = '\033[1;31m'
        self.time = time()
        self.ports = []
        self.result = []
        self.mutex = Lock()
        self.get_ports()
        self.check_target()

    def get_ports(self):
        for i in range(int(self.start), int(self.end) + 1):
            self.ports.append(i)

    def check_cdn(self):
        # 目标域名cdn检测
        myResolver = dns.resolver.Resolver()
        myResolver.lifetime = myResolver.timeout = 2.0
        dnsserver = [['114.114.114.114'], ['8.8.8.8'], ['223.6.6.6']]
        try:
            for i in dnsserver:
                myResolver.nameservers = i
                record = myResolver.query(self.target)
                self.result.append(record[0].address)
        except Exception as e:
            pass
        finally:
            return True if len(set(list(self.result))) > 1 else False

    def scan_port(self, port):
        # 端口扫描
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            return True if s.connect_ex((self.target, port)) == 0 else False
        except Exception as e:
            pass
        finally:
            s.close()

    def get_http_banner(self, url):
        # http/https请求获取banner
        try:
            r = requests.get(url, headers={'UserAgent': UserAgent().random}, timeout=2, verify=False,
                             allow_redirects=True)
            soup = BeautifulSoup(r.content, 'lxml')
            return soup.title.text.strip('\n').strip()
        except Exception as e:
            pass

    def get_socket_info(self, port):
        # socket获取banner
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((self.target, port))
            s.send(b"alibaba")
            return s.recv(1024)
            s.close()
        # return s.recv(1024).split('\r\n')[0].strip('\r\n')
        except Exception as e:
            pass
        finally:
            s.close()

    def run(self, port):
        try:
            if self.scan_port(port):
                banner = self.get_http_banner('http://{}:{}'.format(self.target, port))
                self.mutex.acquire()
                if banner:
                    print(banner[:18])
                    print('[+] {} ---- open   {}'.format(str(port).rjust(6), ))
                else:
                    banner = self.get_http_banner('https://{}:{}'.format(self.target, port))
                    if banner:
                        # print(str(port).rjust(6))
                        # print(banner[:18])
                        print('[+] {} ---- open   {}{}'.format(str(port).rjust(6), banner[:18], self.W))
                    else:
                        banner = self.get_socket_info(port)
                        if banner:
                            print(str(port).rjust(6))
                            print(banner[:18])
                            # print("222")
                        # print('[+] {} ---- open   {}{}'.format( str(port).rjust(6), banner[:18], self.W))
                        else:
                            print('[+] {} ---- open   {}'.format(str(port).rjust(6), self.W))
                self.mutex.release()
        except Exception as e:
            pass

    def _start(self):
        try:
            print('-' * 60)
            print(u'[-] 正在扫描地址:'+ socket.gethostbyname(self.target))
            print('-' * 60)
            # 线程数
            pool = ThreadPool(processes=100)
            # get传递超时时间，用于捕捉ctrl+c
            pool.map_async(self.run, self.ports).get(0xffff)
            pool.close()
            pool.join()
            print('-' * 60)
            print(time() - self.time)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print(u'[-] 用户终止扫描')
            sys.exit(1)

    def check_target(self):
        # 判断目标是域名还是还是ip地址
        flag = self.target.split('.')[-1]
        try:
            # ip地址
            if int(flag) >= 0:
                self._start()
        except:
            # 域名地址
            if not self.check_cdn():
                self._start()
            else:
                print(u'[-] 目标使用了CDN技术,停止扫描')


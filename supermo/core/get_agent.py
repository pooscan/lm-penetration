# coding:utf-8
import time,threading
import requests,urllib
from lxml import etree
import pymysql as mdb
import datetime
import config.config  as conf
from supermo.core.mysqldb import mysqldb as mysql
from supermo.core.get_ua import UA

class IPFactory:
    """
    代理ip抓取/评估/存储一体化。
    """
    def __init__(self):
        self.page_num = conf.PAGE_NUM
        self.round = conf.EXAMINE_ROUND
        self.timeout = conf.PROXY_TIMEOUT
        self.all_ip = set()
        # self.PROXY_THREADS = cfg.PROXY_THREADS
        # mysql().create_db()# 创建数据库
        # current_ips = self.get_all_ip()# 抓取全部ip
        # valid_ip = self.get_the_best(current_ips, self.timeout, self.round)# 获取有效ip
        # print ("123")
        # self.create_workers()

    def get_content(self, url, url_xpath, port_xpath):
        """
        使用xpath解析网页内容,并返回ip列表。
        """
        # 返回列表
        ip_list = []
        try:
            # 设置请求头信息
            headers = {'User-Agent': UA().getPCUA()}
            # 获取页面数据
            results = requests.get(url, headers=headers, timeout=4)
            tree = etree.HTML(results.text)
            # 提取ip:port
            url_results = tree.xpath(url_xpath)
            port_results = tree.xpath(port_xpath)
            urls = [line.strip() for line in url_results]
            ports = [line.strip() for line in port_results]

            if len(urls) == len(ports):
                for i in range(len(urls)):
                    # 匹配ip:port对
                    full_ip = urls[i]+":"+ports[i]
                    if full_ip in self.all_ip:
                        continue
                    # 存储
                    ip_list.append(full_ip)
        except Exception as e:
            print ('get proxies error: ', e)

        return ip_list

    def get_all_ip(self):
        """
        各大网站抓取的ip聚合。
        """
        # 有2个概念：all_ip和current_all_ip。前者保存了历次抓取的ip，后者只保存本次的抓取。
        current_all_ip = set()#保存本次的抓取

        ##################################
        # 66ip网
        ###################################
        url_xpath_66 = '/html/body/div[last()]//table//tr[position()>1]/td[1]/text()'
        port_xpath_66 = '/html/body/div[last()]//table//tr[position()>1]/td[2]/text()'
        for i in range(self.page_num):
            url_66 = 'http://www.66ip.cn/' + str(i+1) + '.html'
            results = self.get_content(url_66, url_xpath_66, port_xpath_66)
            self.all_ip.update(results)
            current_all_ip.update(results)
            # 停0.5s再抓取
            time.sleep(0.5)

        ##################################
        # xici代理
        ###################################
        url_xpath_xici = '//table[@id="ip_list"]//tr[position()>1]/td[position()=2]/text()'
        port_xpath_xici = '//table[@id="ip_list"]//tr[position()>1]/td[position()=3]/text()'
        for i in range(self.page_num):
            url_xici = 'http://www.xicidaili.com/nn/' + str(i+1)
            results = self.get_content(url_xici, url_xpath_xici, port_xpath_xici)
            self.all_ip.update(results)
            current_all_ip.update(results)
            time.sleep(0.5)

        ##################################
        # mimiip网
        ###################################
        url_xpath_mimi = '//table[@class="list"]//tr[position()>1]/td[1]/text()'
        port_xpath_mimi = '//table[@class="list"]//tr[position()>1]/td[2]/text()'
        for i in range(self.page_num):
            url_mimi = 'http://www.mimiip.com/gngao/' + str(i+1)
            results = self.get_content(url_mimi, url_xpath_mimi, port_xpath_mimi)
            self.all_ip.update(results)
            current_all_ip.update(results)
            time.sleep(0.5)

        ##################################
        # kuaidaili网
        ###################################
        url_xpath_kuaidaili = '//td[@data-title="IP"]/text()'
        port_xpath_kuaidaili = '//td[@data-title="PORT"]/text()'
        for i in range(self.page_num):
            url_kuaidaili = 'http://www.kuaidaili.com/free/inha/' + str(i+1) + '/'
            results = self.get_content(url_kuaidaili, url_xpath_kuaidaili, port_xpath_kuaidaili)
            self.all_ip.update(results)
            current_all_ip.update(results)
            time.sleep(0.5)

        return current_all_ip

    # 代理ip可用性测试
    def get_valid_ip(self, ip_set, timeout):
        url = 'http://ip.chinaz.com/getip.aspx'# 设置请求地址http://1212.ip138.com/ic.asp
        headers = {'User-Agent': UA().getPCUA()}
        # 可用代理结果
        results = set()
        # 挨个检查代理是否可用
        try:  # 请求开始时间
            start = time.time()
            r = requests.get(url, headers=headers, proxies=proxy, timeout=5)
            end = time.time()  # 请求结束时间
            # 判断是否可用
            if r.text is not None:
                print('succeed: ' + ip + '\t' + " in " + format(end - start, '0.2f') + 's')
                # 追加代理ip到返回的set中
                results.add(ip)
        except OSError:
            print('timeout:', ip)
        return results
    def check_ip_valid(self,i,ip):
        # 可用代理结果
        results = set()
        url = 'http://ip.chinaz.com/getip.aspx'  # 设置请求地址http://1212.ip138.com/ic.asp
        headers = {'User-Agent': UA().getPCUA()}
        proxy = {'http': 'http://' + ip}
        try:  # 请求开始时间
            start = time.time()
            r = requests.get(url, headers=headers, proxies=proxy, timeout=5)
            end = time.time()  # 请求结束时间
            # 判断是否可用
            if r.text is not None:
                print('succeed: ' + ip + '\t' + " in " + format(end - start, '0.2f') + 's')
                # 追加代理ip到返回的set中
                results.add(ip)
        except OSError:
            print('timeout:', ip)
        return results

    def get_the_best(self, valid_ip, timeout, round):
        # print(valid_ip)
        """
        N轮检测ip列表，避免"辉煌的15分钟"
        """
        # 循环检查次数
        for i in range(round):
            print ("\n>>>>>>>\tRound\t"+str(i+1)+"\t<<<<<<<<<<")
            # 检查代理是否可用
            valid_ip = self.get_valid_ip(valid_ip, timeout)
            # 停一下
            if i < round-1:
                time.sleep(30)
        # 返回可用数据
        return valid_ip

    def save_to_db(self, valid_ips):
        """
        将可用的ip存储进mysql数据库
        """
        if len(valid_ips) == 0:
            print("本次没有抓到可用ip。")
            return
        # 连接数据库
        print ("\n>>>>>>>>>>>>>>>>>>>> 代理数据入库处理 Start  <<<<<<<<<<<<<<<<<<<<<<\n")
        conn = mdb.connect(conf.DB['HOST'], conf.DB['USER'], conf.DB['PASSWORD'], conf.DB['DB_NAME'])
        cursor = conn.cursor()
        try:
            for item in valid_ips:
                # 检查表中是否存在数据
                item_exist = cursor.execute('SELECT * FROM %s WHERE content="%s"' %("valid_ip", item))
                # 新增代理数据入库
                if item_exist == 0:
                    # 插入数据
                    n = cursor.execute('INSERT INTO %s VALUES("%s", 1, 0, 0, 1.0, 2.5)' %("valid_ip", item))
                    conn.commit()
                    # 输出入库状态
                    if n:
                        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+item+" 插入成功。\n")
                    else:
                        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+item+" 插入失败。\n")
                else:
                    print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" "+ item +" 已存在。\n")
        except Exception as e:
            print ("入库失败：" + str(e))
        finally:
            cursor.close()
            conn.close()
        print ("\n>>>>>>>>>>>>>>>>>>>> 代理数据入库处理 End  <<<<<<<<<<<<<<<<<<<<<<\n")
    # 这里开始get_proxies
    def start(self):
        # print("1sd")
        ip_list = []
        # 连接数据库
        conn = mdb.connect(conf.DB['HOST'],conf.DB['USER'],conf.DB['PASSWORD'], conf.DB['DB_NAME'])
        cursor = conn.cursor()
        # 检查数据表中是否有数据
        try:
            ip_exist = cursor.execute('SELECT * FROM %s ' % ("valid_ip"))
            # 提取数据
            result = cursor.fetchall()
            print(result)
            # 若表里有数据　直接返回，没有则抓取再返回
            if len(result):
                for item in result:
                    ip_list.append(item[0])
            else:
                # 获取代理数据
                current_ips = self.get_all_ip()
                # for i in range(int(cfg.PROXY_THREADS)):
                #     # t = threading.Thread(target=self.get_the_best,args=(current_ips, self.timeout, self.round,))
                #     t.start()
                valid_ips = self.get_the_best(current_ips, self.timeout, self.round)
                self.save_to_db(valid_ips)
                ip_list.extend(valid_ips)
        except Exception as e:
            print ("从数据库获取ip失败！")
            print(e)
        finally:
            cursor.close()
            conn.close()

        return ip_list
# ip_factory = IPFactory()



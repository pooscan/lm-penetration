# coding = utf-8

'''
通过简单的TCP端口连接来判断指定IP是否开放了指定端口。
需要扫描的主机端口，支持1-100或21,53,80两种形式
from supermo.core.portscan import portscan
portscan('www.joyoung.com','1-10000')
'''

import socket,re,threading,sys

class portscan():
    def __init__(self,target_host,target_port):
        target_host = portscan.anlyze_host(target_host)
        target_port = portscan.anlyze_port(target_port)

        for port in target_port:
            t = threading.Thread(target=portscan.scanner, args=(target_host, port))  # 多线程扫描端口
            t.start()

    def anlyze_host(target_host):
        # 将从--host参数获取到的目标值转换为标准的xxx.xxx.xxx.xxx形式，其中主要是利用socket的gethostbyname函数将域名形式的值转换为四位点进制形式
        try:
            pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')  # 匹配标准点进制的IP
            match = pattern.match(target_host)
            if match:
                return (match.group())
            else:
                try:
                    target_host = socket.gethostbyname(target_host)  # 如果不是，就把target_host的值作为域名进行解析
                    return (target_host)
                except Exception as err:
                    print('地址解析错误：', err)
                    exit(0)
        except Exception as err:
            print('请注意错误1：', sys.exc_info()[0], err)
            print(parser.usage)
            exit(0)

    def anlyze_port(target_port):
        # 解析--port参数传入的值，返回端口列表
        try:
            pattern = re.compile(r'(\d+)-(\d+)')  # 解析连接符-模式
            match = pattern.match(target_port)
            if match:
                start_port = int(match.group(1))
                end_port = int(match.group(2))
                return ([x for x in range(start_port, end_port + 1)])
            else:
                return ([int(x) for x in target_port.split(',')])
        except Exception as err:
            print('请注意错误2:', sys.exc_info()[0], err)
            print(parser.usage)
            exit(0)

    def scanner(target_host, target_port):
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect((target_host, target_port))
            s.sendall(b'hello\r\n\r\n')
            message = s.recv(100)
            # if message:
            print('[+]%s的%3s端口:打开' % (target_host, target_port))  # 若可以建立连接，表示此端口是打开的
            print(' %s' % message.decode('utf-8'))
            s.close()
        # except socket.timeout:
        #     print('[-]%s的%3s端口:关闭' % (target_host, target_port))  # 如果连接超时，表示此端口关闭
        except Exception as err:
            # print('[-]%s的%3s端口:关闭' % (target_host, target_port))
            exit(0)


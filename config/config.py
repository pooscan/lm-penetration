# coding:utf-8

# MYSQL配置
DB = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'USER': 'root',
    'PASSWORD' : '123456',
    'DB_NAME': 'supermo',
    'CHARSET' : 'utf8'
}

# 获取代理ip配置
PROXY_THREADS = '8'
EXAMINE_ROUND = 2   # 对已经检测成功的ip测试轮次。可适当提高轮次，然而可能ip也将更少。
PROXY_TIMEOUT = 5   # 超时时间。代理ip在测试过程中的超时时间。
PAGE_NUM = 1        # 从代理ip网站上总共要爬取的ip页数

# redis配置
REDIS_HOST = '192.168.0.6'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = 'Mo52492'

# 邮件服务配置
IS_EMAILL_SERVICE_ENABLE = False
SMTP_SERVER_HOST = ''
SMTP_SERVER_PORT = 25
SMTP_SERVER_PASSWORD = ''
SMTP_FROM_ADDR = ''
SMTP_TO_ADDR = ''
SMTP_EMAIL_HEADER = ''
SMTP_SEND_INERVAL = 3600

# 域名爬虫配置
SPIDER_OF_THREADS = 8
SPIDER_TIME = 1 # 分钟
CRAWL_DEEPTH = 3 # 爬虫深度

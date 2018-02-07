import config.config as conf
import redis,urllib.request
import supermo.core.common as com
import pymysql as mysql
from supermo.core.get_ua import UA
from supermo.core.mysqldb import mysqldb
from supermo.core.domain_find_link import LinkFinder

redis = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT, password=conf.REDIS_PASSWORD, decode_responses=True)

class spider():

    def __init__(self, project_name, homepage):
        spider.project_name = project_name
        spider.homepage = homepage

        spider.redis_cralw = str(spider.project_name + "cralw")
        spider.redis_queue = str(spider.project_name + "queue")

        spider.crawled = spider.readCrawl(spider.project_name)
        spider.crawl_page('First spider',spider.homepage)
    def crawl_page(thread_name,page_url):
        # print(spider.gather_links(page_url))
        # exit()
        if not redis.sismember(spider.redis_cralw,com.md5_url(page_url)):
            print(thread_name + ' now crawling ' + str(page_url))
            print('Queue ' + str(redis.scard(spider.redis_queue)) + ' | Crawled  ' + str(redis.scard(spider.redis_cralw)))
            redis.sadd(spider.redis_cralw, com.md5_url(page_url))  # cralw add
            spider.gather_links(page_url)# 搜索url
            # redis.srem(spider.redis_queue,page_url)# queue remove
            mysqldb.insertCrawl(spider.project_name,page_url)
        else:
            print("it is cralw")

    def readCrawl(project_name):
        mysqldb = mysql.connect(conf.DB['HOST'], conf.DB['USER'], conf.DB['PASSWORD'],conf.DB['DB_NAME'])
        cursor = mysqldb.cursor()
        sql = "SELECT url FROM crawlurl  WHERE  taskname = '%s'" % (project_name)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                redis.sadd(spider.redis_cralw,com.md5_url(row[0]))
        except OSError as e:
            print(e)
        mysqldb.close()

    def gather_links(page_url):
        header = {'User-Agent': UA().getPCUA()}
        html_string = ''
        try:
            req = urllib.request.Request(url=page_url, headers=header)
            response = urllib.request.urlopen(req, timeout=5)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(spider.homepage, page_url,spider.project_name)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))



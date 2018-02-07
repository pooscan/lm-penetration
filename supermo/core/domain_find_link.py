import redis
import config.config as conf
import supermo.core.common as com
from html.parser import HTMLParser
from urllib import parse
# from supermo.core.mysqldb import mysqldb

redis = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT, password=conf.REDIS_PASSWORD)

class LinkFinder(HTMLParser):
    def __init__(self, base_url, page_url,project_name):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        LinkFinder.project_name = project_name
        LinkFinder.domain_name = com.get_domain_name(base_url)
        LinkFinder.redis_queue = str(project_name + "queue")
        LinkFinder.redis_cralw = str(project_name + "cralw")
    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    LinkFinder.add_links_to_queue(url)

    def error(self, message):
        pass

    def add_links_to_queue(url):
        if not redis.sismember(LinkFinder.redis_cralw,com.md5_url(url))or(redis.sismember(LinkFinder.redis_queue,url)):
            if LinkFinder.domain_name == com.get_domain_name(url):
                # redis.sadd(LinkFinder.redis_cralw, com.md5_url(url))
                redis.sadd(LinkFinder.redis_queue,str(url))
                # mysqldb.insertCrawl(LinkFinder.project_name,url)
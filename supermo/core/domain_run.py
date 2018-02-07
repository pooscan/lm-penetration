import threading,redis
import config.config as conf
from supermo.core.domain_spider_redis import spider
redis = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT, password=conf.REDIS_PASSWORD, decode_responses=True)


class domain_run():
    def __init__(self,project_name,homepage):
        self.project_name = project_name
        self.homepage = homepage
        domain_run.current_deepth = 1
        domain_run.redis_cralw = str(project_name + "cralw")
        domain_run.redis_queue= str(project_name + "queue")

        spider(project_name, homepage)
        # domain_run.create_workers()
        domain_run.work()

    # Create worker threads (will die when main exits)
    def create_workers():
        for _ in range(conf.SPIDER_OF_THREADS):
            t = threading.Thread(target=domain_run.work)
            t.daemon = True
            t.start()

    # Do the next job in the queue
    def work():
            while not domain_run.UrlsEnmpy():
                # 队头url出队列
                url = redis.spop(domain_run.redis_queue)
                if url is None or url == "":
                    continue
                spider.crawl_page(threading.current_thread().name, url)

            # while url:
            #     if int(redis.scard(domain_run.redis_queue)) > 0:
            #         spider.crawl_page(threading.current_thread().name, url)
            #         url = redis.spop(domain_run.redis_queue)
            #     # time.sleep(60 * 60 * conf.SPIDER_TIME)
            # current_deepth += 1


    # Each queued link is a new job
    # 判断未访问的url队列是否为空
    def UrlsEnmpy():
        return int(redis.scard(domain_run.redis_queue)) == 0
    # def create_jobs():
    #     for link in file_to_set(QUEUE_FILE):
    #         queue.put(link)
    #     queue.join()
    #     crawl()

    # Check if there are items in the queue, if so crawl them
    def crawl():
        if int(redis.scard(domain_run.redis_queue)) > 0:
            print(str(redis.scard(domain_run.redis_queue)) + ' links in the queue')
            # create_jobs()

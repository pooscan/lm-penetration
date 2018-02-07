import redis
import config.config as conf
from supermo.core.mysqldb import mysqldb
import supermo.core.common as com
redis = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT, password=conf.REDIS_PASSWORD, decode_responses=True)
# a = redis.sadd('iwithbqueue',"hello")
# print(redis.scard("iwithbqueue"))
# # print(a)iwithbqueue iwithbcralw
print(redis.delete("iwithbqueue"))
print(redis.delete("iwithbcralw"))
print(redis.smembers("iwithbqueue"))
# def UrlsEnmpy():
#     return int(redis.scard("iwithbqueue")) == 0
# print(UrlsEnmpy())
# print(redis.spop("iwithbqueue"))
# a = com.get_domain_name("http://www.iwithb.com")
# print(a)
mysqldb().create_valid_ip()
# url = redis.spop("iwithbqueue")
# print(url)
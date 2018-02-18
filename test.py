# from supermo.core.domain_run import domain_run
# import supermo.core.domain_spider_redis as sr
# sr.spider('iwithb','http://www.iwithb.com')
# print(a)
# domain_run('iwithb','http://www.iwithb.com')

from supermo.core.portscans import portscan

portscan('27.221.5.95','1','10000')
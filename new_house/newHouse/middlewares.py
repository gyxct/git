# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from  mysql_connect.mysql_connect import MySQLConn
import time


class CrawlNewhouseMiddlewares(object):
    agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'


    ]
    # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class CrawlProxyMiddleware(object):
    i = 0
    j = 0

    def __init__(self):
        self.proxy_address = None

    def connect_mysqldb(self):
        self.i += 1
        mysql_conn = MySQLConn()
        sql = """
                select type,ip,port from ip_t where status=1 order by crawl_time desc limit 10;
            """
        proxy_address = mysql_conn.select_data(sql)
        print "The %s times connect mysqldb" % self.i
        time.sleep(3)
        return proxy_address

    def process_request(self, request, spider):
        if 'spider_name' in dir(spider) and spider.spider_name:
            if 'beijing_fangtianxia' in spider.spider_name:
                return
        # 使用j次代理IP，就重新从数据库中获取一波新的IP
        if self.j % 10 == 0:
            self.proxy_address = self.connect_mysqldb()
            print self.proxy_address
        self.j += 1
        print "self.j: %s" % self.j
        if spider.name not in ["crawl_ip", "test_proxy", "land_gov_detail"]:
            ip_port = random.choice(self.proxy_address)
            ip = ip_port[1]
            port = ip_port[2]
            print "kanghe: %s" % ip
            with open('ip_contend','w+') as fd:
                fd.write(ip)
                fd.close()
            # request.meta['proxy'] = "http://27.13.164.129:9999"
            request.meta['proxy'] = "http://" + str(ip) + ":" + str(port)
            # print request.meta
            # proxy_user_pass = "kang:he"
            # encode_user_pass = base64.encodestring(proxy_user_pass)
            # request.headers['Proxy-Authorization'] = b'Basic ' + encode_user_pass
            # print request.headers
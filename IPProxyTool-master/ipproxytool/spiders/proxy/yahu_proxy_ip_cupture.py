# -*- coding: utf-8 -*-
from basespider import BaseSpider
from proxy import Proxy
from scrapy.http import Request
import pymysql
from pyquery import PyQuery as pyq
import re
from furl import furl
from get_google_images import GetImageUrl
import random


class YaHuProxySpider(BaseSpider):
    name = "yahuproxy"
    allowed_domains = ["https://*.yahoo.com"]
    start_urls = ['http://google_proxy_ip_cupture/']
    not_allowed_keyword = [
        'arbawy',
        'cn-proxy.com',
        'freeproxylists.net',
        'freesocks.top',
        'freevpn.ninja',
        'hidemy.name',
        'ip181.com',
        'newfreshproxies-24',
        'proxy-daily.com',
        'proxylistplus.com',
        'proxyserverlist-24',
        'spoofs.de',
        'sslproxies24',
        'top90da.com',
    ]

    def __init__(self):
        BaseSpider.__init__(self)
        pass

    def get_proxy(self):
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='ip_proxy',
                                     password='l4771822',
                                     db='ip_proxy',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        # 执行sql语句
        try:
            with connection.cursor() as cursor:
                # 执行sql语句，进行查询
                sql = 'SELECT * FROM lagou WHERE speed > 0 ORDER BY id'
                cursor.execute(sql, )
                # 获取查询结果
                # https://search.yahoo.com/search?p=114.229.212.203&fp=1&ei=UTF-8&fr2=time&age=1d&btf=d&fr=yfp-t
                # https://search.yahoo.com/search?p=hehe&pz=10&fr=yfp-t&fr2=time&bct=0&fp=1&b=21&pz=10&bct=0&xargs=0
                result = ['{}/search?p={}:{}&fp=1&ei=UTF-8&fr2=time&age=1d&btf=d&fr=yfp-t'.format('https://search.yahoo.com', i[u'ip'], i[u'port']) for i in cursor._rows]
                # print(result)

                return result
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            connection.commit()

        finally:
            connection.close()

    def start_requests(self):
        get_ip_proxy_list_url = self.get_proxy()
        for url in get_ip_proxy_list_url:
            yield Request(url, callback=self.parse,
                          # headers=headers
                          )

    def parse(self, response):

        j = pyq(response.body)
        infos = j('a.ac-algo.fz-l.ac-21th.lh-24')

        for i in infos.items():
            url = i.attr('href')
            for key in self.not_allowed_keyword:
                if key in url:
                    break
            else:
                yield Request(url, callback=self.parse_deil, dont_filter=True)

        if infos:
            furl_obj = furl(response.url)
            start_pag = furl_obj.args.get('b', '1')
            furl_obj.args['start'] = int(start_pag) + 10
            yield Request(furl_obj.url, callback=self.parse)

    def parse_deil(self, response):
        ip_port = re.findall(r'(\d+\.\d+\.\d+\.\d+).*?(\d+)', response.body)

        for tr in ip_port:
            ip = tr[0]
            port = tr[1]
            country = ""
            anonymity = ""

            proxy = Proxy()
            proxy.set_value(
                ip=ip,
                port=port,
                country=country,
                anonymity=anonymity,
                source=self.name,
            )

            self.add_proxy(proxy=proxy)

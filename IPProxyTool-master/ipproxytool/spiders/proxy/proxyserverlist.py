
from proxy import Proxy
from pyquery import PyQuery as pyq
from basespider import BaseSpider
from scrapy.http import Request
import re


class ProxyServerList(BaseSpider):
    name = 'proxyserverlist'

    def __init__(self, *a, **kwargs):
        super(ProxyServerList, self).__init__(*a, **kwargs)
        self.urls = [
            'http://proxyserverlist-24.blogspot.com/search/label/Free%20Proxy%20Server%20List'
        ]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'proxyserverlist-24.blogspot.com',
            'Referer': 'http://proxyserverlist-24.blogspot.com/2017/03/07-03-17-free-proxy-server-list-3522.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        jpy = pyq(response.body)
        a_s = jpy("h3.post-title.entry-title >a")
        for info in a_s.items():
            url = info.attr('href')
            yield Request(
                    url=url,
                    headers=self.headers,
                    meta=self.meta,
                    dont_filter=True,
                    callback=self.parse_deil,
                    errback=self.error_parse,
            )

    def parse_deil(self, response):
        ip_port = re.findall(r'(\d+\.\d+\.\d+\.\d+):(\d+)', response.body)

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
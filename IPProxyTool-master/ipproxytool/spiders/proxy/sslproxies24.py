
from proxy import Proxy
from pyquery import PyQuery as pyq
from basespider import BaseSpider
from scrapy.http import Request
import re


class SslProxies24(BaseSpider):

    name = 'sslproxies24'

    def __init__(self, *a, **kwargs):
        super(SslProxies24, self).__init__(*a, **kwargs)
        self.urls = [
            'http://sslproxies24.blogspot.com/search/label/Google%20Proxies'
        ]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Host': 'sslproxies24.blogspot.com',
            'Referer': 'http://sslproxies24.blogspot.com/search/label/Google%20Proxies',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3004.3 Safari/537.36',
        }

        self.init()

    def parse_page(self, response):
        jpy = pyq(response.body)
        a_s = jpy("div.jump-link > a")
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
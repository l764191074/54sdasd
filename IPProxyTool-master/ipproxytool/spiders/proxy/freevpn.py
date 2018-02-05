# coding=utf-8

# http://cn-proxy.com/
from proxy import Proxy
from pyquery import PyQuery as pyq
from basespider import BaseSpider


class FreeVpn(BaseSpider):
    name = 'freevpn'

    def __init__(self, *a, **kw):
        super(FreeVpn, self).__init__(*a, **kw)

        self.urls = ['https://freevpn.ninja/free-proxy',
                     'https://freevpn.ninja/free-proxy/type/http',
                     'https://freevpn.ninja/free-proxy/type/https']
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'freevpn.ninja',
            'If-None-Match': 'W/"cb655e834a031d9237e3c33f3499bd34"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        jpy = pyq(response.body)
        articles = jpy("body > main > section > div:nth-child(2) > article")
        for info in articles.items():
            div = info('div')
            ip, port = div.eq(0)('a').text().split(':')
            country = div.eq(2)('a').text()
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

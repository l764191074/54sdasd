# coding=utf-8

# http://cn-proxy.com/
from proxy import Proxy
from pyquery import PyQuery as pyq
from basespider import BaseSpider


class CnProxy(BaseSpider):
    name = 'cn-proxy'

    def __init__(self, *a, **kw):
        super(CnProxy, self).__init__(*a, **kw)

        self.urls = ['http://cn-proxy.com/']
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.xicidaili.com',
            'If-None-Match': 'W/"cb655e834a031d9237e3c33f3499bd34"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        }

        self.init()

    def parse_page(self, response):
        jpy = pyq(response.body)
        trs = jpy("table.sortable > tbody > tr")
        for info in trs.items():
            tds = info('td')
            ip = tds.eq(0).text()
            port = tds.eq(1).text()
            country = tds.eq(2).text()
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

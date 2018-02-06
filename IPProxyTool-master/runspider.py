#-*- coding: utf-8 -*-

import logging
import os
import sys
import traceback
import scrapydo
import time
import utils
import config

from sqlhelper import SqlHelper
from ipproxytool.spiders.proxy.xicidaili import XiCiDaiLiSpider
from ipproxytool.spiders.proxy.sixsixip import SixSixIpSpider
from ipproxytool.spiders.proxy.ip181 import IpOneEightOneSpider
from ipproxytool.spiders.proxy.kuaidaili import KuaiDaiLiSpider
from ipproxytool.spiders.proxy.gatherproxy import GatherproxySpider
from ipproxytool.spiders.proxy.hidemy import HidemySpider
from ipproxytool.spiders.proxy.proxylistplus import ProxylistplusSpider
from ipproxytool.spiders.proxy.freeproxylists import FreeProxyListsSpider
from ipproxytool.spiders.proxy.peuland import PeulandSpider
from ipproxytool.spiders.proxy.usproxy import UsProxySpider
from ipproxytool.spiders.proxy.cnproxy import CnProxy
from ipproxytool.spiders.proxy.freesocks import FreeSocks
from ipproxytool.spiders.proxy.freevpn import FreeVpn
from ipproxytool.spiders.proxy.proxyserverlist import ProxyServerList
from ipproxytool.spiders.proxy.spoofs import Spoofs
from ipproxytool.spiders.proxy.arbawy import Arbawy
from ipproxytool.spiders.proxy.top90da import Top90da
from ipproxytool.spiders.proxy.proxydaily import ProxyDaily
from ipproxytool.spiders.proxy.newfreshproxies import NewFreshProxies
from ipproxytool.spiders.proxy.sslproxies24 import SslProxies24
from ipproxytool.spiders.proxy.google_proxy_ip_cupture import GoogleProxySpider
from ipproxytool.spiders.proxy.yahu_proxy_ip_cupture import YaHuProxySpider

scrapydo.setup()

if __name__ == '__main__':

    os.chdir(sys.path[0])

    reload(sys)
    sys.setdefaultencoding('utf-8')

    if not os.path.exists('log'):
        os.makedirs('log')

    # logging.basicConfig(
    #         filename = 'log/spider.log',
    #         format = '%(levelname)s %(asctime)s: %(message)s',
    #         level = logging.DEBUG
    # )
    sql = SqlHelper()

    while True:
        utils.log('*******************run spider start...*******************')

        command = "DELETE FROM {table} where save_time < SUBDATE(NOW(), INTERVAL 0.5 DAY)".format(
                table = config.free_ipproxy_table)
        sql.execute(command)
        fun_list = [
                    # SslProxies24, NewFreshProxies, ProxyDaily, Top90da, Arbawy, Spoofs,
                    # ProxyServerList, FreeVpn, FreeSocks, CnProxy, XiCiDaiLiSpider, SixSixIpSpider,
                    # IpOneEightOneSpider, KuaiDaiLiSpider, GatherproxySpider, HidemySpider, ProxylistplusSpider,
                    # FreeProxyListsSpider, PeulandSpider, UsProxySpider,
                    YaHuProxySpider,
                    # GoogleProxySpider
        ]
        for i in fun_list:
            try:
                items = scrapydo.run_spider(i)
            except Exception as e:
                print(e)
                os.system('pkill -f runspider.py')
                os.system('pkill -f runspider.py')
        utils.log('*******************run spider waiting...*******************')
        time.sleep(600)


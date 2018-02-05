#! /usr/bin/env python3
# coding=utf-8
import logging
import pprint
import threading
import traceback
import requests
from pyquery import PyQuery as pyq

logger = logging.getLogger('root')

def request_get(url, *param, **kwargs):
    try:
        r = requests.get(url, verify=False, timeout=20, *param, **kwargs)
        return r.text
    except requests.exceptions.MissingSchema:
        return ''
    except:
        logger.error(traceback.format_exc())
        return ''


class GetGoogle(threading.Thread):
    return_list = set()
    test_url_list = set()
    over_flag = list()

    def __init__(self, url=''):
        threading.Thread.__init__(self)
        self.run_url = url

    def get_google_image(self):
        for url in ['http://coderschool.cn/1853.html',
                    'https://sass.wang/archives/578/',
                    'http://www.zizaifan.com/html/google.html',
                    'https://liyuans.com/archives/google-mirror.html']:
            # jpy = pyq(request_get(url='http://coderschool.cn/1853.html').text)

            jpy = pyq(request_get(url=url) or '<html></html>')

            # jpy = pyq(request_get(url='https://sass.wang/archives/578/').text)
            a_list = jpy('a')

            for a in a_list.items():
                url = a.attr('href')
                if url and not url.split('/')[-1] and len(url.split('/')) <= 4:
                    self.test_url_list.add(url)

    def check_google_image(self, url):
        try:
            jpy = pyq(request_get(url=url) or '<html></html>')
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.ReadTimeout:
            return False
        keyword = jpy('input[type="submit"]:nth-child(1)').attr('type') or ''
        if 'submit' == keyword:
            self.return_list.add(url)

    def run(self):
        try:
            self.over_flag.append(self.name)
            jpy = pyq(request_get(url=self.run_url) or '<html></html>')
        except requests.exceptions.ConnectionError:
            self.over_flag.remove(self.name)
            return False
        except requests.exceptions.ReadTimeout:
            self.over_flag.remove(self.name)
            return False
        keyword = jpy('input[type="submit"]:nth-child(1)').attr('type') or ''
        if 'submit' == keyword:
            self.return_list.add(self.run_url)
        self.over_flag.remove(self.name)


def GetImageUrl():
    g = GetGoogle()
    print(g.get_google_image())

    for u in g.test_url_list:
        x = GetGoogle(u)
        x.start()

    while g.over_flag:
        pass

    return list(g.return_list)


if __name__ == '__main__':
    pprint.pprint(GetImageUrl())


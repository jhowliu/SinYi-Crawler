# -*- coding: utf-8 -*-

import os
import re
import time
import os
import requests

from glob import glob
from random import random

from bs4 import BeautifulSoup

from lib.log import Logger
from lib.settings import headers
from lib.utils import generate_cookies

log_path = os.path.join(os.path.dirname('__file__'), 'sinyi-crawler.log')
logger = Logger(log_path)

class SinYiCrawler(object):
    def __init__(self, root_url='http://buy.sinyi.com.tw/list/1.html'):
        self.root_url = root_url
        self.entry_links = []
        self.__setup()

    def __setup(self):
        self.cookies = generate_cookies(self.root_url)
        headers['Cookie'] = self.cookies
        resp = requests.get(self.root_url)

        if resp.status_code == 200:
            self.soup = BeautifulSoup(resp.text, 'html.parser')
        else:
            self.soup = None
            logger.error("failed to request the page")
            exit(1)

    def __get_all_page_links(self):
        self.page_links = []

        base_url = 'http://buy.sinyi.com.tw/list/'
        m = self.soup.select('#search_pagination .page')
        last_page = int(m[-1].text) if len(m) > 0 else -1

        self.page_links = [base_url + str(i) + '.html' for i in range(1, last_page+1)]

        logger.info("total number of page links is %d." % len(self.page_links))

    def __get_entry_links(self):
        base_url = 'http://buy.sinyi.com.tw'
        not_changed = 0

        for ix, link in enumerate(self.page_links):
            logger.info("start crawling the page: %s" % link)
            try:
                resp = requests.get(link)
                time.sleep(0.5)

                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    entries = soup.select('#search_result_list .search_result_item') # css for entries
                    links = [base_url + e.a['href'] for e in entries]
                    links = list(filter(lambda x: x not in self.entry_links, links))

                    if len(links) == 0:
                        not_changed +=1
                        if not_changed == 5:
                            logger.info("there is no new objects.")
                            break
                        continue

                    logger.info("there is %d new objects." % len(links))
                    not_changed = 0
                    self.entry_links.extend(links)

            except Exception as ex:
                logger.warning(repr(ex))
                break

        logger.info("total number of objects is %d" % len(self.entry_links))
        self.__write_into_files({'links': self.entry_links}, '/home/lingtelli/house/parser/parser/data/link')

    def __get_entry_page(self):
        self.entry_pages = {}

        retry_times = 0

        for ix, link in enumerate(self.entry_links):

            entry_id = self.__extract_entry_id(link)
            if entry_id == None or entry_id in self.cached_pages:
                continue

            logger.info("start get page: %s (%d)" % (link, ix))

            # 確保timeout exception
            try:
                resp = requests.get(link, headers=headers, timeout=10)
            except Exception as ex:
                logger.warning(repr(ex))
                logger.warning("Time out continue new page and sleep for 10 seconds.")
                time.sleep(10)
                retry_times += 1
                continue

            resp.encoding = 'utf-8'

            if resp.status_code == 200:
                self.entry_pages[entry_id] = resp.text
                # 到達重試上限即跳出
                if retry_times == 3:
                    break

                if "ROBOT" in resp.text:
                    self.cookie = generate_cookies(self.root_url)
                    logger.warning("failed to get page which link is %s.(%d)" % (link, ix))
                    logger.info("renew the cookie: %s" % self.cookie)
                    headers['Cookie'] = self.cookie
                    retry_times +=1
                    time.sleep(10)

            if ix and ix % 100 == 0:
                logger.info("take a nap, wait 5 seconds")
                time.sleep(5)
                self.__write_into_files(self.entry_pages)
                self.entry_pages.clear()

            time.sleep(0.2)

        self.__write_into_files(self.entry_pages)

    def __get_cached_pages(self):
        self.cached_pages = [ os.path.basename(name) for name in glob('/home/lingtelli/house/parser/parser/data/html/*')]

        print(len(self.cached_pages))

    def __write_into_files(self, dict_, path='/home/lingtelli/house/parser/parser/data/html'):
        if not os.path.isdir(path):
            os.makedirs(path)

        for id_, value in dict_.items():
            filename = os.path.join(path, id_)
            with open(filename, 'w+') as fp:
                if type(value) is list:
                    fp.write('\n'.join(value))
                else:
                    fp.write(value)

    def __extract_entry_id(self, link):
        entry_id = None
        entry_regex = re.compile('\/([a-zA-Z0-9]+).html')

        match = entry_regex.search(link)
        if match:
            entry_id = match.group(1)

        return entry_id

    def start(self, path='/home/lingtelli/house/parser/parser/data/link/links'):
        self.__get_all_page_links()
        if path:
            with open(path) as fp:
                lines = fp.readlines()
                self.entry_links = [line.replace('\n', '') for line in lines]

        self.__get_entry_links()
        self.__get_cached_pages()
        self.__get_entry_page()

        logger.info("Crawling Done!")

if __name__ == '__main__':
    cool = SinYiCrawler()
    cool.start()



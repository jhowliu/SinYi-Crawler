import re
import requests

from bs4 import BeautifulSoup


class CrawlingFlow(object):
    def __init__(self, crawler, parser):
        self._crawler = crawler
        self._parser = parser

    def run(self):
        self.__crawl()
        self.__parse()

        return self._parser.result

    def __parse(self):
        self._parser.start()

    def __crawl(self):
        self._crawler.start()


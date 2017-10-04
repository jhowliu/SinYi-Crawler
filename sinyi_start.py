# -*- coding: utf-8 -*-
import sys

from time import time

from lib.crawler_flow import CrawlingFlow
from sinyi.sinyi_crawler import SinYiCrawler
from sinyi.sinyi_parser import SuperParserSinYi

from orm.control import insert_items

crawler = SinYiCrawler()
parser = SuperParserSinYi()

pipe = CrawlingFlow(crawler, parser)

result_list = pipe.run()
#crawler.start('data/link/links')
#crawler.start()
#parser.start()
#result_list=parser.result

for result in result_list:
    insert_items(result['WebHouseCase'])

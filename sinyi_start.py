# -*- coding: utf-8 -*-
import sys

from time import time

from lib import logger
from lib.crawler_flow import CrawlingFlow

from sinyi.sinyi_crawler import SinYiCrawler
from sinyi.sinyi_parser import SuperParserSinYi

from orm.control import insert_items


crawler = SinYiCrawler()
parser = SuperParserSinYi()

pipe = CrawlingFlow(crawler, parser)

result_list = pipe.run()

for result in result_list:
    item = result['WebHouseCase']
    logger.info("INSERT - %s" % item['idx'])
    insert_items(item)

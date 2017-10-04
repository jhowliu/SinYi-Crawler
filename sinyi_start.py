import sys

from time import time

from lib.crawler_flow import CrawlingFlow
from sinyi.sinyi_crawler import SinYiCrawler
from sinyi.sinyi_parser import SuperParserSinYi

sys.path.append('/home/lingtelli/house')
from commitLib import commitLib

crawler = SinYiCrawler()
parser = SuperParserSinYi()

pipe = CrawlingFlow(crawler, parser)

result_list = pipe.run()
#crawler.start('data/link/links')
#crawler.start()
#parser.start()
commit=commitLib()

for result in result_list:
    commit.send_database_remote(result, time())

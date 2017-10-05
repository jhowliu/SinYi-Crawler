import os

from .log import Logger

LOG_PATH=os.path.join(os.path.dirname(__file__), '../log', 'crawler.log')

logger = Logger(LOG_PATH)

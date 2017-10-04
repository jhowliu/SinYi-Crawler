import logging

from .schema import *
from .engine import sess

def insert_items(item):

    logging.info("<INSERT> - %s" % item['idx'])

    value = HouseInfos(**item)

    row = sess.query(HouseInfos).filter_by(idx=item['idx']).first()

    if (not row):
        sess.add(value)
        sess.commit()

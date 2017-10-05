import os
import logging

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

class Logger(object):
    def __init__(self, path):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # create a file handler
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        handler = logging.FileHandler(path)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)

        # create a stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(handler)
        self.logger.addHandler(stream_handler)

    def info(self, msg):
        self.logger.info(msg)


    def warning(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

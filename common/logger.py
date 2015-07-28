# encoding:utf8

import logging, types

from logging.handlers import RotatingFileHandler

'''
    This is a logger to handle terminal output logs messages ,
    and saved in log files.
    1-console handle to print logs to terminal's stdout messages and stderr,
    2-rotatingFile handler to handle logs to log file.
'''

def getLogger(logger_name, logfilename, rtMax=500):
    logger = logging.getLogger(logger_name)
    #logging.basicConfig(level=logging.DEBUG,
    #                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'),
    #                    datefmt='%a %d %b %Y %H:%M:%S', filename=logfilename, filemode='w')

    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

    fileRotateHandler = RotatingFileHandler(filename=logfilename,
                                            maxBytes=500*1024*1024,
                                            backupCount=10)
    fileRotateHandler.setLevel(logging.INFO)
    fileRotateHandler.setFormatter(formatter)

    # console logger handler to console output logs.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    logger.addHandler(fileRotateHandler)
    logger.addHandler(console)

    return logger

logger = getLogger('main', './test_.log')
print logger
logger.debug('hahah')
logger.info('23123')
logger.info('opsss!')


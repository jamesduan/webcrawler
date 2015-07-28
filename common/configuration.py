
import ConfigParser, sys

from colors import red

def genCfg():
    # init a cfg obj
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read('../conf/crawler.ini')
        return cfg
    except Exception, e:

        print red(sys.exec_info())

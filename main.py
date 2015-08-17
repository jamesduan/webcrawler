# encoding:utf8

import sys, ConfigParser

from colors import red

from crawler import Crawler

from common.configuration import genCfg

def main(seeds,crawl_count):

    craw=Crawler(seeds)
    craw.crawling(crawl_count)

if __name__ == "__main__":

    cfg = genCfg()

    try:
        seeds = cfg.get('agent', 'seeds').split(',')
        crawler_count = cfg.get('agent', 'crawler_count')
        main(seeds, int(crawler_count))

    except KeyboardInterrupt, interrupt:
        print red("Cancelled by user type Ctrl+c ")
        sys.exit(1)
    except ValueError, err:
        print "value errr: ", err
        sys.exit(1)
    except Exception, e:
        print "Unkown exception occurred!", e
        sys.exit(1)


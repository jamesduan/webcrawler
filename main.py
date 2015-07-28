
import sys, ConfigParser

from crawler import Crawler

def main(seeds,crawl_count):

    craw=Crawler(seeds)
    craw.crawling(crawl_count)

if __name__ == "__main__":

    cfg = ConfigParser.ConfigParser()
    cfg.read('../conf/crawler.ini')

    try:
        seeds = cfg.get('agent', 'seeds').split(',')
        crawler_count = cfg.get('agent', 'crawler_count')
        main(seeds, int(crawler_count))

    except KeyboardInterrupt, interrupt:
        print "keyboard interrupt error: ", interrupt
        sys.exit(1)
    except ValueError, err:
        print "value errr: ", err
        sys.exit(1)
    except Exception, e:
        print "Unkown exception occurred!", e
        sys.exit(1)

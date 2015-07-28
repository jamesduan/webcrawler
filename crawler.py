#encoding:utf8

import sys, ConfigParser

from bs4 import BeautifulSoup
import tornado.httpclient

from url_queue import UrlQueue
from request_sender import send_request

class Crawler:

    def __init__(self, seeds):
        #初始化URL队列
        self.urlQueue=UrlQueue()

        if isinstance(seeds, str):
            self.urlQueue.addUnvisitedUrl(seeds)

        elif isinstance(seeds, list):
            for i in seeds:
                self.urlQueue.addUnvisitedUrl(i)
        print "Add the seeds url {unvisitedUrl} to the unvisited url list".format( unvisitedUrl = str(self.urlQueue.unVisited).lstrip('[').rstrip(']'))

    def process(self):
        #队头url出队列
        print self.urlQueue.unVisited
        visitUrl = self.urlQueue.unVisitedUrlDeQuence()
        print "Pop out one url \"%s\" from unvisited url list" % visitUrl

        #获取超链接
        print "\n get hyper links \n"
        links = self.getHyperLinks(visitUrl)
        print "Get %d new links" % len(links)

        #将url放入已访问的url中
        self.urlQueue.addVisitedUrl(visitUrl)

        print "Add Visited url: \"%s\"\n" % (str(visitUrl))
        print "Visited url count: "+str(self.urlQueue.getVisitedUrlCount())
        #未访问的url入列
        for link in links:
            #if u'http://' in link or u'https://' in link:
            self.urlQueue.addUnvisitedUrl(link)
        print "%d unvisited links:" % len(self.urlQueue.getUnvisitedUrl())
        #print self.urlQueue.getUnvisitedUrl()


    #抓取过程主函数
    def crawling(self, crawl_count):

        #循环条件：未被访问的URL链接队列不为空且抓取的的URL链接不多于crawl_count
        flag = True
        if crawl_count is 0:
            flag = False
        elif crawl_count >= 0:
            flag = True
        else:
               raise ValueError("Fetal error : crawler_count->{num} number is invalid.".format(num=str(crawler_count)))

        try:
            if flag:
                while not self.urlQueue.unVisitedUrlsEmpty() and self.urlQueue.getVisitedUrlCount() <= crawl_count-1:
                    self.process()
            else:
                while not self.urlQueue.unVisitedUrlsEnmpy():
                    self.process()
        except Exception, e:
            print "process error:", e
            sys.exit(1)

       ##print self.urlQueue.getUnvisitedUrl()
        print self.urlQueue.getVisitedUrlCount()
        print self.urlQueue.getVisitedUrl()

    #获取源码中得超链接
    def getHyperLinks(self,url):
        print "--------read configs-------"
        cfg = ConfigParser.ConfigParser()
        cfg.read('../conf/crawler.ini')

        server_ip = cfg.get('agent', 'server_ip')
        server_port = cfg.get('agent', 'port')
        server_protocol = cfg.get('agent', 'protocol')
        api = cfg.get('agent', 'api')

        links = []
        title_contents = []
        data = self.getPageSource(url)
        print "got html data."
        #print data
        try:
            #print server_protocol, server_ip, server_port, api
            inner_server_response = send_request(''.join([server_protocol, "://", server_ip, \
                ':', server_port, api]), 'POST', str(data))
            print "-----send reques -----for upload.."
            if inner_server_response.body is "200":
                print "upload html docs done."

        except ValueError, e:
            print "get HyperLinks Value error: ", e
        except Exception, e:
            print "getHyperlinks unkown error:", e

        if data[0] == "200":
            soup = BeautifulSoup(data[1])
            for link in soup.find_all('a'):
                links.append(link.get('href'))

        return links

    #获取网页源码
    def getPageSource(self,url,timeout=100,coding=None):

        try:

            http_response = send_request(url, 'GET')

            if http_response.code == 200:
                return ["200",http_response.body]

        except Exception,e:
            print str(e)
            return [str(e),None]


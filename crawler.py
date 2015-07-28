#encoding:utf8

import sys, ConfigParser

from bs4 import BeautifulSoup
import tornado.httpclient
from colors import yellow, green

from url_queue import UrlQueue
from request_sender import send_request
from common.configuration import genCfg

class Crawler:

    def __init__(self, seeds):

        self.urlQueue=UrlQueue()

        if isinstance(seeds, str):
            self.urlQueue.addUnvisitedUrl(seeds)

        elif isinstance(seeds, list):
            for i in seeds:
                self.urlQueue.addUnvisitedUrl(i)

        print yellow("Add seeds {unvisitedUrl} site.".format( unvisitedUrl = \
            str(self.urlQueue.unVisited).lstrip('[').rstrip(']')))

    def process(self):

        visitUrl = self.urlQueue.unVisitedUrlDeQuence()
        print yellow("\nProcessing Url: {url}".format(url=visitUrl))

        print "Get Hyper Links:"
        links = self.getHyperLinks(visitUrl)
        print yellow("\nGet {linkno} new links".format(linkno = len(links)))

        print yellow("\nAdding url: {url} to VisitedQueue".format(url=visitUrl))
        self.urlQueue.addVisitedUrl(visitUrl)

        print yellow("\nVisited url count: {count}".format(count = \
            str(self.urlQueue.getVisitedUrlCount())))

        for link in links:
            print "\nAdding new link {link_name} to UnvisitedUrlQueue."\
                .format(link_name = green(link))
            self.urlQueue.addUnvisitedUrl(link)

        print "\nHave %d unvisited links" % len(self.urlQueue.getUnvisitedUrl())

    def crawling(self, crawl_count):

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

    def getHyperLinks(self,url):

        cfg = genCfg()

        server_ip = cfg.get('agent', 'server_ip')
        server_port = cfg.get('agent', 'port')
        server_protocol = cfg.get('agent', 'protocol')
        api = cfg.get('agent', 'api')

        links = []
        title_contents = []
        data = self.getPageSource(url)
        #print "got html data."
        #print data

        if data[0] == "200":

            soup = BeautifulSoup(data[1], "html.parser")

            for d_addr in soup.find_all('a'):
                links.append(d_addr.get('href'))

            #for img_addr in soup.find_all('img'):
            #    links.append(img_addr.get('href'))
            print soup.title
            #for link in soup.find_all('a'):
            #    print link
            #    links.append(link.get('href'))

            try:
                inner_server_response = send_request(''.join([server_protocol,
                                                    "://", server_ip, ':',
                                                    server_port, api]), 'POST',
                                                    str(data[1]))

                print "-----send reques -----for upload.."
                if inner_server_response.body is "200":
                    print "upload html docs done."

            except ValueError, e:
                print "get HyperLinks Value error: ", e
            except Exception, e:
                print "getHyperlinks unkown error:", e

        return links

    def getPageSource(self, url, timeout=100, coding=None):

        try:

            http_response = send_request(url, 'GET')

            if http_response.code == 200:
                return ["200",http_response.body]

        except Exception,e:
            print str(e)
            return [str(e),None]


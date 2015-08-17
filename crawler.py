#encoding:utf8

import sys, ConfigParser, traceback, json

from bs4 import BeautifulSoup
import tornado.httpclient
from tornado.escape import utf8
from colors import yellow, green

from url_queue import UrlQueue
from request_sender import send_request
from common.configuration import genCfg

from common.error_link import *


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
            traceback.print_exc()
            sys.exit(1)

       ##print self.urlQueue.getUnvisitedUrl()
        print self.urlQueue.getVisitedUrlCount()
        print self.urlQueue.getVisitedUrl()

    def handle_origin_addr(self, orig_addr):

        #flag = []

        #for err_link_name, val in ERROR_LINK.items():

        #    if orig_link == val:
        #        flag.append(True)

        #if len(flag) == 0:
        #    return orig_link
        addr = str(orig_addr)
        soup = BeautifulSoup(addr, 'html.parser')
        return soup.find_all('a')[0].get('href').encode('utf-8')

    def getHyperLinks(self,url):

        page = {}
        links = []
        title_contents = []

        cfg = genCfg()

        server_ip = cfg.get('agent', 'server_ip')
        server_port = cfg.get('agent', 'port')
        server_protocol = cfg.get('agent', 'protocol')
        api = cfg.get('agent', 'api')

        data = self.getPageSource(url)

        #print "got html data."
        #print data

        if data[0] == "200":
            try:
                soup = BeautifulSoup(data[1], "html.parser")

                #origin_links = []
                #for d_addr in soup.find_all('a'):
                #    origin_links.append(d_addr.get('href'))

                #print origin_links

                #for link in map(self.handle_origin_links, origin_links):

                #    if link:
                #        links.append(link)
                http_addr = soup.select('a[href^=http://]')
                https_addr = soup.select('a[href^=https://]')

                links += map(self.handle_origin_addr, http_addr) + \
                    map(self.handle_origin_addr, https_addr)

#                links = list(set(links))

                #print links
            except ImportError, e:
                print red('Please install BeautifulSoup4 module first.')

            try:
                #code_type = sys.getfilesystemencoding()
                #print "code type: ", code_type
                page[url] = data[1]
                #print page
                inner_server_response = send_request(''.join([server_protocol,
                                                    "://", server_ip, ':',
                                                    server_port, api]), 'POST',
                                                    json.dumps(page))

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
                #print "page : " , utf8(http_response.body)
                return ["200",http_response.body]

        except Exception,e:
            print str(e)
            return [str(e),None]


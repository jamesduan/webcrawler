# encoding:utf8

import sys
from tornado import httpclient
from tornado.escape import utf8

def send_request(url, method, request_body=None, timeout=100):

    print "request {url}".format(url=url)
    try:
        http_header = {'User-Agent' : 'Chrome'}
        http_request = httpclient.HTTPRequest(url=url, method=method, body=request_body,
                                            headers= http_header, connect_timeout=20,
                                            request_timeout=timeout)

        http_client = httpclient.HTTPClient()
        http_response = http_client.fetch(http_request)
        return http_response

    except httpclient.HTTPError as httperror:
        print "send request http error:".join(str(httperror))
        #sys.exit(1)
    except Exception,e:
        print "send request exception : error occurred: ", e
        sys.exit(1)
    finally:
        http_client.close()


#print utf8(send_request('http://www.baidu.com', 'GET').body)

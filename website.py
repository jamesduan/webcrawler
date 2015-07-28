#encoding:utf8

from test import print_r
import unittest

class WebSite(object):
	'''
	def __init__(self, plugin, collection, resource, attr_info,
             allow_bulk=False, member_actions=None, parent=None,
             allow_pagination=False, allow_sorting=False):
	'''
	def __init__(self, site_name , url, title, content = ""):
		self._site_name = site_name
		self._url = url
		self._title = title
		self._content = content

	@property
	def getSiteName(self):
		if (self._site_name != '' and self._site_name!= None):
			return self._site_name

	@property
	def getUrl(self):
		if (self._url != '' and self._url != None):
			return self._url

	@property
	def getTitle(self):
		if (self._title != '' and self._title != None):
			return self._title

	@property
	def getContent(self):
		if (self._content != '' and self._content != None):
			return self._content

if __name__ == "__main__":
#	website = WebSite("baidu", 'http://www.baidu.com', '百度一下，你就知道', '擦点擦点罚款了对方家里卡剪短发了肯定撒')
#	print_r(obj = website)
	suite = unittest.TestLoader().loadTestsFromTestCase(WebSite)
	unittest.TextTestRunner(verbosity=2).run(suite)


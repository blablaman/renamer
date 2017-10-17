# -*- coding: utf-8 -*-
import fetch
import helper
import time
import random
from helper import list_files,normilize,kp_parser,FeedbackCounter,duckParser
import requests
import time, os
import pickle, urllib
from urlparse import urlparse

#plist = [u'http://163.172.156.247:3128', u'http://85.255.0.100:3128', u'http://217.23.156.173:80', u'http://188.0.226.248:53281', u'http://153.122.75.53:8080', u'http://191.252.100.152:80', u'http://111.13.7.118:80', u'http://112.5.56.108:3128', u'http://188.166.252.247:3128', u'http://128.199.192.252:80', u'http://202.51.182.106:8080', u'http://91.234.125.208:53281', u'http://111.13.2.131:80', u'http://190.121.29.235:65309', u'http://216.100.88.228:8080', u'http://216.100.88.229:8080', u'http://197.232.17.83:8080', u'http://122.143.150.202:8998', u'http://223.68.1.38:8000', u'http://95.143.143.59:53281', u'http://139.59.125.77:80', u'http://181.112.228.126:53281']
#nalist = [normilize(n[0]) for n in helper.list_files('/Volumes/Multimedia/Movies/', includeSubdirs=False)]
#nalist = nalist[:10]
fbc = FeedbackCounter()
BASE_URL = 'https://www.kinopoisk.ru/index.php?first=no&what=&kp_query=%s'
#BASE_URL = 'https://www.duckduckgo.com/html/?q=%s'

class KinopoiskGRequests:
	def __init__(self):
		if os.path.exists('proxylist'):
			if (time.time() - os.path.getmtime('proxylist')) < 3600:
				with open('proxylist','rb') as pf:
					self.plist = pickle.load(pf)
				return
		self.plist = fetch.run()
		#['http://127.0.0.1:8888','http://127.0.0.1:8888','http://127.0.0.1:8888']#fetch.run()
		self.url = BASE_URL
		#self.s = requests.Session()
		headers = {
		 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
			}
		with open('proxylist','wb') as pf:
			pickle.dump(self.plist,pf)

	def exception_handler(self, request, exception):
		import grequests
		session = requests.Session()
		print exception
		print request.kwargs['proxies'].get('https')
		print self.plist
		if request.kwargs['proxies'].get('https') in self.plist:
			self.plist.remove(request.kwargs['proxies'].get('https'))
		r = [grequests.get(request.url, proxies={"https" : random.choice(self.plist)}, timeout=10, callback=fbc.feedback, session = session )]
		result = grequests.map(r, exception_handler=self.exception_handler)
		del grequests
		return result[0]

	def kinopoiskSearch(self, namesList):
		import grequests
		session = requests.Session()
		#base_url = BASE_URL
		rss = []
		nlist = namesList[:]
		try:
			while True:
				rs = []
				for p in self.plist:
					name = nlist.pop()
					rs.append(grequests.get(self.url % name, proxies={"https" : p}, callback=fbc.feedback,timeout=10, session = session))
				rss.append(rs)
		except Exception as e:
			print e
			print len(nlist)
			if rs:
				rss.append(rs)

		reqs = []
		for rs in rss:
			reqs += grequests.map(rs, exception_handler=self.exception_handler)
			time.sleep(1)

		print reqs
		responses = []
		for el in namesList:
			for r in reqs:
				#print type(urllib.unquote(r.url.strip(self.url).encode('ascii')))
				#print type(el)
				#print urllib.unquote(r.url.lstrip(self.url[:-2]).encode('ascii'))
				#print el
				#print urllib.unquote(r.url.lstrip(self.url[:-2]).encode('ascii')) == el
				if el==urllib.unquote(r.url.lstrip(self.url[:-2]).encode('ascii')).decode('utf-8'):
					responses.append(r)	
					print urllib.unquote(r.url.strip(self.url))
				
		domain = urlparse(self.url).netloc.lstrip('www.')
		if domain == 'duckduckgo.com':
			res = list(map(duckParser, responses))
		elif domain == 'kinopoisk.ru':
			res = list(map(kp_parser, responses))

		del grequests
		return res

	def setUrl(self, url):
		self.url = url

#plist = fetch.run()
#res = kinopoiskSearch(nalist, plist)
#for i in range(len(nalist)):
	#print (res[i][0] if res else u"None") 
	#nalist[i] + u" ==> " + (res[i][0] if res else u"None") 



	

# -*- coding: utf-8 -*-
import fetch
import helper
import time
import random
from helper import list_files,normilize,kp_parser,FeedbackCounter
import requests

#plist = [u'http://163.172.156.247:3128', u'http://85.255.0.100:3128', u'http://217.23.156.173:80', u'http://188.0.226.248:53281', u'http://153.122.75.53:8080', u'http://191.252.100.152:80', u'http://111.13.7.118:80', u'http://112.5.56.108:3128', u'http://188.166.252.247:3128', u'http://128.199.192.252:80', u'http://202.51.182.106:8080', u'http://91.234.125.208:53281', u'http://111.13.2.131:80', u'http://190.121.29.235:65309', u'http://216.100.88.228:8080', u'http://216.100.88.229:8080', u'http://197.232.17.83:8080', u'http://122.143.150.202:8998', u'http://223.68.1.38:8000', u'http://95.143.143.59:53281', u'http://139.59.125.77:80', u'http://181.112.228.126:53281']
#nalist = [normilize(n[0]) for n in helper.list_files('/Volumes/Multimedia/Movies/', includeSubdirs=False)]
#nalist = nalist[:10]
fbc = FeedbackCounter()

def exception_handler(request, exception):
	import grequests
	session = requests.Session()
	print exception
	r = [grequests.get(request.url, proxies={"https" : random.choice(plist)}, timeout=10, callback=fbc.feedback, session = session)]
	result = grequests.map(r, exception_handler=exception_handler)
	del grequests
	return result[0]

def kinopoiskSearch(namesList, proxyList):
	import grequests
	session = requests.Session()
	base_url = 'https://www.kinopoisk.ru/index.php?first=no&what=&kp_query=%s'
	rss = []
	nlist = namesList[:]
	try:
		while True:
			rs = []
			for p in proxyList:
				name = nlist.pop()
				rs.append(grequests.get(base_url % name, proxies={"https" : p}, callback=fbc.feedback,timeout=10, session = session))
			rss.append(rs)
	except Exception as e:
		print e
		print len(nlist)
		if rs:
			rss.append(rs)

	reqs = []
	for rs in rss:
		reqs += grequests.map(rs, exception_handler=exception_handler)
		time.sleep(1)

	print reqs

	res = list(map(kp_parser, reqs))

	del grequests
	return res

#plist = fetch.run()
#res = kinopoiskSearch(nalist, plist)
#for i in range(len(nalist)):
	#print (res[i][0] if res else u"None") 
	#nalist[i] + u" ==> " + (res[i][0] if res else u"None") 



	

# -*- coding: utf-8 -*-
import grequests
import helper
import time
from helper import list_files,normilize,kp_search,FeedbackCounter

base_url = 'https://www.kinopoisk.ru/index.php?first=no&what=&kp_query=%s'
#nlist = [x for x in xrange(83)]
plist = [u'http://217.23.156.251:80', u'http://190.60.234.131:3128', u'http://177.206.37.217:53281', u'http://112.85.1.94:9131', u'http://64.77.242.74:3128', u'http://62.138.16.87:3128', u'http://121.42.176.133:3128', u'http://193.193.68.2:3128', u'http://178.215.188.223:53281', u'http://162.243.18.46:3128', u'http://1.52.160.100:53281', u'http://202.152.40.28:8080', u'http://104.236.65.142:8080', u'http://190.131.203.90:3128', u'http://103.24.150.242:53281', u'http://186.251.180.33:8080', u'http://187.189.60.141:3130', u'http://158.69.198.191:3128', u'http://41.222.57.164:53281', u'http://103.250.147.22:8080', u'http://123.49.53.210:8080', u'http://125.89.52.189:8118', u'http://109.121.161.44:53281']

rss = []
fbc = FeedbackCounter()

nlist = [normilize(n[0]) for n in helper.list_files('/Volumes/Multimedia/Movies/', includeSubdirs=False)]
#print nlist
nlist = nlist[:20]

try:
	while True:
		rs = []
		for p in plist:
			name = nlist.pop()
			rs.append(grequests.get(base_url % name, proxies={"https" : p}, callback=fbc.feedback,timeout=10))
			#print u"Name: %s, proxy: %s" % (name.encode('ascii','ignore'), p)
			#print name + ' ==> ' + p.encode('ascii','ignore')
		rss.append(rs)
except Exception as e:
	print str(e)
	print len(nlist)
	if rs:
		rss.append(rs)

requests = []
for rs in rss:
	requests += grequests.map(rs)
	time.sleep(1)

print requests
#l = [x for x in requests if x]
#print l
res = list(map(kp_search, l))
print res

#print kp_search(grequests.map(rss[1][6:12])[0])


	

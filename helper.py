# -*- coding: utf-8 -*-
import os
from lxml import html

class FeedbackCounter:
    """Object to provide a feedback callback keeping track of total calls."""
    def __init__(self):
        self.counter = 0

    def feedback(self, r, **kwargs):
        self.counter += 1
        print("{0} fetched, {1} total.".format(r.url, self.counter))
        return r


def kp_parser(request):
	kp_names = list()
	kp_original_names = list()
	years = list()
	result = list()
	if request:
		tree = html.fromstring(request.text)
		ps = tree.xpath('.//div[@class="info" and child::p/a/@data-type="film"]')
		if ps:
			for p in ps:
			    kp_names.append(p.xpath('./p/a[@data-type="film"]/text()')[0])
			    try:
				    years.append(p.xpath('.//span[@class="year"]/text()')[0])
			    except:
				    years.append('')
			    try:
				    n_t = p.xpath('./span[1]/text()')[0].split(',')[0]
			    except:
				    n_t = ''
			    if n_t.split(' ')[-1:][0] == u'мин':
				kp_original_names.append('')
			    else:
				kp_original_names.append(n_t)
		else:
			print "no ps"
			return []

		for i in range(len(ps)):
			result.append(unicode(i) +u'. '+ kp_names[i] + (u' ['+ kp_original_names[i] +u']' if kp_original_names[i] != '' else '') +' ('+ years[i] +u')')
	else:
		print 'no response'
		return []
	return result

def duckParser(response):
	namesList = list()
	if response:
                tree = html.fromstring(response.text)
		a = tree.xpath('.//a[@class="result__a"]/text()')
                if a:
                        for el in a:	
				temp_name = el.split(')')[0]
				if len(temp_name) != el:
					temp_name+=')'
					if len(temp_name.split('/')) > 1:
						namesList.append(temp_name.split('/')[1])
				#namesList.append(unicode(el))
	else:
		print "no duck"
	return namesList		

			


def list_files(directory, includeSubdirs = True):
    ext = ('mkv','avi','mp4')
    r = []
    if includeSubdirs:
            subdirs = [x[0] for x in os.walk(directory)]
            for subdir in subdirs:
                files = os.walk(subdir).next()[2]
                if (len(files) > 0):
                    for f in files:
                        if f.split('.')[-1:][0] in ext:
                                r.append([f,subdir])
    else:
           files = os.walk(directory).next()[2]
           if (len(files) > 0):
                    for f in files:
                        if f.split('.')[-1:][0] in ext:
                                r.append([f,directory])
    return r

def list_files_qt(directory):
            ext = ('mkv','avi','mp4')
            r = []
            subdirs = [x[0] for x in os.walk(directory)]
            for subdir in subdirs:
                files = os.walk(subdir).next()[2]
                if (len(files) > 0):
                    for f in files:
                        if f.split('.')[-1:][0] in ext:
                                r.append(subdir + "/" + f)
            return r

def get_year(s):
	year = ''
	for i in range(len(s)):
		if s[i].isdigit():
			year = year + s[i]
		else:
			if len(year) < 4:
				year = ''
			else: #if len(year) == 4:
				if year[:2] == '19' or year[:2] == '20':
					return year
	return ''

def normilize(file_name):
	name = file_name.replace('.',' ').replace('_',' ')
	year = get_year(name)
	if year:
		name = name[:name.find(year)]
		name += ' (' + year + ')'      
	return name

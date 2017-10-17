# -*- coding: utf-8 -*-
from greq import KinopoiskGRequests
from helper import duckParser
import pickle
import os
import requests

files = ['The.Revenant.2015_WEB-DLRip__[scarabey.org].avi', 'BarKRaFT.2O16.D.Telecine.72Op_KOSHERA.mkv', 'Bce.TTo.HoBoi.2016.L.WEBRip.avi', 'The.Offering.2016.L.WEB-DLRip.avi', 'Bezumnyj.Maks.Doroga.jarosti.2015.D.BDRip.1.46Gb_MegaPeer_by_Twi7ter.avi', 'HuKorga.He.CgaBaiC9.3.2016.L2.DVDRip.avi', 'Kill.Command.2016.L.WEB-DLRip.avi', 'L1ud1.X.Ap0laL1pCiC.2O16.D.TC.1O8Op.mkv', 'Mefika.Nekromant.2O15.P.WEBDLRip.avi', 'Mafiya.Igra.na.vyzhivanie.2016.RUS.BDRip.XviD.AC3.-HQCLUB.avi', 'The.Hobbit.The.Battle.of.the.Five.Armies.2014.Ext_HDRip_r5__[scarabey.org].avi', 'Hobbit.2012.Ext.D.BDRip.2.18GB_New-team_by_Yarmak23.avi', 'Chempiony.Bystree..Vyshe..Silnee.2016.RUS.BDRip.XviD.AC3.-HQCLUB.avi', 'Hobbit.Pustosh.Smauga.2013.RUS.BDRip.XviD.AC3.-HQCLUB.avi']

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
#page = requests.get('https://duckduckgo.com/html/?q=Bce.TTo.HoBoi.2016.L.WEBRip&ia=web', headers=headers, proxies = {'https':'http://127.0.0.1:8888'})
#for el in duckParser(page):
	#print el

if os.path.exists('ducklog'):
	with open('ducklog','rb') as pf:
		res = pickle.load(pf)
else:
	kpr = KinopoiskGRequests()
	kpr.setUrl('https://www.duckduckgo.com/html/?q=%s')
	res = kpr.kinopoiskSearch(files)
	#map(unicode, res)
	with open('ducklog','wb') as pf:
				pickle.dump(res,pf)
for i in range(len(res)):
	for j in range(len(res[i])):
		print res[i][j]
		#res[i][j] = res[i][j].encode('ascii')
#print res

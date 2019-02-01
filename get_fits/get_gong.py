from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u
import urllib
from bs4 import BeautifulSoup 
import os
import time
import numpy as np
from fits_utils import *
import ftplib

out_dir = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/GONG/'
if not os.path.exists(out_dir):
	os.mkdir(out_dir)


time_now = datetime.datetime.utcnow()


#maglc
def get_gong_mag(time_now, out_dir):



	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	url = 'gong2.nso.edu'

	#first do mag gong

	#path = '/QR/bqa/201901/bbbqayy190121'

	base_path = '/QR/bqa/'+time_now.strftime('%Y%m/')

	path = [base_path + x + time_now.strftime('%y%m%d') for x in ['bbbqa', 'lebqa', 'mlbqa', 'tcbqa', 'tdbqa']]


	#ftp_list = 'ftp://' + url + path

	ftpp = ftplib.FTP('gong2.nso.edu') 
	ftpp.login()   
	file_paths = []
	for p in path:
		try:
			ftpp.cwd(p)

			list_of_files = [p +'/'+ x for x in ftpp.nlst('*fits.gz')]

			file_paths.append(list_of_files)
			#print(p, list_of_files)
		except:
			print('still searching!', p)

	list_of_files = sorted(np.concatenate(file_paths), key = lambda x: int(x[-12:-8]))
	latest_file = list_of_files[-1]
	ftpp.close()

	#ftpp.cwd('/QR/bqa/201901/udbqa190121/')   
	#list_of_files = ftpp.nlist('*fits.gz')
	#full_path = 'ftp://gong2.nso.edu/QR/bqa/201901/udbqa190121/' + list_of_files[-1]


	full_path = 'ftp://'+url+latest_file
	urllib.request.urlretrieve(full_path, out_dir + 'gong_mag_'+time_now.strftime('%Y%m%d')+'.fits')#latest_file.split('/')[-1])
	if os.path.exists(out_dir + 'gong_mag_'+time_now.strftime('%Y%m%d')+'.fits'): #latest_file.split('/')[-1]):
		print('gong_mag success!')

#igram
def get_gong_igram(time_now, out_dir):


	if not os.path.exists(out_dir):
		os.mkdir(out_dir)


	url = 'gong2.nso.edu'

	#first do mag gong

	#path = '/QR/bqa/201901/bbbqayy190121'

	base_path = '/QR/iqa/'+time_now.strftime('%Y%m/')

	path = [base_path + x + time_now.strftime('%y%m%d') for x in ['bbiqa', 'leiqa', 'mliqa', 'tciqa', 'tdiqa']]


	#ftp_list = 'ftp://' + url + path

	ftpp = ftplib.FTP('gong2.nso.edu') 
	ftpp.login()   
	file_paths = []
	for p in path:
		try:
			ftpp.cwd(p)

			list_of_files = [p +'/'+ x for x in ftpp.nlst('*fits.gz')]

			file_paths.append(list_of_files)
			#print(p, list_of_files)
		except:
			print('still searching!', p)

	list_of_files = sorted(np.concatenate(file_paths), key = lambda x: int(x[-12:-8]))
	latest_file = list_of_files[-1]
	ftpp.close()

	#ftpp.cwd('/QR/bqa/201901/udbqa190121/')   
	#list_of_files = ftpp.nlist('*fits.gz')
	#full_path = 'ftp://gong2.nso.edu/QR/bqa/201901/udbqa190121/' + list_of_files[-1]


	full_path = 'ftp://'+url+latest_file
	urllib.request.urlretrieve(full_path, out_dir + 'gong_igram_'+time_now.strftime('%Y%m%d')+'.fits')#latest_file.split('/')[-1])
	if os.path.exists(out_dir + 'gong_igram_'+time_now.strftime('%Y%m%d')+'.fits'):#latest_file.split('/')[-1]):
		print('gong_igram success!')

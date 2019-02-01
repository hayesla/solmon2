from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u
import urllib
from bs4 import BeautifulSoup 
import os

#output directory
out_dir = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/SWAP/'
if not os.path.exists(out_dir):
	os.mkdir(out_dir)


def get_swap(time_now, out_dir):
	#get utc time rounded down to the previous hour
	#time_now = datetime.datetime.utcnow().replace(microsecond = 0, second = 0, minute = 0)
	time_now = time_now.replace(microsecond = 0, second = 0, minute = 0)

	base_url = 'http://proba2.oma.be/swap/data/bsd/'
	date_url = base_url + str(time_now.year)+'/' + str('%02d' % time_now.month)+'/'+ str('%02d' %time_now.day) + '/'


	#find the list of available fits files on webpage
	test = urllib.request.urlopen(date_url)
	soup = BeautifulSoup(test, features="lxml")

	fits_links = []
	for link in soup.findAll('a'):
		if link.get('href')[-4:] == 'fits':
			fits_links.append(date_url  + link.get('href'))

	#want the latest file
	latest_files = fits_links[-1]
	#output path directory
	output_path2 = out_dir + latest_files.split('/')[-1]

	urllib.request.urlretrieve(latest_files, output_path2)
	if os.path.exists(output_path2):
		print('swap success!')
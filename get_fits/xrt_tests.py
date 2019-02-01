from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u
import urllib
from bs4 import BeautifulSoup 
import os
import time
import numpy as np

#start_time = time.time()



#output directory
out_dir = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/XRT/'
if not os.path.exists(out_dir):
	os.mkdir(out_dir)

#get utc time rounded down to the previous hour
time_now = datetime.datetime.utcnow().replace(microsecond = 0, second = 0, minute = 0)

def get_xrt(time_now, out_dir):
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	base_url = 'http://solar.physics.montana.edu/HINODE/XRT/QL/syn_comp_fits/'

	#find the list of available fits files on webpage
	test = urllib.request.urlopen(base_url)
	soup = BeautifulSoup(test, features="lxml")

	fits_links = []
	for link in soup.findAll('a'):
		if link.get('href')[-4:] == 'fits':
			fits_links.append(base_url  + link.get('href'))


	time_dif = []
	for i in range(len(fits_links)):

		time_dif.append((time_now - datetime.datetime.strptime(fits_links[i][-22:-7], '%Y%m%d_%H%M%S')).total_seconds())

	index = np.where(time_dif == np.min(time_dif))[0][0]
	latest_file = fits_links[index]


	print(latest_file)

	#output path directory
	output_path2 = out_dir + latest_file.split('/')[-1]

	urllib.request.urlretrieve(latest_file, output_path2)
	if os.path.exists(output_path2):
		print('XRT success!')

#end_time = time.time()
#print(end_time - start_time)
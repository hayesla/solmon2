from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u
import urllib
from bs4 import BeautifulSoup 
import os
import time
import numpy as np
from fits_utils import *


time_now = datetime.datetime.utcnow()


def get_stereo(time_now, out_dir, satellite = 'ahead'):
	#check or make directory to save
	#out_dir = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/STEREO'+satellite[0]+'/'
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	url = 'https://stereo-ssc.nascom.nasa.gov/data/beacon//'+satellite+'/secchi/img/euvi/'
	path = url + time_now.strftime('%Y%m%d/')
	if check_servers_online(path) == 1:
		file_list = list_path_files(path, 'fts')
		latest_file = file_list[-1]

		output_path2 = out_dir + latest_file.split('/')[-1]

		urllib.request.urlretrieve(latest_file, output_path2)
		if os.path.exists(output_path2):
			print('stereo success!')


#get_stereo(satellite = 'ahead')
#get_stereo(satellite = 'behind')
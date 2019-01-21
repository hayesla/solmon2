from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u
import urllib
from bs4 import BeautifulSoup 
import os
import time
import numpy as np
from fits_utils import *




out_dir = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/GONG/'
if not os.path.exists(out_dir):
	os.mkdir(out_dir)

time_now = datetime.datetime.utcnow()
#files are always a day previous
time_file = time_now - datetime.timedelta(days = 1)

url='http://farside.nso.edu'
path='/oQR/fqo/'

if check_servers_online(url) == 1:
	date_path = url + path + time_file.strftime('%Y%m/') + 'mrfqo' + time_file.strftime('%y%m%d/')
	file_list = list_path_files(date_path, 'fits')
	file_to_download = file_list[-1]


	output_path2 = out_dir + file_to_download.split('/')[-1]

	urllib.request.urlretrieve(file_to_download, output_path2)
import datetime
import urllib
from urllib.error import HTTPError, URLError
import os
import pandas as pd 
import numpy as np
#from get_srs_test import date_struct

output_path_test = '/Users/admin/Documents/solarmonitor_2_0/get_data_tests/'

time_now = datetime.datetime.utcnow()

def check_servers_online(website_url):
	check = 0
	try:
		res = urllib.request.urlopen(website_url)
		check = 1
	except HTTPError as e:
		print(website_url, ' Server cant be accessed, ', str(e.code))
	except URLError as e:
		print(website_url, 'Server cant be accessed, ', str(e.reason))

	return check


def get_srs_from_datetime(date):
	server_path = 'ftp://ftp.swpc.noaa.gov/pub/warehouse'
	file_srs = server_path + '/' + date.strftime('%Y') + '/SRS/' + date.strftime('%Y%m%d') + 'SRS.txt'

	solmon_path = 'https://solarmonitor.org'
	file_srs_solmon = solmon_path+'/data/'+date.strftime('%Y')+'/'+date.strftime('%m')+'/'+date.strftime('%d')+'/meta/'+date.strftime('%m')+date.strftime('%d')+'SRS.txt'


	cc = check_servers_online(file_srs)
	dd = check_servers_online(file_srs_solmon)
	if cc == 1:

		file_name = date.strftime('%Y%m%d')+'SRS.txt'
		file_path = os.path.join(output_path_test, file_name)

		urllib.request.urlretrieve(file_srs, file_path)
		print('downloading into ', file_path)
		srs = urllib.request.urlopen(file_srs).read().decode('utf-8')
		srs_found = srs

	elif dd == 1:
		file_name = date.strftime('%Y%m%d')+'SRS.txt'
		file_path = os.path.join(output_path_test, file_name)

		urllib.request.urlretrieve(file_srs_solmon, file_path)
		print('downloading into ', file_path)
		srs = urllib.request.urlopen(file_srs_solmon).read().decode('utf-8')
		srs_found = srs
	else:
		srs_found= 'No data'
	
	return srs_found


srs_today = get_srs_from_datetime(time_now)
srs_yesterday = get_srs_from_datetime(time_now - datetime.timedelta(days = 1))

issued = datetime.datetime.strptime(srs_today.split('\n')[1][9:-4], '%Y %b %d %H%M')
t_noaa = datetime.datetime.strptime(srs_today.split('\n')[1][9:-6] + '00', '%Y %b %d %H%M')
print(issued, t_noaa)
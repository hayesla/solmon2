import datetime
import urllib
from urllib.error import HTTPError, URLError
output_path_test = '/Users/admin/Documents/solarmonitor_2_0/get_data_tests/'
import os
import pandas as pd 

import numpy as np

class date_struct():
	def __init__(self, date = 'now'):
		"""
		Creates a date object that includes directory format and previous and next dates.
		If no date is given, the object returns the current UTC time now.
		Input must be a date format in YYMMDD
		"""
		if date == 'now':
			self.utc_date = datetime.datetime.utcnow()
		else:
			try:
				self.utc_date = datetime.datetime.strptime(date, '%Y%m%d') 
			except:
				print('date input must be a str in yymmdd format, e.g. 20181128')


		self.date_dir = self.utc_date.strftime('%Y/%m/%d') 			#yyyy/mm/dd
		self.date = self.utc_date.strftime('%Y%m%d') 				#yyyymmdd
		self.year = self.utc_date.strftime('%Y')
		self.month = self.utc_date.strftime('%m')
		self.day = self.utc_date.strftime('%d')
		self.utc = self.utc_date.strftime('%d-%b-%Y %H:%M')			#dd-mmm-yyyy HH:MM
		self.prev_date = (self.utc_date - datetime.timedelta(days = 1)).strftime('%Y%m%d')  #yyyymmdd
		self.next_date = (self.utc_date + datetime.timedelta(days = 1)).strftime('%Y%m%d')  #yyyymmdd



#get todays date structure
date_time = date_struct()

#todays directory for saving files
today_dir = output_path_test + date_time.date_dir +'/'

#test if website is active

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


server = 'http://services.swpc.noaa.gov'
solmon_server = 'http://solarmonitor.org'
back_up = 'http://legacy-www.swpc.noaa.gov/'
server_path = 'ftp://ftp.swpc.noaa.gov/pub/warehouse'

server_check = check_servers_online(server)
solmon_server_check = check_servers_online(solmon_server)
back_up_check = check_servers_online(back_up)


def get_srs(date):
	server_path = 'ftp://ftp.swpc.noaa.gov/pub/warehouse'
	file_srs = server_path + '/' + date.year + '/SRS/' + date.date + 'SRS.txt'

	solmon_path = 'https://solarmonitor.org'
	file_srs_solmon = solmon_path+'/data/'+date.year+'/'+date.month+'/'+date.day+'/meta/'+date.month+date.day+'SRS.txt'


	cc = check_servers_online(file_srs)
	dd = check_servers_online(file_srs_solmon)
	if cc == 1:

		file_name = date.date+'SRS.txt'
		file_path = os.path.join(output_path_test, file_name)

		urllib.request.urlretrieve(file_srs, file_path)
		print('downloading into ', file_path)
		srs = urllib.request.urlopen(file_srs).read().decode('utf-8')
		srs_today = srs

	elif dd == 1:
		file_name = date.date+'SRS.txt'
		file_path = os.path.join(output_path_test, file_name)

		urllib.request.urlretrieve(file_srs_solmon, file_path)
		print('downloading into ', file_path)
		srs = urllib.request.urlopen(file_srs_solmon).read().decode('utf-8')
		srs_today = srs
	else:
		srs_today = 'No data'
	
	return srs_today


#tests on dfferent days
tod_date = date_struct()
yes_time = date_struct()

srs_today = get_srs(tod_date)
srs_yday = get_srs(yes_time)

srs_today = srs_today.upper()
srs_yday = srs_yday.upper()
issued = srs_today[31:45]+':'+srs_today[45:47]
t_noaa = srs_today[31:42] + ' 00:00' 


#ar comb

srs_test = srs_today.split('\n')
srs_test2 = srs_yday.split('\n')
issued = srs_test[1][9:20]
t_noaa = srs_test[1][9:20]



nlines = len(srs_test)

def put_srs_in_df(srs_test):
	for i in range(0, len(srs_test)-1):
		if srs_test[i][0:2] == 'I.':
			ind_start = i
		if srs_test[i][0:3] == 'IA.':
			ind_end = i


	header_srs = srs_test[ind_start+1].split()[0:-1] 

	data_srs = np.array([x.split() for x in srs_test[ind_start+2:ind_end]])
	if data_srs[0][0] == 'NONE':
		data_srs = np.array([len(header_srs)*['NONE']])
	
	data_test = pd.DataFrame(data_srs, columns = header_srs)
	#print(data_test)
	#get into right format for McIntost Classification i.e. Zpc
	data_test['Z'] = [x[0].upper() + x[1:3].lower() for x in data_test['Z']]
	data_test['MAG_AL'] = data_test['MAG']
	greek_to_alpha(data_test['MAG_AL'])
	return data_test


def greek_to_alpha(x):
	for i in range(0, len(x)):
		if x[i] == 'ALPHA':
			x[i] = 'a'
		if x[i] == 'BETA':
			x[i] = 'b'
		if x[i] == 'BETA-GAMMA':
			x[i] = 'bg'
		if x[i] == 'DELTA':
			x[i] == 'd'
		if x[i] == 'BETA-DELTA':
			x[i] = 'bd'
		if x[i] == 'GAMMA-DELTA':
			x[i] = 'gd'
		if x[i] == 'BETA-GAMMA-DELTA':
			x[i] == 'bgd'	
	return x		

data_test = put_srs_in_df(srs_test)
print(data_test)



import datetime
import urllib
from urllib.error import HTTPError, URLError
import os
from scipy.io import readsav
import numpy as np
output_path_test = '/Users/admin/Documents/solarmonitor_2_0/get_data_tests/'
from bs4 import BeautifulSoup 
import pandas as pd
from rot_location2 import rot_location
from sunpy.time import parse_time

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
		self.prev_date = (self.utc_date - datetime.timedelta(days = 1))
		self.next_date = (self.utc_date + datetime.timedelta(days = 1))





#get todays date structure
date_time = date_struct()

#todays directory for saving files
today_dir = output_path_test + date_time.date_dir +'/'


#get latest data
gevloc_fname = 'ssw_gev_locate.geny'
http_parent = 'http://www.lmsal.com/solarsoft/latest_events'


full_url =  os.path.join(http_parent, gevloc_fname)

#name of file
file_name = date_time.date+'_ssw_lastevents.geny'
#path or which the path is saved
file_path = os.path.join(output_path_test, file_name)
#pull down the latest 
urllib.request.urlretrieve(full_url, file_path)



print('downloading into ', file_path)

archive_url = 'http://www.lmsal.com/solarsoft/latest_events_archive/events_summary/2015/09/29/gev_20150929_2250/index.html'


#once you have the data in the structure find the events for the date of interest and previous day

#data = readsav(file_name)['p0']

#dates = np.frompyfunc(lambda x: x[0:10], 1, 1)(data.date_obs.astype('str'))
#ind_today = np.where(dates == date_time.utc_date.strftime('%Y-%m-%d'))[0]
#ind_yday = np.where(dates == date_time.prev_date.strftime('%Y-%m-%d'))[0]


#today_data = data[ind_today]
#yesterday_data = data[ind_yday]
#if today_data.size != 0:





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


def find_latest_events():
	ssw_url = 'http://www.lmsal.com/solarsoft/latest_events/'
	if check_servers_online(ssw_url) == 1:
		dataframe = pd.read_html(ssw_url, header = 0)[0]
		events = dataframe.drop('Event#', axis = 1)
	else:
		events = 'No data'
	return events

def find_old_events(date):


	test_url = 'http://www.lmsal.com/solarsoft/latest_events_archive/events_summary/'+date.date_dir+'/'

	if check_servers_online(test_url) == 1:
		test = urllib.request.urlopen(test_url)
		soup = BeautifulSoup(test, features="lxml")

		gev_links = []
		for link in soup.findAll('a'):
			if link.get('href')[0:3] == 'gev':
				gev_links.append(test_url  + link.get('href'))

		try:
			dataframes = [pd.read_html(x, header = 0)[0] for x in gev_links]
			events = pd.concat(dataframes, ignore_index = True).drop('Event#', axis = 1)
		except:
			events = 'No data'

	else:
		events = 'No data'

	return events

events = find_latest_events()

#update to new derived positions


solar_xy = []
new_loc = []
for i in range(len(events)):

	new_location, xy = rot_location(events['Derived Position'].values[i], parse_time(events['Start'].values[i]), date_time.utc_date)
	solar_xy.append(xy)
	new_loc.append(new_location)

solar_xy = np.array(solar_xy)
events['new_x'] = solar_xy[:,0]
events['new_y'] = solar_xy[:,1]
events['new_loc'] = new_loc

if type(events) != str:
	dates = np.array([x[0:10] for x in events['Start']])

	ind_today = np.where(dates == date_time.utc_date.strftime('%Y-%m-%d'))[0]
	ind_yday = np.where(dates == date_time.prev_date.strftime('%Y-%m-%d'))[0]


	today_data = events[ind_today]
	yesterday_data = events[ind_yday]

def events_test(dates):

	#events = find_latest_events()
	events = find_old_events(dates)
	#update to new derived positions


	solar_xy = []
	new_loc = []
	for i in range(len(events)):

		new_location, xy = rot_location(events['Derived Position'].values[i], parse_time(events['Start'].values[i]), date_time.utc_date)
		solar_xy.append(xy)
		new_loc.append(new_location)

	solar_xy = np.array(solar_xy)
	events['new_x'] = solar_xy[:,0]
	events['new_y'] = solar_xy[:,1]
	events['new_loc'] = new_loc


	return events
















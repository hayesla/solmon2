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

def check_servers_online(website_url):
	'''
	function to ping server to check online

	Parameters
    ----------

    url of website of interest
    e.g. check_servers_online('https://solarmonitor.org')
    	 
   	Returns
    -------
	0 if not online, 1 if online
	prints error is url not online

    '''

	check = 0
	try:
		res = urllib.request.urlopen(website_url)
		check = 1
	except HTTPError as e:
		print(website_url, ' Server cant be accessed, ', str(e.code))
	except URLError as e:
		print(website_url, 'Server cant be accessed, ', str(e.reason))

	return check


def find_old_events(date):

	'''
	function to find event summary from a specific date

	Parameters
    ----------

    date - datetime.datetime
    e.g. date_interest = datetime.datetime.strptime('2013-10-28', '%Y-%m-%d')
    	 events = find_old_events(date_interest)

   	Returns
    -------

    if data available returns pandas Dataframe of event information
    if no data - return str 'No data'

    '''


	test_url = 'http://www.lmsal.com/solarsoft/latest_events_archive/events_summary/'+date.strftime('%Y/%m/%d/')

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
			events = pd.DataFrame(columns = ['EName', 'Start', 'Stop', 'Peak', 'GOES Class', 'Derived Position', 'new_x', 'new_y', 'new_loc'])

	else:
		events = pd.DataFrame(columns = ['EName', 'Start', 'Stop', 'Peak', 'GOES Class', 'Derived Position', 'new_x', 'new_y', 'new_loc'])

	return events


def find_latest_events():
	'''
	function to return latest event summary

   	Returns
    -------

    if data available returns pandas Dataframe of event information
    if no data - return str 'No data'

    '''
	ssw_url = 'http://www.lmsal.com/solarsoft/latest_events/'
	if check_servers_online(ssw_url) == 1:
		dataframe = pd.read_html(ssw_url, header = 0)[0]
		events = dataframe.drop('Event#', axis = 1)
	else:
		events = pd.DataFrame(columns = ['EName', 'Start', 'Stop', 'Peak', 'GOES Class', 'Derived Position', 'new_x', 'new_y', 'new_loc'])
	return events



def get_event_struct(date):
	'''
	function to return events structure of interest with the 
	updated derived position from when occured to time of interest

	Parameters
	----------

	date of interest - datetime.datetime
	if today then finds latest events
	if earlier day finds old events


	Returns
	-------
	pandas.Dataframe with event information including new l
	ocation at time of interest

	'''
	time_now = datetime.datetime.utcnow()
	if type(date) != datetime.datetime:
		print('needs to be in datetime.datetime format!')
		return

	if date.date() == time_now.date():
		events = find_latest_events()
	else:
		events = find_old_events(date)
	#update to new derived positions

	if len(events)>0:
		solar_xy = []
		new_loc = []
		for i in range(len(events)):

			new_location, xy = rot_location(events['Derived Position'].values[i], parse_time(events['Start'].values[i]), date)
			solar_xy.append(xy)
			new_loc.append(new_location)

		solar_xy = np.array(solar_xy)
		events['new_x'] = solar_xy[:,0]
		events['new_y'] = solar_xy[:,1]
		events['new_loc'] = new_loc


	return events

#####################################

#time of interest
time_now = datetime.datetime.utcnow()
date_search = time_now #datetime.datetime.strptime('2013-10-28', '%Y-%m-%d')


def events_arm(date_search):
	'''
	function that returns pandas Dataframes of X, M and C class events
	from the date searched and the previous day

	Parameters
	----------

	date_search - date of interest, datetime.datetime

	Returns
	-------

	pd.Dataframes from X, M, C events from date_search and date_search - 1day

	'''

	if date_search.date() == time_now.date():
		events = get_event_struct(date_search)
	else:
		events_today = get_event_struct(date_search)
		events_yday = get_event_struct(date_search - datetime.timedelta(days = 1))

		events = pd.concat((events_today, events_yday)).reset_index(drop = True)

	#check that the returned events is not 'No data' string

	dates = np.array([datetime.datetime.strptime(x[0:10], '%Y/%m/%d') for x in events['Start']])
	ind_today = np.where(dates == date_search.replace( microsecond = 0, second = 0, minute = 0, hour = 0))[0]
	ind_yday = np.where(dates == (date_search - datetime.timedelta(days = 1)).replace( microsecond = 0, second = 0, minute = 0, hour = 0))[0]


	today_events = events.loc[ind_today]
	yday_events = events.loc[ind_yday]


	x_class_today = today_events[today_events['GOES Class'].map(lambda x: x[0]) == 'X']
	m_class_today = today_events[today_events['GOES Class'].map(lambda x: x[0]) == 'M']
	c_class_today = today_events[today_events['GOES Class'].map(lambda x: x[0]) == 'C']


	x_class_yday = yday_events[yday_events['GOES Class'].map(lambda x: x[0]) == 'X']
	m_class_yday = yday_events[yday_events['GOES Class'].map(lambda x: x[0]) == 'M']
	c_class_yday = yday_events[yday_events['GOES Class'].map(lambda x: x[0]) == 'C']

	return today_events.reset_index(drop = True), yday_events.reset_index(drop = True)

	'''
	print('todays X-class flares ', x_class_today['GOES Class'].values)
	print('todays M-class flares', m_class_today['GOES Class'].values)
	print('todays C-class flares', c_class_today['GOES Class'].values)
	print('ydays X-class flares ',x_class_yday['GOES Class'].values)
	print('ydays M-class flares ',m_class_yday['GOES Class'].values)
	print('ydays C-class flares ',c_class_yday['GOES Class'].values)
	'''
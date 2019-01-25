import datetime
import urllib
from urllib.error import HTTPError, URLError
import os
import pandas as pd 
import numpy as np

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



def get_noaa_probs():
	url_noaa = 'http://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt'
	cc = check_servers_online(url_noaa)
	if cc == 1:

		noaa_data = urllib.request.urlopen(url_noaa).read().decode('utf-8')
		st = noaa_data.find('Reg_Prob')
		if st == -1:
			noaa_name = ['...']
			noaa_c_probs = ['...']
			noaa_m_probs = ['...']
			noaa_x_probs = ['...']
			



		else:
			noaa_probs = noaa_data[st:].split('\n')[1:-1]
			noaa_name = []
			noaa_c_probs = []
			noaa_m_probs = []
			noaa_x_probs = []
			for i in range(len(noaa_probs)):
				noaa_name.append('1'+noaa_probs[i].split()[0])
				noaa_c_probs.append(noaa_probs[i].split()[1])
				noaa_m_probs.append(noaa_probs[i].split()[2])
				noaa_x_probs.append(noaa_probs[i].split()[3])
	else:
		print('cant access server')
	return noaa_name, noaa_c_probs, noaa_m_probs, noaa_x_probs


from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u
import urllib
from bs4 import BeautifulSoup 
import os
import numpy as np
from fits_utils import *
from astropy.io import fits 
from sunpy import map
import matplotlib.pyplot as plt 



#date of interest
time_now = datetime.datetime.utcnow()
#test date
#time_now = datetime.datetime.strptime('2019-01-04', '%Y-%m-%d')
time_now_date = time_now.strftime('%Y/%m/%d')


#try Kanzelhohe first
def try_kanz(time_now):
	url = 'http://cesar.kso.ac.at'
	latest_file = None
	if check_servers_online(url) == 1:
		path = url + '/halpha2k/recent/' + time_now.strftime('%Y/')
		#find the list of available fits files on webpage

		fits_links = list_path_files(path, 'fts.gz')

		if len(fits_links)>0:
			time_dif = []
			for i in range(len(fits_links)):

				time_dif.append(np.abs((time_now - find_file_times(fits_links[i])).total_seconds()))

			index = np.where(time_dif == np.min(time_dif))[0][0]
			latest_file = fits_links[index]
			

	return latest_file



#next try BBSO 
def try_bbso(time_now):
	url = 'http://www.bbso.njit.edu'
	latest_file = None
	if check_servers_online(url) == 1:
		i = 0
		max_date = 5
		
		#check last 5 days for data
		while i < max_date:
			date = (time_now - datetime.timedelta(days = i))
			path = url + '/pub/archive/'+date.strftime('%Y/%m/%d/')
			
			fits_links = list_path_files(path, 'fts')

			#if there are files find which one is closest to current time
			if len(fits_links)>0:
				time_dif = []
				for i in range(len(fits_links)):

					time_dif.append(np.abs((time_now - find_file_times(fits_links[i])).total_seconds()))

				index = np.where(time_dif == np.min(np.abs(time_dif)))[0][0]
				latest_file = fits_links[index]
				#if a file is found - exit out of while loop
				i = max_date + 1

			else:
				i = i+1

	return latest_file 


def get_halpha(date_search, out_dir):

	if not os.path.exists(out_dir):
		os.mkdir(out_dir)


	file_to_download = None
	files_kanz = try_kanz(date_search)#; print(files_kanz)
	files_bbso = try_bbso(date_search)#; print(files_bbso)

	if files_kanz != None and files_bbso != None:

		time_kanz = (time_now - find_file_times(files_kanz)).total_seconds()
		time_bbso =  (time_now - find_file_times(files_bbso)).total_seconds()
		if np.abs(time_kanz) > np.abs(time_bbso):
			file_to_download = files_bbso
		elif np.abs(time_kanz) < np.abs(time_bbso):
			file_to_download = files_kanz
		else:
			print('somethings wrong')

	elif files_kanz != None and files_bbso == None:
		file_to_download = files_kanz

	elif files_kanz == None and files_bbso != None:
		file_to_download = files_bbso

	elif files_kanz == None and files_bbso == None:
		print('No files at http://cesar.kso.ac.at or http://www.bbso.njit.edu')

	else:
		print('bug somewhere!')


	print(file_to_download)

	output_path2 = out_dir + 'halpha_'+date_search.strftime('%Y%m%d') + '.fits'#file_to_download.split('/')[-1]

	urllib.request.urlretrieve(file_to_download, output_path2)
	if os.path.exists(output_path2):#latest_file.split('/')[-1]):
		print('halpha success!')
#maybe come back to check nso and njit archives

### now if no file available - search other sites ###
'''
def try_nso():
	url = 'http://halpha.nso.edu/'
	if check_servers_online(url) == 1:
		i = 0
		max_date = 5
		
		#check last 5 days for data
		while i < max_date:
			date = (time_now - datetime.timedelta(days = i))
			path = url + '/keep/haf/'+ date.strftime('%Y%m') +'/' + date.strftime('%Y%m%d')



			i = i + 1

'''

#for plotting
def plot_results():
	fits_data = fits.open(output_path2)
	map_halpha = map.Map(fits_data[0].data, fits_data[0].header)
	map_halpha.plot()





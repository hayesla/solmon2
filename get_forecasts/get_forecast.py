import datetime
import urllib
from urllib.error import HTTPError, URLError
import os
import pandas as pd 
import numpy as np
from scipy.io import readsav


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


#this needs to be fixed!
def get_noaa_probs():
	url_noaa = 'http://services.swpc.noaa.gov/text/3-day-solar-geomag-predictions.txt'
	cc = check_servers_online(url_noaa)
	if cc == 1:

		noaa_data = urllib.request.urlopen(url_noaa).read().decode('utf-8')
		st = noaa_data.find('Reg_Prob')
		if st == -1:
			noaa_name = ['...']
			noaa_prob_all = ['...', '...', '...']


		else:
			noaa_probs = noaa_data[st:].split('\n')[1:-1]
			noaa_name = []
			noaa_prob_all = []

			for i in range(len(noaa_probs)):
				noaa_name.append('1'+noaa_probs[i].split()[0])
				noaa_prob_all.append((float(noaa_probs[i].split()[1]), float(noaa_probs[i].split()[2]), float(noaa_probs[i].split()[3])))

	else:
		print('cant access server')
		noaa_name = ['...']
		noaa_prob_all = (['...', '...', '...'])



	return noaa_name, noaa_prob_all



def get_mcstat_forecast(mcintosh):


	flarehist_path = '/Users/laurahayes/Documents/solarmonitor2_0/solmon2/get_forecasts/'
	flarehist_file = os.path.join(flarehist_path, 'flarehist.txt')

	flarehist_data = pd.read_csv(flarehist_file, skiprows = 14, delim_whitespace = True)

	mcpi = flarehist_data['CLS']

	nc = flarehist_data['C'] / flarehist_data['N']
	nm = flarehist_data['M'] / flarehist_data['N']
	nx = flarehist_data['X'] / flarehist_data['N']


	mci = mcintosh.upper()
	index = np.where(mcpi == mci)[0]
	if len(index) < 1:
		cprob = '...'
		mprob = '...'
		xprob = '...'
	else:
		index = index[0]
		cprob = round(100.*(1-np.exp(-nc[index]))) 
		mprob = round(100.*(1-np.exp(-nm[index])))
		xprob = round(100.*(1-np.exp(-nx[index]))) 

		#print(cprob, mprob, xprob)
	return cprob, mprob, xprob



def get_mcevol_forecast(mcintosh_1, mcintosh_2):
		

	#Defining McIntosh Classifications
	Zur = np.array(['A','B','H', 'C', 'D', 'E', 'F'])
	Pen = np.array(['X', 'R', 'S', 'A','H', 'K'])
	Comp = np.array(['X', 'O', 'I' , 'C'])

	flarehist_path = '/Users/laurahayes/Documents/solarmonitor2_0/solmon2/get_forecasts/'
	flarehist_file = os.path.join(flarehist_path, 'mcint_evol_flarehist.sav')

	flarehist_data = readsav(flarehist_file)
	mcint_flrate_c = flarehist_data['mcint_flrate_c']
	mcint_flrate_m = flarehist_data['mcint_flrate_m']
	mcint_flrate_x = flarehist_data['mcint_flrate_x']
	

	count = 0

	mcint_t = mcintosh_1.upper()
	mcint_y = mcintosh_2.upper()

	if len(mcint_t) < 3  or len(mcint_y) < 3:
		count += 1

	else:	
		index_zt = np.where(Zur == mcint_t[0])[0][0]
		index_pt = np.where(Pen == mcint_t[1])[0][0]
		index_ct = np.where(Comp == mcint_t[2])[0][0]

		index_zy = np.where(Zur == mcint_y[0])[0][0]
		index_py = np.where(Pen == mcint_y[1])[0][0]
		index_cy = np.where(Comp == mcint_y[2])[0][0]

		index_list = [index_ct, index_pt, index_zt, index_cy,index_py, index_zy]

	#check if evolution has never been seen before - i.e check if nan
		if np.isfinite(mcint_flrate_c[index_ct, index_pt, index_zt, index_cy,index_py, index_zy]) == False:
			count +=1



	if count > 0:
		cprob_evol = '...'
		mprob_evol = '...'
		xprob_evol = '...'

	else:
		c_rate = mcint_flrate_c[index_ct, index_pt, index_zt, index_cy,index_py, index_zy]
		m_rate = mcint_flrate_m[index_ct, index_pt, index_zt, index_cy,index_py, index_zy]
		x_rate = mcint_flrate_x[index_ct, index_pt, index_zt, index_cy,index_py, index_zy]

		cprob_evol = round(100 * (1 - np.exp(-c_rate)))
		mprob_evol = round(100 * (1 - np.exp(-m_rate)))
		xprob_evol = round(100 * (1 - np.exp(-x_rate)))


	return cprob_evol, mprob_evol, xprob_evol









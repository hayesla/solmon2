import numpy as np 
import pandas as pd 
from scipy.io import readsav
import os





def get_mcevol_forecast(mcintosh_1, mcintosh_2):
		

	#Defining McIntosh Classifications
	Zur = np.array(['A','B','H', 'C', 'D', 'E', 'F'])
	Pen = np.array(['X', 'R', 'S', 'A','H', 'K'])
	Comp = np.array(['X', 'O', 'I' , 'C'])

	flarehist_path = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/get_forecasts/'
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


	print(cprob_evol, mprob_evol, xprob_evol)	






def get_mcevol_forecast_test():

	mci_list = ['CRO/CRO', 'CRO/CAO']
	names = ['12733']
	for i in range(len(mci_list)):
		mci = mci_list[i]
		length = len(mci)
		mci_str_first = mci

		#------------------------#


		#if the McIntosh = ' / '
		if length == 1:
			
			mci_today = ''
			mci_yest = ''

		#if the McIntosh = ' /Xxx' or 'Xxx/ '
		elif length == 4:

			if mci_str_first == '/':
				mci_today = ''
				mci_yest = mci[1:]
			else:
				mci_today = mci[1:]
				mci_yest = ''
		#if the McIntosh  = 'Xxx/Xxx' 
		elif length == 7:
			mci_today = mci[0:3]
			mci_yday = mci[4:]


		#-------------------------#
		count = 0

		mcint_t = mci_today
		mcint_y = mci_yday

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


		print(cprob_evol, mprob_evol, xprob_evol)




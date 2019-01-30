import numpy as np 
import pandas as pd
import os


def get_mcstat_forecast(mcintosh):


	flarehist_path = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/get_forecasts/'
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

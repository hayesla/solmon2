import os 
import sys
import datetime
import numpy as np
#get path access to code in different folders
sys.path.append('/Users/laurahayes/Documents/solarmonitor2_0/solmon2/get_fits')
sys.path.append('/Users/laurahayes/Documents/solarmonitor2_0/solmon2/get_forecasts')
sys.path.append('/Users/laurahayes/Documents/solarmonitor2_0/solmon2/get_data_tests')
sys.path.append('/Users/laurahayes/Documents/solarmonitor2_0/solmon2/get_pngs')

from data_batch import get_summary
from get_forecast import get_mcstat_forecast, get_mcevol_forecast, get_noaa_probs
from get_goes_png_test import get_goes_plots
from get_ace_png_test import get_ace_pngs
from get_eve_png_test import get_eve_pngs
from get_all_fits import get_all_fits
#--------------------------------------------#
#date of interest
#date_search = datetime.datetime.strptime('2017-09-10 19:30', '%Y-%m-%d %H:%M')
date_search = datetime.datetime.utcnow() #- datetime.timedelta(days = 1)

#make directories to store data
output_path = '/Users/laurahayes/Documents/solarmonitor2_0/solmon2/data/'+date_search.strftime('%Y/%m/%d/')
png_path = output_path + 'pngs/'
fits_path = output_path + 'fits/'
meta_path = output_path + 'meta/'
for i in [png_path, fits_path, meta_path]:
	if not os.path.exists(i):
		os.makedirs(i)

#--------------------------------------------#

summary = get_summary(date_search)


#get forecasts and add to summary dataframe
#--------------------------------------------#
mc_evol = []
mc_stat = []
for i in range(len(summary)):
	me = get_mcevol_forecast(summary['MCINTOSH_TODAY'][i], summary['MCINTOSH_YDAY'][i])
	ms = get_mcstat_forecast(summary['MCINTOSH_TODAY'][i])

	mc_evol.append(me)
	mc_stat.append(ms)


#this will cause issues
'''noaa_names, noaa_data = get_noaa_probs()
noaa_name, noaa_probs = [], []
for i in range(len(noaa_names)):
	noaa_name.append(noaa_names[i][0])
	noaa_probs.append(noaa_data[i])


summary['FORE_MCSTAT'] = mc_stat
summary['FORE_MCEVOL'] = mc_evol
#summary['FORE_NOAA'] = noaa_probs'''

#-------------------------------------------#

get_goes_plots(date_search, png_path)
get_ace_pngs(date_search, png_path)
get_eve_pngs(date_search, png_path)



get_all_fits(date_search, fits_path)



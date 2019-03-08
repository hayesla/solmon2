import numpy as np 
import datetime
from get_srs_solmon import get_srs_from_datetime
from last_events2arm2 import events_arm
import pandas as pd 
from rot_location2 import rot_location



#---------------------------------------------------------#

# Functions Used in Script - will be moved to meta_utils.py          

#---------------------------------------------------------#



def greek_to_alpha(x):

	'''
	function to convert Hale class into alphabetical values

	Parameters
	----------

	x - list, array or pandas column

	Returns 
	-------

	x - list or array pandas column as abc ect
	'''

	for i in range(0, len(x)):
		if x[i] == 'ALPHA':
			x[i] = 'a'
		if x[i] == 'BETA':
			x[i] = 'b'
		if x[i] == 'BETA-GAMMA':
			x[i] = 'bg'
		if x[i] == 'DELTA':
			x[i] = 'd'
		if x[i] == 'BETA-DELTA':
			x[i] = 'bd'
		if x[i] == 'GAMMA-DELTA':
			x[i] = 'gd'
		if x[i] == 'BETA-GAMMA-DELTA':
			x[i] = 'bgd'	
	return x	



def put_srs_in_df(srs_test):

	'''
	function to put the SRS file format as a list of list of strings (I know gross)
	into a pandas DataFrame

	Parameters
	----------

	list of lists of strings read from the txt file


	Returns 
	-------

	pandas DataFrame of the  active regions in SRS file and their atributes

	'''

	for i in range(0, len(srs_test)-1):
		if srs_test[i][0:2] == 'I.':
			ind_start = i
		if srs_test[i][0:3] == 'IA.':
			ind_end = i
		if srs_test[i][0:3] == 'II.':
			ind_end_end = i


	header_srs = srs_test[ind_start+1].split()[0:-1] 
	header_srs2 = srs_test[ind_end+1].split()[0:2]

	data_srs = np.array([x.split() for x in srs_test[ind_start+2:ind_end]])
	if data_srs[0][0] == 'NONE':
		data_srs = None
	data_srs2 = np.array([x.split() for x in srs_test[ind_end+2:ind_end_end]])
	if data_srs2[0][0] == 'NONE':
		data_srs2 = None
	else:
		data_srs2 = data_srs2[:,0:2]

	data_test1 = pd.DataFrame(data_srs, columns = header_srs)
	#data_test2 = pd.DataFrame(data_srs2[0:,0:2], columns = header_srs2)
	data_test2 = pd.DataFrame(data_srs2, columns = header_srs2)
	
	#get into right format for McIntost Classification i.e. Zpc
	data_test1['Z'] = [x[0].upper() + x[1:3].lower() for x in data_test1['Z']]
	data_test1['MAG_AL'] = data_test1['MAG']
	greek_to_alpha(data_test1['MAG_AL'])

	data_test = pd.concat((data_test1, data_test2), sort = False).reset_index(drop = True)
	return data_test


def update_loc_events(date_search, srs_test, t_noaa):

	'''
	function to update the derived locations of the ARs from the SRS file to the current time
	Uses rot_location that rotates the location of the AR due to differential rotation of the Sun


	Parameters
	----------

	srs_test - the pandas Dataframe containing the SRS information
	t_noaa - issue date of the SRS information


	Returns 
	-------

	pandas DataFrame with updated location

	'''

	t_start_srs = datetime.datetime.strptime(t_noaa, '%Y %b %d %H:%M')
	t_end_srs = date_search 

	if len(srs_test) == 0:
		srs_test['NEW_LOCATION'], srs_test['NEW_X'], srs_test['NEW_Y'] = None, None, None
	else:
		srs_new_loc, srs_new_xy = [], []

		for i in range(len(srs_test)):
			new_loc, new_xy = rot_location(srs_test['LOCATION'].values[i], t_start_srs, t_end_srs)
			srs_new_loc.append(new_loc)
			srs_new_xy.append(new_xy)

		srs_test['NEW_LOCATION'] = srs_new_loc
		srs_test['NEW_X'], srs_test['NEW_Y'] = np.array(srs_new_xy)[:,0], np.array(srs_new_xy)[:,1]
	
	return srs_test




def distance(x1, x2, y1, y2):

	'''
	Function to return distance between two coordinates (x1, y1) to (x2, y2)
	
	Parameters
	----------

	x1, y1, x2, y2 - ints/floats

	Returns
	-------
	Distance between two points
	
	'''


	return np.sqrt( abs(x2 - x1)**2 + abs(y2 - y1)**2)


def find_AR_nmb_sol_mon(events_today, srs_test):

	'''
	Function to find the AR of the flaring events from the lsmal latest events based on the locations
	of the events and the AR properties from the SRS files.
	Finds the distances of each event to AR in SRS files and assigns the AR with closest distance within
	a max radius of 120 arcsec. If none found - a 'no_noaa' is assigned

	Parameters
	----------

	events_today - events DataFrame that includes the LMSAL latest events information
	srs_test - the SRS DataFrame

	Returns
	-------

	events_today with a new column of AR tag - 'NOAA NBR'


	'''
	if len(events_today) == 0 or len(srs_test) == 0:
		events_today['NOAA_NBR'] = None
	else:

		positions = []
		r_search = 120.

		for i in range(len(events_today)):
			r = distance(events_today['new_x'].values[i], srs_test['NEW_X'].values, events_today['new_y'].values[i], srs_test['NEW_Y'].values)
			#print(i, np.min(r))
			if np.min(r) < r_search:
				r_index = np.where(r == np.min(r))[0][0]

				positions.append(srs_test['NMBR'][r_index])
			else:
				positions.append('no_noaa')

		events_today['NOAA_NBR'] = positions
	return events_today


#-----------------------------------------------#


'''			Begin setup  			'''




def get_summary(date_search, out_dir):
	#get SRS information from today and yday and make all characters uppercase (why? cause solarmonitor does)
	srs_today = get_srs_from_datetime(date_search, out_dir).upper()
	srs_yday = get_srs_from_datetime(date_search - datetime.timedelta(days =1), out_dir).upper()

	#get events DataFrame from LMSAL
	events_today, events_yday = events_arm(date_search)



	#-------------------------------------------------#

	#issue times for today and yday - needed for update of location

	issued_today = srs_today.split('\n')[1][9:25]
	t_noaa_today = srs_today.split('\n')[1][9:20] + ' 00:00' 

	issued_yday = srs_yday.split('\n')[1][9:25]
	t_noaa_yday = srs_yday.split('\n')[1][9:20] + ' 00:00' 

	srs_today = put_srs_in_df(srs_today.split('\n'))
	srs_yday = put_srs_in_df(srs_yday.split('\n'))


	#update location of ARs to current time

	srs_today = update_loc_events(date_search, srs_today, t_noaa_today)
	srs_yday = update_loc_events(date_search, srs_yday, t_noaa_yday)

	#find AR of the latest events

	events_today = find_AR_nmb_sol_mon(events_today, srs_today)
	events_yday = find_AR_nmb_sol_mon(events_yday, srs_yday)

	#same as above but takes directly from LMSAL info rather than calculating it like 
	#like the way the current solar monitor does it

	other_nbr = []
	for i in range(len(events_today)):
		pos = events_today['Derived Position'][i].split()
		if len(pos) > 1:
			other_nbr.append(pos[2])
		else:
			other_nbr.append(None)

	other_nbr_day = []
	for i in range(len(events_yday)):
		pos = events_yday['Derived Position'][i].split()
		if len(pos) > 1:
			other_nbr_day.append(pos[2])
		else:
			other_nbr_day.append(None)


	#so to summarize events['NOAA_NMBR'] is the calculated position and events['NMBR'] are from LMSAL
	#this will be fixed after testing, but good to keep when comparing to solarmonitor.org/data
	events_today['NMBR'] = other_nbr
	events_yday['NMBR'] = other_nbr_day


	#fixing indices of DataFrame and droppings NaNs to be empty strings
	srs_today = srs_today.sort_values('NMBR').reset_index(drop = True).replace(np.nan, '', regex = True)
	srs_yday = srs_yday.sort_values('NMBR').reset_index(drop = True).replace(np.nan, '', regex = True)


	#----------------------------------------#

	# Now put all the info into a summary Dataframe - similar to summary structrue in IDL version

	date_str, ar_noaa, latest_pos, latest_loc, hale_t, hale_y, hale_t_alp, hale_y_alp, mcintosh_t, mcintosh_y, area_t, area_y, \
	no_sunspots_t, no_sunspots_y, flares_t, flares_y, flares_t_st, flares_t_gev, flares_y_st, flares_y_gev \
	 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],[]

	for i in range(len(srs_today)):
		t = srs_today.loc[i]
		y = srs_yday.loc[np.where(srs_yday['NMBR'] == t['NMBR'])[0]]
		if y.empty == True:
			y = pd.Series(index = t.index)
		else:
			y = pd.Series(y.values[0], index = t.index)
		f_t, f_t_st, f_t_gev = [], [], []
		f_y, f_y_st, f_y_gev = [], [], []
		if len(events_today) > 0:
			f_t = list(events_today[events_today['NMBR'] == t['NMBR']]['GOES Class'].values)
			f_t_st = list(events_today[events_today['NMBR'] == t['NMBR']]['Start'].values)
			f_t_gev = list(events_today[events_today['NMBR'] == t['NMBR']]['EName'].values)
		if len(events_yday) > 0:
			f_y = list(events_yday[events_yday['NMBR'] == t['NMBR']]['GOES Class'].values)
			f_y_st = list(events_yday[events_yday['NMBR'] == t['NMBR']]['Start'].values)
			f_y_gev = list(events_yday[events_yday['NMBR'] == t['NMBR']]['EName'].values)

		ar_noaa.append('1' + t['NMBR'])
		latest_pos.append(t['NEW_LOCATION'])
		latest_loc.append((int(t['NEW_X']), int(t['NEW_Y'])))
		hale_t.append(t['MAG'])
		hale_y.append(y['MAG'])
		hale_t_alp.append(t['MAG_AL'])
		hale_y_alp.append(y['MAG_AL'])
		mcintosh_t.append(t['Z'])
		mcintosh_y.append(y['Z'])
		area_t.append(t['AREA'])
		area_y.append(y['AREA'])
		no_sunspots_t.append(t['NN'])
		no_sunspots_y.append(y['NN'])
		flares_t.append(f_t)
		flares_y.append(f_y)
		flares_t_st.append(f_t_st)
		flares_t_gev.append(f_t_gev)
		flares_y_st.append(f_y_st)
		flares_y_gev.append(f_y_gev)
		date_str.append(date_search.strftime('%Y/%m/%d %H:%M:%S'))

	summary_dict = {'AR_NUM' : ar_noaa,
					'LATEST_POS' : latest_pos,
					'LATEST_LOC' : latest_loc,
					'HALE_TODAY' : hale_t,
					'HALE_YDAY' :  hale_y,
					'HALE_TODAY_AL' : hale_t_alp,
					'HALE_YDAY_AL' :  hale_y_alp,
					'MCINTOSH_TODAY': mcintosh_t,
					'MCINTOSH_YDAY' : mcintosh_y,
					'AREA_T' : area_t, 
					'AREA_Y' : area_y,
					'NO_SUNSPOT_T' : no_sunspots_t, 
					'NO_SUNSPOT_Y' : no_sunspots_y, 
					'FLARES_T' : flares_t, 
					'FLARES_Y' : flares_y, 
					'FLARES_T_TS': flares_t_st, 
					'FLARES_T_GEV': flares_t_gev,
					'FLARES_Y_TS': flares_y_st,
					'FLARES_Y_GEV': flares_y_gev,
					'DATE_SEARCH': date_str}

	summary = pd.DataFrame(summary_dict).replace(np.nan, '')
	#print(summary)
	return summary


#----------------------------------------#
#date of interest
'''
date_search = datetime.datetime.strptime('2016-03-18 19:30', '%Y-%m-%d %H:%M')
date_search = datetime.datetime.utcnow()

summary = get_summary(date_search)
print(summary)'''

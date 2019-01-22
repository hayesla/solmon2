import numpy as np 
import datetime
from get_srs_solmon import get_srs_from_datetime
from last_events2arm2 import events_arm
import pandas as pd 
from rot_location2 import rot_location


date_search = datetime.datetime.strptime('2013-10-26 23:35', '%Y-%m-%d %H:%M')

srs_today = get_srs_from_datetime(date_search).upper()
srs_yday = get_srs_from_datetime(date_search - datetime.timedelta(days =1)).upper()



events_today, events_yday = events_arm(date_search)

def greek_to_alpha(x):
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
	for i in range(0, len(srs_test)-1):
		if srs_test[i][0:2] == 'I.':
			ind_start = i
		if srs_test[i][0:3] == 'IA.':
			ind_end = i
		if srs_test[i][0:3] == 'II.':
			ind_end_end = i


	header_srs = srs_test[ind_start+1].split()[0:-1] 

	data_srs = np.array([x.split() for x in srs_test[ind_start+2:ind_end]])
	if data_srs[0][0] == 'NONE':
		data_srs = np.array([len(header_srs)*['NONE']])
	
	data_test = pd.DataFrame(data_srs, columns = header_srs)



	#get into right format for McIntost Classification i.e. Zpc
	data_test['Z'] = [x[0].upper() + x[1:3].lower() for x in data_test['Z']]
	data_test['MAG_AL'] = data_test['MAG']
	greek_to_alpha(data_test['MAG_AL'])
	return data_test


def put_srs_in_df2(srs_test):
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
		data_srs = np.array([len(header_srs)*['NONE']])
	
	data_srs2 = np.array([x.split() for x in srs_test[ind_end+2:ind_end_end]])
	if data_srs2[0][0] == 'NONE':
		data_srs2 = np.array([len(header_srs)*['NONE']])

	data_test1 = pd.DataFrame(data_srs, columns = header_srs)
	data_test2 = pd.DataFrame(data_srs2[0:,0:2], columns = header_srs2)

	
	#get into right format for McIntost Classification i.e. Zpc
	data_test1['Z'] = [x[0].upper() + x[1:3].lower() for x in data_test1['Z']]
	data_test1['MAG_AL'] = data_test1['MAG']
	greek_to_alpha(data_test1['MAG_AL'])

	data_test = pd.concat((data_test1, data_test2), sort = False).reset_index(drop = True)
	return data_test


srs_test = put_srs_in_df2(srs_today.split('\n'))
issued = srs_today[31:45]+':'+srs_today[45:47]
t_noaa = srs_today[31:42] + ' 00:00' 

t_start_srs = datetime.datetime.strptime(t_noaa, '%Y %b %d %H:%M')
t_end_srs = date_search 


srs_new_loc, srs_new_xy = [], []

for i in range(len(srs_test)):
	new_loc, new_xy = rot_location(srs_test['LOCATION'].values[i], t_start_srs, t_end_srs)
	srs_new_loc.append(new_loc)
	srs_new_xy.append(new_xy)

srs_test['NEW_LOCATION'] = srs_new_loc
srs_test['NEW_X'], srs_test['NEW_Y'] = np.array(srs_new_xy)[:,0], np.array(srs_new_xy)[:,1]


#identify NOAA region closest to each event

def distance(x1, x2, y1, y2):
	return np.sqrt( abs(x2 - x1)**2 + abs(y2 - y1)**2)


#events_today = events_yday
#search area in arcsec
positions = []
r_search = 120.

for i in range(len(events_today)):
	r = distance(events_today['new_x'].values[i], srs_test['NEW_X'].values, events_today['new_y'].values[i], srs_test['NEW_Y'].values)
	print(i, np.min(r))
	if np.min(r) < r_search:
		r_index = np.where(r == np.min(r))[0][0]

		positions.append(srs_test['NMBR'][r_index])
	else:
		positions.append('no_noaa')

events_today['NOAA_NBR'] = positions






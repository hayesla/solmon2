import numpy as np 
import datetime
from get_srs_solmon import get_srs_from_datetime
from last_events2arm2 import events_arm
import pandas as pd 
from rot_location2 import rot_location


date_search = datetime.datetime.strptime('2016-03-18 19:30', '%Y-%m-%d %H:%M')

srs_today = get_srs_from_datetime(date_search).upper()
srs_yday = get_srs_from_datetime(date_search - datetime.timedelta(days =1)).upper()



events_today, events_yday = events_arm(date_search)
events_today = events_today.reset_index(drop = True)
events_yday = events_yday.reset_index(drop = True)

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
		#data_srs = np.array([len(header_srs)*['NONE']])
		data_srs2 = None
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


issued_today = srs_today.split('\n')[1][9:25]
t_noaa_today = srs_today.split('\n')[1][9:20] + ' 00:00' 

issued_yday = srs_yday.split('\n')[1][9:25]
t_noaa_yday = srs_yday.split('\n')[1][9:20] + ' 00:00' 

srs_today = put_srs_in_df2(srs_today.split('\n'))
srs_yday = put_srs_in_df2(srs_yday.split('\n'))





def update_loc_events(srs_test, t_noaa):
	t_start_srs = datetime.datetime.strptime(t_noaa, '%Y %b %d %H:%M')
	t_end_srs = date_search 

	srs_new_loc, srs_new_xy = [], []

	for i in range(len(srs_test)):
		new_loc, new_xy = rot_location(srs_test['LOCATION'].values[i], t_start_srs, t_end_srs)
		srs_new_loc.append(new_loc)
		srs_new_xy.append(new_xy)

	srs_test['NEW_LOCATION'] = srs_new_loc
	srs_test['NEW_X'], srs_test['NEW_Y'] = np.array(srs_new_xy)[:,0], np.array(srs_new_xy)[:,1]
	return srs_test



srs_today = update_loc_events(srs_today, t_noaa_today)
srs_yday = update_loc_events(srs_yday, t_noaa_yday)


#identify NOAA region closest to each event

def distance(x1, x2, y1, y2):
	return np.sqrt( abs(x2 - x1)**2 + abs(y2 - y1)**2)


#events_today = events_yday
#search area in arcsec
def find_AR_nmb_sol_mon(events_today, srs_test):
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
	return events_today

events_today = find_AR_nmb_sol_mon(events_today, srs_today)
events_yday = find_AR_nmb_sol_mon(events_yday, srs_yday)

other_nbr = []
for i in range(len(events_today)):
	other_nbr.append(events_today['Derived Position'][i].split()[2])

other_nbr_day = []
for i in range(len(events_yday)):
	print(events_yday['Derived Position'][i])
	other_nbr_day.append(events_yday['Derived Position'][i].split()[2])

events_today['NMBR'] = other_nbr
events_yday['NMBR'] = other_nbr_day

srs_today = srs_today.sort_values('NMBR').reset_index(drop = True).replace(np.nan, '', regex = True)
srs_yday = srs_yday.sort_values('NMBR').reset_index(drop = True).replace(np.nan, '', regex = True)

print(events_today.sort_values('NOAA_NBR'))

print(events_yday.sort_values('NOAA_NBR'))

print(srs_today)
print(srs_yday)


#----------------------------------------#

ar_noaa, latest_pos, latest_loc, hale_t, hale_y, mcintosh_t, mcintosh_y, area_t, area_y, no_sunspots_t, no_sunspots_y, flares_t, flares_y = [], [], [], [], [], [], [], [], [], [], [], [], []
for i in range(len(srs_today)):
	t = srs_today.loc[i]
	y = srs_yday.loc[np.where(srs_yday['NMBR'] == t['NMBR'])[0]]
	if y.empty == True:
		y = pd.Series(index = t.index)
	else:
		y = pd.Series(y.values[0], index = t.index)
	f_t = list(events_today[events_today['NMBR'] == t['NMBR']]['GOES Class'].values)
	f_y = list(events_yday[events_yday['NMBR'] == t['NMBR']]['GOES Class'].values)


	ar_noaa.append('1' + t['NMBR'])
	latest_pos.append(t['NEW_LOCATION'])
	latest_loc.append((int(t['NEW_X']), int(t['NEW_Y'])))
	hale_t.append(t['MAG'])
	hale_y.append(y['MAG'])
	mcintosh_t.append(t['Z'])
	mcintosh_y.append(y['Z'])
	area_t.append(t['AREA'])
	area_y.append(y['AREA'])
	no_sunspots_t.append(t['NN'])
	no_sunspots_y.append(y['NN'])
	flares_t.append(f_t)
	flares_y.append(f_y)

summary_dict = {'AR_NUM' : ar_noaa,
				'LATEST_POS' : latest_pos,
				'LATEST_LOC' : latest_loc,
				'HALE_TODAY' : hale_t,
				'HALE_YDAY' :  hale_y,
				'MCINTOSH_TODAY': mcintosh_t,
				'MCINTOSH_YDAY' : mcintosh_y,
				'AREA_T' : area_t, 
				'AREA_Y' : area_y,
				'NO_SUNSPOT_T' : no_sunspots_t, 
				'NO_SUNSPOT_Y' : no_sunspots_y, 
				'FLARES_T' : flares_t, 
				'FLARES_Y' : flares_y}

summary = pd.DataFrame(summary_dict).replace(np.nan, '')
print(summary)



#----------------------------------------#

'''

for i in range(len(srs_today)):
	t = srs_today.loc[i]
	y = srs_yday.loc[np.where(srs_yday['NMBR'] == t['NMBR'])[0][0]]
	flares_t = list(events_today[events_today['NMBR'] == t['NMBR']]['GOES Class'].values)
	flares_y = list(events_yday[events_yday['NMBR'] == t['NMBR']]['GOES Class'].values)

	str_to_print =(t['NMBR'] + ' ' + t['NEW_LOCATION'] +' ' +t['Z'] +'/' + y['Z'] + ' '+ t['MAG_AL'] + '/' + y['MAG_AL'] + ' ' + t['AREA'] + '/' + y['AREA'] + ' '+  t['NN'] + '/' + y['NN'])
	flare_today_str = ''




	flare_yday_str = ''
	if len(flares_t) > 0:
		for j in range(len(flares_t)):
			flare_today_str = flare_today_str + flares_t[j] + ' '
	else:
		flare_today_str = '- '
	if len(flares_y)>0:

		for j in range(len(flares_y)):
			flare_yday_str = flare_yday_str + flares_y[j] + ' '

	else:
		flare_yday_str = '-'

	print(str_to_print + ' '+flare_today_str + '/ ' + flare_yday_str)


for i in range(len(srs_today)):
	t = srs_today.loc[i]
	y = srs_yday.loc[np.where(srs_yday['NMBR'] == t['NMBR'])[0][0]]


'''

'''
#arm ar titles
for i in range(len(srs_test)):
	print('1' + srs_test['NMBR'][i] + ' NOAA 1' + srs_test['NMBR'][i] + ' - ' + srs_test['NEW_LOCATION'][i] + 
		  ' (' + str(int(srs_test['NEW_X'][i])) + '",' + str(int(srs_test['NEW_Y'][i])) + '")' + ' - ' + srs_test['MAG'][i] )


#arm ar summary
fl_class, ename = [], []
for i in range(len(srs_today)):

	fl_class.append(list(events_today[events_today['NOAA_NBR'] == srs_today['NMBR'][i]]['GOES Class'].values))
	ename.append(list(events_today[events_today['NOAA_NBR'] == srs_today['NMBR'][i]]['EName'].values))

summary = srs_today
summary['EName'] = ename
summary['GOES Class'] = fl_class


base_url = 'http://www.lmsal.com/solarsoft/latest_events_archive/events_summary/'+date_search.strftime('%Y/%m/%d/')#2013/10/28/gev_20131028_0432/index.html'
for i in range(len(summary)):
	str_to_print = ('1'+summary['NMBR'][i] + ' ' + summary['NEW_LOCATION'][i] + ' (' + str(int(summary['NEW_X'][i])) + '",' + str(int(summary['NEW_Y'][i])) + '") ' + summary['MAG_AL'][i] + '/ ' + summary['Z'][i] + '/ ' + summary['AREA'][i] + '/ ' + summary['NN'][i] + '/ ' )
	#print(str_to_print)
	
	if len(summary['EName'][i])>0:
		#print(i)
		for j in range(len(summary['EName'][i])):
			str_to_print = (str_to_print + base_url + summary['EName'][i][j] + '/index.html ' + summary['GOES Class'][i][j]) + ' '


	print(str_to_print)


'''
'''
noaa_name, latest_location, hale_class = [], [], []
for i in range(len(srs_today)):
	prev = srs_yday[srs_yday['NMBR'] == srs_today['NMBR'][i]] 
	noaa_name.append(srs_today['NMBR'][i])
	latest_location.append(srs_today['NEW_LOCATION'][i])
	#print(type(prev['Z']))
	if type(prev['Z'].values[0])!= str:
		hale_class.append(srs_today['Z'][i] + '/-')
	else:
		hale_class.append(srs_today['Z'][i] + '/' + prev['Z'].values[0])



'''

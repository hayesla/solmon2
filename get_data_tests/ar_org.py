from rot_location2 import rot_location
from last_events2arm import events_test
from get_srs_function import get_srs_structure
import datetime
import numpy as np

class date_struct():
	def __init__(self, date = 'now'):
		"""
		Creates a date object that includes directory format and previous and next dates.
		If no date is given, the object returns the current UTC time now.
		Input must be a date format in YYMMDD
		"""
		if date == 'now':
			self.utc_date = datetime.datetime.utcnow()
		else:
			try:
				self.utc_date = datetime.datetime.strptime(date + ' 23:59', '%Y%m%d %H:%M') 
			except:
				print('date input must be a str in yymmdd format, e.g. 20181128')


		self.date_dir = self.utc_date.strftime('%Y/%m/%d') 			#yyyy/mm/dd
		self.date = self.utc_date.strftime('%Y%m%d') 				#yyyymmdd
		self.year = self.utc_date.strftime('%Y')
		self.month = self.utc_date.strftime('%m')
		self.day = self.utc_date.strftime('%d')
		self.utc = self.utc_date.strftime('%d-%b-%Y %H:%M')			#dd-mmm-yyyy HH:MM
		self.prev_date = (self.utc_date - datetime.timedelta(days = 1))
		self.next_date = (self.utc_date + datetime.timedelta(days = 1))


date_time = date_struct(date = '20131028')


srs_struct, srs_raw = get_srs_structure(date_time)
events = events_test(date_time)

t_srs = srs_raw[1].split()[1:5]
t_srs = datetime.datetime.strptime(t_srs[0]+t_srs[1]+t_srs[2]+'00:00', '%Y%b%d%H:%M')

srs_locs, srs_xy = [], []
for i in range(len(srs_struct)):
	new_loc, new_xy = rot_location(srs_struct['LOCATION'].values[i], t_srs, date_time.utc_date)
	srs_locs.append(new_loc)
	srs_xy.append(new_xy)

srs_xy = np.array(srs_xy)
srs_struct['new_x'] = srs_xy[:,0]
srs_struct['new_y'] = srs_xy[:,1]
srs_struct['new_loc'] = srs_locs

#identify NOAA region closest to each event

def distance(x1, x2, y1, y2):
	return np.sqrt( abs(x2 - x1)**2 + abs(y2 - y1)**2)

#search area in arcsec
positions = []

r_search = 120.
for i in range(len(events)):
	r = distance(events['new_x'].values[i], srs_struct['new_x'].values, events['new_y'].values[i], srs_struct['new_y'].values)
	print(i, np.min(r))
	if np.min(r) < r_search:
		r_index = np.where(r == np.min(r))[0][0]
		#print(i, r_index)


		#print(r_index, srs_struct['LOCATION'][r_index], srs_struct['NMBR'][r_index], events['GOES Class'][i])
		positions.append(srs_struct['NMBR'][r_index])
	else:
		positions.append('no_noaa')

events['NOAA_NBR'] = positions
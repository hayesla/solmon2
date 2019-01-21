import datetime
import numpy as np 
import astropy.units as u
from astropy.coordinates import SkyCoord
from sunpy.coordinates import frames
from sunpy.physics.differential_rotation import diff_rot 

def rot_location(loc_test, ts, te):
	# example inputs to function
	'''
	ts = datetime.datetime.strptime('2018-12-02 10:22', '%Y-%m-%d %H:%M')
	te = datetime.datetime.strptime('2018-12-04 09:27', '%Y-%m-%d %H:%M')

	loc_test = 'S44W42

	'''

	#time difference in seconds in astropy.units.Quantity
	dt = (te - ts).total_seconds()*u.s

	#lat and lon values in astropy.units.Quantity
	lat = int(loc_test[1:3])*u.deg
	lon = int(loc_test[4:6])*u.deg

	#positive N, negative S, positive W, negative E 
	if loc_test[0] == 'S':
		lat = -lat
	if loc_test[3] == 'E':
		lon = -lon

	#convert into SkyCoord sunpy coordinates
	coords_old = SkyCoord(lon, lat, frame = frames.HeliographicStonyhurst, obstime = ts) 

	#calculate rotation of lon (i.e. x) after time dt
	new_lon = (round(diff_rot(dt, lat).value) + lon.value)*u.deg

	#check is regions are off limb - if so set to 91 (west limb) or -91 (east limb)
	if new_lon.value > 90:
		new_lon = 91*u.deg
	if new_lon.value < -90:
		new_lon = -91*u.deg

	#new Skycoord after time dt
	coords_new = SkyCoord(new_lon, lat, frame = frames.HeliographicStonyhurst, obstime = te)


	#convert back to N, S, E, W format

	if coords_new.lat.value <= 0:
		lat_end = 'S'+ str('%02d' % np.abs(int(coords_new.lat.value)))

	elif coords_new.lat.value > 0:
		lat_end = 'N' + str('%02d' % np.abs(int(coords_new.lat.value)))
	else:
		print('problem')

	if coords_new.lon.value  <= 0:
		lon_end = 'E' + str('%02d' % np.abs(int(coords_new.lon.value)))
	elif coords_new.lon.value > 0:
		lon_end = 'W' + str('%02d' % np.abs(int(coords_new.lon.value)))
	else:
		print('problem')

	loc_end = lat_end + lon_end

	coords_new_hpc = coords_new.transform_to(frames.Helioprojective)
	solar_xy = [coords_new_hpc.Tx.value, coords_new_hpc.Ty.value]
	return loc_end, solar_xy
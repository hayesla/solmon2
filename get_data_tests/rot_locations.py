import datetime
import numpy as np 
import astropy.units as u
from astropy.coordinates import SkyCoord
from sunpy.coordinates import frames


ts = datetime.datetime.strptime('2018-12-02 10:22', '%Y-%m-%d %H:%M')
te = datetime.datetime.strptime('2018-12-04 09:27', '%Y-%m-%d %H:%M')

dt = (te - ts).total_seconds() / 86400

loc_test = 'S44W42'

lat = int(loc_test[1:3])
lon = int(loc_test[4:6])


#positive N, negative S, positive W, negative E 
if loc_test[0] == 'S':
	lat = -lat
if loc_test[3] == 'E':
	lon = -lon

def diff_rot(ddays, latitude, allen = False, snodgrass = False):
	'''
	computes the differential rotation of the Sun
	same as the SSW idl code diff_rot.pro
	Defalt here is Howard et al. 
	Can also use the Allen, 1973 or Snodgrass 1990
	'''


	latitude = float(latitude)
	sin2l = np.sin(np.deg2rad(latitude))**2
	sin4l = sin2l*sin2l

	if allen == True:
		rotation = ddays*(14.44 - 3.*sin2l)

	elif snodgrass == True:
		rotation = ddays*(14.252 - 1.678*sin2l - 2.401*sin4l)

	else:	

		rotation = (1.e-6)*ddays*(2.894 - 0.428*sin2l - 0.37*sin4l)*24.*3600./ np.deg2rad(1)


	return rotation


#rotate coordinates by dt
lon = int(round(diff_rot(dt, lat)+ lon))

#check is off limb, and if so set to 91 (west limb)/-91 (east limb)
if lon > 90:
	lon = 91
if lon < -90:
	lon = -91

#convert back to N, S, E, W format
if lat <= 0:
	lat_end = 'S'+ str(np.abs(lat))
elif lat > 0:
	lat_end = 'N' + str(np.abs(lat))
else:
	print('problem')

if lon <= 0:
	lon_end = 'E' + str(np.abs(lon))
elif lon > 0:
	lon_end = 'W' + str(np.abs(lon))
else:
	print('problem')

loc_end = lat_end + lon_end

coords = SkyCoord(lon*u.deg, lat*u.deg, frame = frames.HeliographicStonyhurst, obstime = te)
hpc_coords =  coords.tranform_to(frames.Helioprojective)

print(loc_end)

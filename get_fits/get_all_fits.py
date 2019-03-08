from get_gong_farside_mag import get_gong_fs
from get_gong import get_gong_mag, get_gong_igram
from get_halpha import get_halpha
from get_sdo_fits_test import get_aia_fido
from swap_data import get_swap
from hmi_tests2 import get_hmi_m 
from xrt_tests import get_xrt
from get_stereo import get_stereo


def get_all_fits(date_search, fits_path):
	"""
	Downloads fits files that solarmonitor requires and saves them into associated directories
	
	Parameters
	----------
	date_search : datetime object 
		time of interest
	fits_path : str
		path to where fits files are saved. eg: ~/data/fits/

	Notes
	-----
	Based mainly on solarmonitor written in IDL

	TODO
	-----
	Writes success/fails to log file
	Include tests
	"""

	#GONE Farside
	get_gong_fs(date_search, fits_path + '/GONG/')
	#GONG magnetic field gradeint
	get_gong_mag(date_search, fits_path + '/GONG/')
	#GONG intensity gram
	get_gong_igram(date_search, fits_path + '/GONG/')
	#BBSO Halpha observations
	get_halpha(date_search, fits_path + '/HALPHA/')
	#AIA files
	get_aia_fido(date_search, fits_path + '/AIA/')
	#PROBA2 SWAP
	get_swap(date_search, fits_path + '/SWAP/')
	#SDO HMI data - get NRT data 
	get_hmi_m(date_search, fits_path + '/HMI/')
	#HINODE XRT data
	get_xrt(date_search, fits_path + '/XRT/')
	#STEREO A and B data
	get_stereo(date_search, fits_path + '/STEREO/')


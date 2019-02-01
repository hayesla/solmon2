import numpy as np 
import datetime
import os


from get_gong_farside_mag import get_gong_fs
from get_gong import get_gong_mag, get_gong_igram
from get_halpha import get_halpha
from get_sdo_fits_test import get_aia_fido
from swap_data import get_swap
from hmi_tests2 import get_hmi_m 
from xrt_tests import get_xrt
from get_stereo import get_stereo



def get_all_fits(date_search, fits_path):

	#get gong data
	get_gong_fs(date_search, fits_path + '/GONG/')
	get_gong_mag(date_search, fits_path + '/GONG/')
	get_gong_igram(date_search, fits_path + '/GONG/')
	get_halpha(date_search, fits_path + '/HALPHA/')
	get_aia_fido(date_search, fits_path + '/AIA/')
	get_swap(date_search, fits_path + '/SWAP/')
	get_hmi_m(date_search, fits_path + '/HMI/')
	get_xrt(date_search, fits_path + '/XRT/')
	get_stereo(date_search, fits_path + '/STEREO/')
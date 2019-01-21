from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u


def get_aia_fido(output_path = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/{instrument}/'):
	
	#get utc time rounded down to the previous hour
	time_now = datetime.datetime.utcnow().replace(microsecond = 0, second = 0, minute = 0)

	#time to search for available fits files
	search_time = a.Time( (time_now-datetime.timedelta(hours  = 10)).strftime('%Y/%m/%d %H:%M'), time_now.strftime('%Y/%m/%d %H:%M') )


	#search for all aia fits files from the timerange in search_time
	aia_search = Fido.search(search_time, a.Instrument('aia'), a.vso.Sample(1*u.hour))

	#get the latest hour available - the last 10 files to include all aia fits
	aia_files = aia_search[0, -10:]

	#download them into output_path
	#download aia hold the path to download file path
	download_aia = Fido.fetch(aia_files, path = output_path)
	return download_aia



def get_aia_vso(output_path = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/{instrument}/'):
	
	client = vso.VSOClient()


	#search_time = a.Time( '2019-01-12 00:00', '2019-01-15 00:00' )
	#get utc time rounded down to the previous hour
	time_now = datetime.datetime.utcnow().replace(microsecond = 0, second = 0, minute = 0)

	#time to search for available fits files
	search_time = a.Time( (time_now-datetime.timedelta(hours  = 10)).strftime('%Y/%m/%d %H:%M'), time_now.strftime('%Y/%m/%d %H:%M') )

	#using the VSO client rather than FIDO
	result_aia = client.search(
		search_time,
		a.vso.Instrument('AIA'), 
		a.vso.Sample(1*u.hour))

	download_aia = client.fetch(result_aia[-10:], path = output_path)
	return download_aia
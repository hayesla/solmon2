from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u
import os
import urllib
from bs4 import BeautifulSoup 
from sunpy.net import jsoc
import drms

def get_hmi_m(time_now, output_path):
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	#output_path = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/HMI/'
	#get utc time rounded down to the previous hour
	#time_now = datetime.datetime.utcnow().replace(microsecond = 0, second = 0, minute = 0)
	#time_now = time_now2 - datetime.timedelta(hours = 2)
	time_now = time_now.replace(microsecond = 0, second = 0, minute = 0)
	#time to search for available fits files

	base_url = 'http://jsoc.stanford.edu/data/hmi/fits/'
	date_url = base_url + str(time_now.year)+'/' + str('%02d' % time_now.month)+'/'+ str('%02d' %time_now.day) + '/'

	#fname = 'hmi.M_720s.'+ time_now.strftime('%Y%m%d_%H%M%S') + '_TAI'

	#full_url = os.path.join(date_url, fname)



	test = urllib.request.urlopen(date_url)
	soup = BeautifulSoup(test, features="lxml")

	fits_links = []
	for link in soup.findAll('a'):
		if link.get('href')[-4:] == 'fits':
			fits_links.append(date_url  + link.get('href'))


	output_path2 = output_path + link.get('href')
	#output_path2 = output_path + fits_links[-1].split('/')[-1]
	urllib.request.urlretrieve(fits_links[-1], output_path2)
	if os.path.exists(output_path2):
		print('hmi_success')


def hmi_fido(output_path = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/fits_tests/HMI/'):
	res = Fido.search(a.jsoc.Time('2019-01-15T01:00:00', '2019-01-15T02:00:00'), 
		a.jsoc.Series('hmi.Ic_noLimbDark_720s_nrt'), a.jsoc.Notify('hayesla@tcd.ie'))

	dow = Fido.fetch(res, output_path)


def new_hmi_jsoc(output_path):

	#get utc time rounded down to the previous hour
	time_now = datetime.datetime.utcnow().replace(microsecond = 0, second = 0, minute = 0)

	#time to search for available fits files
	search_time = a.jsoc.Time( (time_now-datetime.timedelta(hours  = 2)).strftime('%Y/%m/%d %H:%M'), time_now.strftime('%Y/%m/%d %H:%M') )


	res = Fido.search(search_time, 
			a.jsoc.Series('hmi.Ic_noLimbDark_720s_nrt'), a.jsoc.Notify('hayesla@tcd.ie'))

	hmi_files = res[0, -2:]

	#download them into output_path
	#download aia hold the path to download file path
	download_hmi = Fido.fetch(hmi_files, path = output_path)

def hmi_jsoc():

	client = jsoc.JSOCClient()  
	res = client.search(a.jsoc.Time('2019-01-16T00:00:00', '2019-01-17T01:00:00'),
                    a.jsoc.Series('hmi.Ic_noLimbDark_720s_nrt'),	a.jsoc.Notify('hayesla@tcd.ie'))  

	requests = client.request_data(res)  


def hmi_drms_chmi():
	c = drms.Client(email='hayesla@tcd.ie', verbose=True)
	ds = 'hmi.Ic_noLimbDark_720s_nrt[2019.01.17_10:00_TAI]'
	r = c.export(ds, method='url', protocol='fits')
	r.wait()
	r.status
	r.request_url
	r.download(out_dir)


def hmi_drms_shmi():
	c = drms.Client(email='hayesla@tcd.ie', verbose=True)
	ds = 'hmi.M_720s_nrt[2019.01.17_10:00_TAI]'
	r = c.export(ds, method='url', protocol='fits')
	r.wait()
	r.status
	r.request_url
	r.download(out_dir)



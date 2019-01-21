import datetime
import urllib
from urllib.error import HTTPError, URLError

########################################
#these will be moved to utils in future#
########################################


def check_servers_online(website_url):
	check = 0
	try:
		res = urllib.request.urlopen(website_url)
		check = 1
	except HTTPError as e:
		print(website_url, ' Server cant be accessed, ', str(e.code))
	except URLError as e:
		print(website_url, 'Server cant be accessed, ', str(e.reason))

	return check

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
				self.utc_date = datetime.datetime.strptime(date, '%Y%m%d') 
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


##############################################
#	Actual code part 						 #
#											 #
##############################################
date_time = date_struct()
date = date_time.date

output_path = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/png_tests/'

#out_goes = output_path + '/pngs/goes/'

server = 'http://lasp.colorado.edu/eve/data_access/quicklook/quicklook_data/'

eve = server+'latest_3day.png'


eve_save = output_path + 'eve_'+date+'.gif'


cc = check_servers_online(server)

if cc == 1:
	urllib.request.urlretrieve(eve, eve_save)




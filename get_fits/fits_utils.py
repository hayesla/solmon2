
import urllib
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup , SoupStrainer
import re
import datetime

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


def list_path_files(url_path, file_name):
	test = urllib.request.urlopen(url_path)
	soup = BeautifulSoup(test, features="lxml")

	fits_links = []
	for link in soup.findAll('a'):
		if link.get('href') is not None and link.get('href').find(file_name) != -1:
			fits_links.append(url_path + link.get('href').split('/')[-1]) 
			#split is put there as bbso seems to be linking filename with the path links also?

	return fits_links

def find_file_times(file_name):
	t = re.search('\d{8}_\d{6}', file_name).group()
	tt = datetime.datetime.strptime(t, '%Y%m%d_%H%M%S')
	return tt

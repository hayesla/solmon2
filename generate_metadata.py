import datetime

def make_arm_times(date_search, output_path):
	"""
	writes the time solarmonitor is ran for

	Parameters
	----------
	date_search : datetime object

	"""

	file_path = output_path + 'arm_last_update_'+ date_search.strftime('%Y%m%d') +'.txt'
	file_to_write = open(file_path, 'a')
	str_to_print = date_search.strftime('%d-%b-%Y %H:%M UT')
	file_to_write.write(str_to_print)
	file_to_write.close()



def make_arm_ar_titles(date_search, summary, output_path):
	"""
	writes meta data for arm_ar_titles.txt
	legacy from solarmonitor.org

	Parameters
	----------
	summary - pandas DataFrame
		arm summary of ARs and events

	"""

	file_path = output_path + 'arm_ar_titles_'+ date_search.strftime('%Y%m%d') +'.txt'

	file_to_write = open(file_path, 'w')

	for i in range(len(summary)):
		#make all elements in each row a str
		summary_data = summary.loc[i].astype('str')

		str_to_print = summary_data['AR_NUM']  + ' NOAA ' + summary_data['AR_NUM'] + ' - ' \
				+  summary_data['LATEST_POS'] + ' ' +  summary_data['LATEST_LOC'] + \
				' - ' +  summary_data['HALE_TODAY'].title()

		file_to_write.write('%s \n' %str_to_print)

	file_to_write.close()


def make_arm_ar_table(date_search, summary, output_path):
	"""
	creates txt file containing info of AR and associated flares 
	legacy from solarmonitor.org

	Parameters
	----------
	summary - pandas DataFrame
		arm summary of ARs and events

	"""
	file_path = output_path + 'arm_ar_summary_'+ date_search.strftime('%Y%m%d') +'.txt'

	file_to_write = open(file_path, 'w')
	lmsal_url_t = 'http://www.lmsal.com/solarsoft/latest_events_archive/events_summary/' + date_search.strftime('%Y/%m/%d/')
	lmsal_url_y = 'http://www.lmsal.com/solarsoft/latest_events_archive/events_summary/' + (date_search - datetime.timedelta(days =1)).strftime('%Y/%m/%d/')
	for i in range(len(summary)):

		summary_data = summary.loc[i]
		summary_str = summary_data.astype('str')

		str_to_print = summary_str['AR_NUM'] + ' ' + summary_str['LATEST_POS'] + ' ' + summary_str['LATEST_LOC'] + \
					   ' ' + summary_str['HALE_TODAY_AL'] + '/' + summary_str['HALE_YDAY_AL'] + \
					   ' ' + summary_str['MCINTOSH_TODAY'].title() + '/'+ summary_str['MCINTOSH_YDAY'].title() + \
					   ' ' + summary_str['AREA_T'] + '/' + summary_str['AREA_Y'] + \
					   ' ' + summary_str['NO_SUNSPOT_T'] + '/' + summary_str['NO_SUNSPOT_Y'] + ' '
		if len(summary_data['FLARES_T']) == 0 and len(summary_data['FLARES_Y']) == 0:
			str_to_print = str_to_print + '- '
		else:

			for f_t in range(len(summary_data['FLARES_T'])):
				str_to_print =  str_to_print +  lmsal_url_t + summary.loc[i]['FLARES_T_GEV'][f_t] + '/index.html' + \
				' ' + summary_data['FLARES_T'][f_t] + ' ('+summary_data['FLARES_T_TS'][f_t][11:16] + ')' + ' '

			str_to_print = str_to_print + '/ '

			for f_y in range(len(summary_data['FLARES_Y'])):
				str_to_print =  str_to_print +  lmsal_url_y  + summary.loc[i]['FLARES_Y_GEV'][f_y] + '/index.html' + \
				' ' + summary_data['FLARES_Y'][f_y] + ' ('+summary_data['FLARES_Y_TS'][f_y][11:16] + ')' + ' '


		file_to_write.write('%s \n' %str_to_print)

	file_to_write.close()



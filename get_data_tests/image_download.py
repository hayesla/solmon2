from sunpy.net import Fido, attrs as a 
import datetime

time_now = datetime.datetime.utcnow()


search_time = a.Time( (time_now-datetime.timedelta(hours  = 1)).strftime('%Y/%m/%d %H:%M'), time_now.strftime('%Y/%m/%d %H:%M') )

aia_search = Fido.search(search_time, a.Instrument('aia'))
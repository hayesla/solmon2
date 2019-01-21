from sunpy.net import Fido, attrs as a, vso
import datetime
from astropy import units as u

#get utc time rounded down to the previous hour
time_now = datetime.datetime.utcnow().replace(microsecond = 0, second = 0, minute = 0)

#time to search for available fits files
search_time = a.Time( (time_now-datetime.timedelta(hours  = 10)).strftime('%Y/%m/%d %H:%M'), time_now.strftime('%Y/%m/%d %H:%M') )

search_time2 = a.Time( '2014-01-01 00:00', '2014-01-02 00:00' )
Fido.search(search_time2, a.Instrument('hmi'), a.vso.Sample(1*u.hour))

hmi_search = Fido.search(search_time, a.Instrument('hmi'), a.vso.Sample(1*u.hour))


from astropy.time import Time
from sunpy.net.attr import AttrAnd, AttrOr

ta = Time(time_now, format='datetime', scale='tai')
ta1 = Time(time_now - datetime.timedelta(days = 2), format = 'datetime', scale = 'tai')
ta2 = Time(time_now - datetime.timedelta(days = 1), format = 'datetime', scale = 'tai')

segments = ['inclination', 'azimuth', 'disambig', 'field']
series = 'hmi.B_720s'
interval = 10 * u.min
email = 'lydiazly@nju.edu.cn'

response = Fido.search(
a.jsoc.Time(ta1, ta2),
a.jsoc.Series(series),
a.jsoc.Notify(email),
a.Sample(interval),
AttrAnd(list(map(a.jsoc.Segment, segments)))
# i.e. attrs.jsoc.Segment('...') & attrs.jsoc.Segment('...') ...
)
response

Fido.search(a.jsoc.Time('2014-01-01T00:00:00', '2014-01-01T01:00:00'),
           a.jsoc.Series('hmi.sharp_720s'), a.jsoc.Notify('hayesla@tcd.ie'),
           a.jsoc.Segment('image')) 




Fido.search(a.jsoc.Time('2019-01-15T00:00:00', '2019-01-16T01:00:00'),
           a.jsoc.Series('hmi.M_720s_nrt'), a.jsoc.Notify('hayesla@tcd.ie'),
           a.jsoc.Segment('image')) 

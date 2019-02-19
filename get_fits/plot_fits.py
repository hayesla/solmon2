import matplotlib.pyplot as plt 
from sunpy import map 
from astropy.io import fits
import datetime
import os
from astropy import units as u

date_search = datetime.datetime.utcnow()

base_path = '/Users/admin/Documents/solarmonitor_2_0/sol_mon/data/'+date_search.strftime('%Y/%m/%d/')+'fits/'


mapy = map.Map(base_path + 'AIA/*.fits')

def plot_map(mapy):


	fig = plt.figure(figsize = (10, 10))
	ax = fig.add_subplot(111,projection = mapy)

	plt.grid(False)

	mapy.plot(axes = ax, vmin = 0, vmax = mapy.mean() + 6*mapy.std())

	mapy.draw_grid(grid_spacing = 10*u.deg, axes = ax)#, ls = 'dashed')

	ax.set_xlabel('X (arcsec)')
	ax.set_ylabel('Y (arcsec)')
	ax.set_title('AIA Tests', pad = 0.005)

	ax.text(0.76, 0.018, 'SolarMonitor.org', color = 'w', transform = ax.transAxes, fontsize = 'xx-large')



	#plt.subplots_adjust(left = 0.07, right = 1, top = 0.95, bottom = 0.05)

	#ax.set_xlim(-1100, 1100)
	#ax.set_ylim(-1100, 1100)
	plt.tight_layout()
	plt.subplots_adjust(bottom = 0.08, left = 0.08, right = 0.99, top = 0.95)



	plt.savefig('test.png')
	plt.close()



def plot2(mapy):
	plt.grid(False)
	mapy.plot()
	mapy.draw_grid(grid_spacing = 10*u.deg)
	mapy.draw_limb()
	plt.tight_layout()
	plt.savefig('test.png')


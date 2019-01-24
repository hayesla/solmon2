import numpy as np 
import pandas as pd

flarehist_file = 'flarehist.txt'
flarehist_data = np.loadtxt(flarehist_file, dtype = 'str', skiprows = 15)

flarehist_data = pd.read_csv(flarehist_file, skiprows = 14, delim_whitespace = True)

mcpi = flarehist_data['CLS']

nc = flarehist_data['C'] / flarehist_data['N']
nm = flarehist_data['M'] / flarehist_data['N']
nx = flarehist_data['X'] / flarehist_data['N']

mci = ['CRO', 'CRO/CAO']
names = ['12733']

cprob = len(mci)
mprob = len(mci)
cprob = len(mci)

for i in range(len(mci)):
	index = np.where(mcpi == mci[i])[0]
	if len(index) < 1:
		cprob = '...'
		mprob = '...'
		xprob = '...'
	else:
		index = index[0]
		cprob = round(100.*(1-np.exp(-nc[index]))) 
		mprob = round(100.*(1-np.exp(-nm[index])))
		xprob = round(100.*(1-np.exp(-nx[index]))) 

		print(cprob, mprob, xprob)
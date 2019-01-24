pro idl_tests

flarehist_file = 'flarehist.txt'

readcol, flarehist_file, mcip, nc_raw, nm_raw, nx_raw, nn_raw, skipline=15, $
         format='A,D,D,D,D', /silent

nc = nc_raw / nn_raw
nm = nm_raw / nn_raw
nx = nx_raw / nn_raw

print, nx
print, nm
print, nx

stop
end
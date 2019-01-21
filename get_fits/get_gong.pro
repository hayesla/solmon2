pro get_gong, date, mag = mag, int = int

err=''
fname=''
url='gong2.nso.edu'
remote_file=''

if not keyword_Set(date) then date=time2file(systim(/utc),/date) else date=strtrim(date,2)
yyyy=strmid(strtrim(date,2),0,4)
yy=strmid(strtrim(date,2),2,2)
mm=strmid(strtrim(date,2),4,2)
dd=strmid(strtrim(date,2),6,2)

;IGRAM or MAG
if keyword_set(int) then begin
   path='/QR/iqa/'+yyyy+mm+['/bbiqa', $
                            '/leiqa', $
                            '/mliqa', $
                            '/tciqa', $
                            '/tdiqa']
endif else begin
   path='/QR/bqa/'+yyyy+mm+['/bbbqa', $
                            '/lebqa', $
                            '/mlbqa', $
                            '/tcbqa', $
                            '/tdbqa'] 
endelse
path += yy+mm+dd+'/'
print, path


file_reg = (keyword_set(int))?'*iqa*':'*bqa*'
for i=0,n_elements(path)-1 do begin
	print, url+ path[i]+ file_reg
   ftp_find, filei, url=url, path=path[i], file=file_reg+'.fits*'
   filelist = (i eq 0)?filei:[filelist,filei]
endfor
wgood=where(strpos(filelist,'.fits') ne -1,num_good)


if num_good gt 0 then begin
   filelist=filelist[wgood]
   sfits=strpos(filelist,'.fits')
   tlist=long(strmid(filelist,sfits[0]-4,4))
   ;tlist=anytim(file2time(strmid(filelist,sfits[0]-4,4)))
   tsort=sort(tlist)
   filelist=(reverse(filelist[tsort]))[0]
endif else begin & err=-1 & print,'No GONG2 FITS found...' & return & endelse


;if filelist[0] eq '' then begin & print,'No GONG2 FITS found...' & err=1 & return & endif
fname=(reverse(str_sep(filelist,' ')))[0]
ftime=file2time(fname)

path_archive='../data/'+date+'/fits/gong/'
if keyword_Set(int) then $
	is_file = FILE_EXIST( path_archive+'gong_igram_fd_'+ftime+'*.fts.gz' ) $
else $
	is_file = FILE_EXIST( path_archive+'gong_maglc_fd_'+ftime+'*.fts.gz' ) 

if is_file then begin & err=-1 & return & endif

if keyword_set(int) then $
   filefull=url+'/QR/iqa/'+yyyy+mm+'/'+strmid(fname,0,5)+yy+mm+dd+'/'+fname $
else $
   filefull=url+'/QR/bqa/'+yyyy+mm+'/'+strmid(fname,0,5)+yy+mm+dd+'/'+fname



print, filefull
end
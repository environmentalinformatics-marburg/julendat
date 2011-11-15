	subroutine read_ssmi_day(filename,ssmi_data,iexist)

c	This routine reads version-6 RSS SSM/I daily files

c	INPUT
c 	filename  with path in form Fss_yyyymmddvv.gz
c	 where vv  = version  'v6' or 'rt' for real time
c		   ss  = satellite number
c	       yyyy= year
c		   mm  = month
c		   dd  = day of month
c
c	OUTPUT  
c	ssmi_data  (a 1440x720x5x2 array of data)
c	the 5 elements of ssmi_data correspond to:
c	1:time	time of measurement in fractional hour GMT
c	2:wind	10m surface wind in meters/second
c	3:vapor	columnar water vapor in millimeters
c	4:cloud	cloud liquid water in millimeters
c	5:rain	rain rate in millimeters/hour
c
c	Longitude  is 0.25*xdim-0.125
c	Latitude   is 0.25*ydim-90.125


      CHARACTER(1) abuf(1440,720,5)
      real, dimension(1440,720,5,2) ::ssmi_data
	character*60 filename
	real xscale(5)
	logical lexist
      DATA XSCALE/0.1,0.2,0.3,0.01,0.1/

c
c set data arrays to missing
	ssmi_data=254.
	 
	INQUIRE(FILE=filename,EXIST=LEXIST)
	if(.not.lexist) then
		iexist=-1
		return
	endif
	iexist=0
	write(*,*) 'reading ssmi file: ', filename

      OPEN(3,FILE=FILENAME,STATUS='OLD',RECL=5184000,
     1 ACCESS='DIRECT',FORM='UNFORMATTED')
      do ia=1,2
	    READ(3,rec=ia) abuf
		do iv=1,5
			  ssmi_data(:,:,iv,ia)=ICHAR(abuf(:,:,iv))
			  where(ssmi_data(:,:,iv,ia)<=250)
				ssmi_data(:,:,iv,ia)=ssmi_data(:,:,iv,ia)*xscale(iv)
			  endwhere
		enddo
	enddo	
	close(3)

	return
	end



cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
	subroutine read_ssmi_averaged(filename,ssmi_data,iexist)

c	This routine reads version-5 SSM/I time-averaged files including:
c	  3-day		(average of 3 days ending on file date)
c	  weekly	(average of 7 days ending on Saturday of file date)
c	  monthly	(average of all days in month)


c	INPUT
c 	filename
c		format of file names are:
c			3-day		Fss_yyyymmddv6_d3d.gz
c			weekly		Fss_yyyymmddv6.gz
c			monthly		Fss_yyyymmv6.gz
c
c		where	ss	=satellite number
c				yyyy=year
c				mm	=month
c				dd	=day of month
c
c	OUTPUT  
c	ssmi_data   (a 1440x720x4 array of data)
c	the 4 elements of ssmi_data correspond to time averages of:
c	1:wind   10m surface wind in meters/second
c	2:vapor	columnar water vapor in millimeters
c	3:cloud  cloud liquid water in millimeters
c	4:rain	rain rate in millimeters/hour
c
c	Longitude  is 0.25*xdim-0.125
c	Latitude   is 0.25*ydim-90.125

      CHARACTER(1) abuf(1440,720)
      real, dimension(1440,720,4) ::ssmi_data
	character*60 filename
	real xscale(4)
	logical lexist
      DATA XSCALE/0.2,0.3,0.01,0.1/


	ssmi_data=254.
	 
	INQUIRE(FILE=filename,EXIST=LEXIST)
	if(.not.lexist) then
		iexist=-1
		return
	endif
	iexist=0
	write(*,*) 'reading ssmi file: ', filename

      OPEN(3,FILE=FILENAME,STATUS='OLD',RECL=1036800,
     1 ACCESS='DIRECT',FORM='UNFORMATTED')
	do iv=1,4
		READ(3,rec=iv) abuf
		ssmi_data(:,:,iv)=ICHAR(abuf)
		where(ssmi_data(:,:,iv)<=250)
			ssmi_data(:,:,iv)=ssmi_data(:,:,iv)*xscale(iv)
		endwhere
	enddo
	close(3)

	return
	end

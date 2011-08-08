      PROGRAM VERIFY_SSMI_v6

c	this program calls the fortran subroutines that read the 
c	daily and time-averaged data files.  It is currently set
c	to write out the data in the verification files
	
c	remove or comment out sections you do not have files for
     
      CHARACTER*60  filename
      REAL*4, DIMENSION(1440,720,5,2):: ssmi_data
      REAL*4, DIMENSION(1440,720,4)  :: avgd_data
        

CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

	filename='your drive:\your directory\f10_19950120v6'	  !change to match your system
	CALL READ_SSMI_DAY(FILENAME,SSMI_DATA,IEXIST)
	if(iexist.ne.0) stop

	write(*,*) 'gmt time'
	write(*,'(6f11.2)') ssmi_data(170:175,274:278,1,1)
	write(*,*) ' '
	write(*,*) 'wind speed'
	write(*,'(6f11.2)') ssmi_data(170:175,274:278,2,1)
	write(*,*) ' '
	write(*,*) 'water vapor'
	write(*,'(6f11.2)') ssmi_data(170:175,274:278,3,1)
	write(*,*) ' '
	write(*,*) 'cloud'
	write(*,'(6f11.2)') ssmi_data(170:175,274:278,4,1)
	write(*,*) ' '
	write(*,*) 'rain rate'
	write(*,'(6f11.2)') ssmi_data(170:175,274:278,5,1)

c
c
c
	write(*,*) '***********3-day******************'
	filename='your drive:\your directory\f10_19950120v6_d3d'	!change to match your system

	CALL READ_SSMI_averaged(FILENAME,AVGD_DATA,IEXIST)
	if(iexist.ne.0) stop

	write(*,*) 'wind speed'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,1)
	write(*,*) ' '
	write(*,*) 'water vapor'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,2)
	write(*,*) ' '
	write(*,*) 'cloud'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,3)
	write(*,*) ' '
	write(*,*) 'rain rate'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,4)


	write(*,*) '***********weekly******************'
	filename='your drive:\your directory\f10_19950121v6'

	CALL READ_SSMI_averaged(FILENAME,AVGD_DATA,IEXIST)
	if(iexist.ne.0) stop

	write(*,*) 'wind speed'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,1)
	write(*,*) ' '
	write(*,*) 'water vapor'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,2)
	write(*,*) ' '
	write(*,*) 'cloud'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,3)
	write(*,*) ' '
	write(*,*) 'rain rate'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,4)


	write(*,*) '***********month******************'
	filename='your drive:\your directory\f10_199501v6'

	CALL READ_SSMI_averaged(FILENAME,AVGD_DATA,IEXIST)
	if(iexist.ne.0) stop

	write(*,*) 'wind speed'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,1)
	write(*,*) ' '
	write(*,*) 'water vapor'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,2)
	write(*,*) ' '
	write(*,*) 'cloud'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,3)
	write(*,*) ' '
	write(*,*) 'rain rate'
	write(*,'(6f11.2)') avgd_data(170:175,274:278,4)

	stop
	end

	include 'read_ssmi_subroutines_v6.f'
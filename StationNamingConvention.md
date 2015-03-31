

# Naming convention of station files #
The following naming convention is used for the station data filenames in julendat. The components are also used to describe each data value in the appropriate column of each date file.

## F I L E   N A M E ##

PP\_pppppppp\_sss\_YYYYMMDDhhmm\_YYYYMMDDhhmm\_ttt\_LLLL\_GGggg\_PPPP.dat


## C O M P O N E N T S ##

PP:         project ID
pppppppp:   plot ID
sss:        station type
YYYY:       year
MM:         month
DD:         day
hh:         hour
mm:         minute
ttt:        time zone
LLLL:       calibration
GGggg:      aggregation
PPPP:       processing level


## C O D E S ##

### PP - project ID ###
  * ki: DFG-FOR Kilimanjaro
  * be: DFG-SPP Exploratories

### pppppppp - plot ID ###
Plot ID of the station


### ttt - time zone ###
  * mez: middle european standard time (winter!)
  * eat: east afrian standard time

### LLLL - calibration ###
  * rb--: raw binary
    * rb01: raw binary from logger
    * ra--: raw ascii
    * ra01: raw ascii from logger

  * ca--: calibrated
    * ca01: inital calibration (e. g. Volt to Kelvin)

### GGggg - aggregation ###
  * na---: no aggregation
  * ct---: no aggregation but higher input than output resolution
  * fa---: full aggregation (standard set of aggregation statistics)
  * --i--: minutes
  * --h--: hours
  * --d--: days
  * --m--: month
  * --a--: year
  * --n--: Mannheim hours
  * --s--: slots
  * ---xx: time with respect to unit given at position 3
  * m1---: minimum value
  * m2---: mean value
  * m3---: maximum value

### PPPP - processing level ###
  * 0000: initial dataset/no processing (except file renaming)
  * 0005: level 0.05: standardised headers
  * 0050: level 0.5: calibrated data
  * [...see overview in wiki](JulendatStationLevels.md)
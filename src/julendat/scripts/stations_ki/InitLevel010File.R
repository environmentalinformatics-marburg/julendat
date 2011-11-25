init_level_010_file <- function(outpath, start_time, end_time, time_step) {
  
  ## we need 'chron' to handle time zone and daylight saving time independent data
  stopifnot(require("chron"))
  
  ## extract date and time components from start_time
  date_from <- substr(start_time, 1, 8)
  time_from <- substr(start_time, 9, 14)

  ## set 'chron' options to display years as yyyy istead of yy (default)
  options(chron.year.abb = F)
  
  ## create chron object for start of series
  datetime_from <- chron(date_from, time_from, format = c(dates = "ymd", 
                                                          times = "hms"),
                         out.format = c(dates = "y-m-d", times = "h:m:s"))

  ## extract date and time components from end_time
  date_to <- substr(end_time, 1, 8)
  time_to <- substr(end_time, 9, 14)
  
  ## create chron object for end of series
  datetime_to <- chron(date_to, time_to, format = c(dates = "ymd", 
                                                    times = "hms"),
                       out.format = c(dates = "y-m-d", times = "h:m:s"))
  
  ## create chron conform delta t value ("hh:mm:ss")
  ## from time_step (seconds as fractions of day)
  deltat <- times(time_step / 60 / 60 / 24)
  
  ## create regular time series
  tseries <- seq(from = datetime_from, to = datetime_to, 
                 by = deltat)
  
  ## tidy up chron object (i.e. delete enclosing brackets)
  tseries <- gsub("(", "", tseries, fixed=T)
  tseries <- gsub(")", "", tseries, fixed=T)
  
  ## convert time series to data frame for output
  tseries  <- data.frame("dateEAT"=tseries)  

  ## create output
  write.table(tseries, outpath, append=F, col.names=T, row.names=F, sep=",")
  
}

## EXAMPLE
#init_level_010_file("e:/kili_data/testing/level05/test_level010.dat", 
#                   "20110327000000", "20110327035500", 300)

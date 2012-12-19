init_level_010_file <- function(outpath, start_time, end_time, time_step) {
  
  ## set system locale time zone to "UTC" for time handling w/out
  ## daylight saving - save current (old) time zone setting
  Sys.setenv(TZ = "UTC")
  print(Sys.time())
  ## create series 
  date_from <- as.POSIXct(start_time)
  date_to <- as.POSIXct(end_time)
  deltat <- time_step
  
  ## create regular time series
  tseries <- seq(from = date_from, to = date_to, 
                 by = deltat)

  ## convert to character and write
  tseries <- format(tseries, usetz = F)
  write.table(tseries, outpath, append=F, col.names="date", row.names=F, sep=",")
  
  ## revert system local time zone setting to original
  Sys.setenv(TZ = "CET")
  print(Sys.time())
}

## EXAMPLE
# init_level_010_file("/home/tappelhans/test.dat", "2011-03-27 00:00:00", 
# "2011-03-27 03:00:00", 300)

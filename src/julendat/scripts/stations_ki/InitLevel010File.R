init_level_010_file <- function(outpath, start_time, end_time, time_step) {
  
  ## set system locale time zone to "UTC" for time handling w/out
  ## daylight saving - save current (old) time zone setting
  Old.TZ <- Sys.getenv("TZ")
  Sys.setenv(TZ = "UTC")
  
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
  Sys.setenv(TZ = Old.TZ)
  
}

## EXAMPLE
init_level_010_file("e:/kili_data/testing/level05/test_level001_POSIX.dat", 
                    "2011-10-01 00:00:00", "2011-10-31 23:55:00", 300)
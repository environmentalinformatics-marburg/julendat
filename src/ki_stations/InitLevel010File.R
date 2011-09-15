init_level_010_file <- function(outpath, start_time, end_time, time_step) {
  
  start_time <- format(start_time, scientific = F)
  end_time <- format(end_time, scientific = F)
  
  from <- strptime(start_time, format = "%Y%m%d%H%M")
  to <- strptime(end_time, format = "%Y%m%d%H%M")
  by <- time_step
  
  tseries <- seq(from, to, by)
  tseries <- format(tseries, usetz=F)
  #tseries <- as.POSIXct(tseries)
  tseries  <- data.frame("dateEAT"=tseries)
   
  write.table(tseries, outpath, append=F, col.names=T, row.names=F, sep=",")
  
}
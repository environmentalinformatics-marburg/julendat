## define function
compute_level_005_file <- function(asciipath, outpath, plotID, loggertype, 
                       cf, reorder, skip, tz, quality, adjust_time, order_out) {

  ## define order for reading in data and writing out data
  order_in <- c(1:length(order_out))

  ## read in logger data table (temp), create empty table (tab) of same size 
  ## (filled with NAs) and replace columns accoring to defined order
  temp <- read.table(asciipath, col.names=order_in, skip=skip, fill=T)
  tab <- matrix(ncol = length(order_out), nrow = length(temp[,1]))

  for (i in 1:length(reorder)) 
    for (j in 1:length(reorder))
      tab[,reorder[[i]]] <- temp[,i]    

  tab <- as.data.frame(tab)
  names(tab) <- order_out
               
  ## create date and time variables -- convert to local time (EAT)
  year <- substr(temp[,1],7,8)
  year <- paste("20",year,sep="")
  month <- substr(temp[,1],4,5)
  day <- substr(temp[,1],1,2)
  hour <- substr(temp[,2],1,2)
  minute <- substr(temp[,2],4,5)
  second <- substr(temp[,2],7,8)

  dateCET <- as.POSIXct(ISOdate(year,month,day,hour,minute,second))

  dateEAT <- dateCET + adjust_time

  dateEAT <- as.POSIXct(format(dateEAT, usetz=F))
  dateEAT <- as.character(dateEAT)

  chdateEAT <- strftime(dateEAT, "%Y%m%d%H%M%S")
  chdateEAT <- as.character(chdateEAT)

  year <- substr(chdateEAT,1,4)
  year <- as.character(year)

  month <- substr(chdateEAT,5,6)
  month<- as.character(month)

  day <- substr(chdateEAT,7,8)
  day <- as.character(day)

  hour <- substr(chdateEAT,9,10)
  hour <- as.character(hour)

  minute <- substr(chdateEAT,11,12)
  minute <- as.character(minute)

  second <- substr(chdateEAT,13,14)
  second <- as.character(second)
               
  tab$dateEAT <- dateEAT
  tab$year <- year
  tab$month <- month
  tab$day <- day
  tab$hour <- hour
  tab$minute <- minute
  tab$chdateEAT <- chdateEAT

  ## create vectors and fill table (tab) accordingly
  quality <- rep(quality, length(year))
  quality <- sprintf("%04d", quality)
  tab$quality <- quality

  plotid <- rep(plotID, length(year))
  plotid <- as.character(plotid)
  tab$plotID <- plotid

  logger <- rep(loggertype, length(year))
  logger <- as.character(logger)
  tab$logger <- logger

  c_precip_pu1 <- rep(cf[1], length(year))
  c_precip_pu1 <- as.numeric(c_precip_pu1)
  tab$precip_pu1 <- tab$p_precip_pu1 * c_precip_pu1
  tab$c_precip_pu1 <- c_precip_pu1

  c_precip_pu2 <- rep(cf[2], length(year))
  c_precip_pu2 <- as.numeric(c_precip_pu2)
  tab$precip_pu2 <- tab$p_precip_pu2 * c_precip_pu2
  tab$c_precip_pu2 <- c_precip_pu2

  c_fog_pu2 <- rep(cf[3], length(year))
  c_fog_pu2 <- as.numeric(c_fog_pu2)
  tab$fog_pu2 <- tab$p_fog_pu2 * c_fog_pu2
  tab$c_fog_pu2 <- c_fog_pu2

  c_kd_wxt <- rep(cf[4] / 1000, length(year))
  c_kd_wxt <- as.numeric(c_kd_wxt)
  tab$c_kd_wxt <- c_kd_wxt

  c_ku_wxt <- rep(cf[5] / 1000, length(year))
  c_ku_wxt <- as.numeric(c_ku_wxt)
  tab$c_ku_wxt <- c_ku_wxt

  c_ld_wxt <- rep(cf[6] / 1000, length(year))
  c_ld_wxt <- as.numeric(c_ld_wxt)
  tab$c_ld_wxt <- c_ld_wxt

  c_lu_wxt <- rep(cf[7] / 1000, length(year))
  c_lu_wxt <- as.numeric(c_lu_wxt)
  tab$c_lu_wxt <- c_lu_wxt

  c_kd_rad <- rep(cf[8], length(year))
  c_kd_rad <- as.numeric(c_kd_rad)
  tab$c_kd_rad <- c_kd_rad

  c_par_rad <- rep(cf[9], length(year))
  c_par_rad <- as.numeric(c_par_rad)
  tab$c_par_rad <- c_par_rad

  ## define Stefan-Boltzman calculations (needed for ld and lu - see below)
  kStefanBoltzman <- 5.672e-08 
  ZeroKelvin <- 273.15              
  SBlaw <- kStefanBoltzman * (tab$t_cnr_wxt + ZeroKelvin)^4
               
  tab$kd_w_wxt <- tab$u_kd_wxt / c_kd_wxt
  tab$kd_w_wxt <- as.numeric(tab$kd_w_wxt)
  tab$ku_w_wxt <- tab$u_ku_wxt / c_ku_wxt + SBlaw
  tab$ku_w_wxt <- as.numeric(tab$ku_w_wxt)
  tab$kd_w_wxt <- tab$u_kd_wxt / c_kd_wxt
  tab$kd_w_wxt <- as.numeric(tab$kd_w_wxt)
  tab$lu_w_wxt <- tab$u_lu_wxt / c_lu_wxt + SBlaw
  tab$lu_w_wxt <- as.numeric(tab$lu_w_wxt)

  for (i in 1:length(tab)) { 
    if (isTRUE(is.numeric(tab[,i]))) tab[,i] <- round(tab[,i], 4) }

  write.table(tab, outpath, append=F, col.names=T, row.names=F, sep=",", na="NaN")

}

#library(compiler)
#compute_level_005_file.c <- cmpfun(compute_level_005_file)

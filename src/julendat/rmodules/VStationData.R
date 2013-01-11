VStationData <- function(
  plotval,
  datetime,
  cond= rep(" ", length(plotval)),
  fun = mean, 
  arrange = c("long", "wide"),
  colour = colorRampPalette(c("darkblue", "darkseagreen", 
                                              "gold", "darkred"),
                                            interpolate = "linear"),
                  ...) {
################################################################################
################################################################################
  
  ## load packages needed (produce error message if not installed)
  stopifnot(require(latticeExtra))
  stopifnot(require(grid))
  
  ## set system locale time zone to "UTC" for time handling w/out
  ## daylight saving - save current (old) time zone setting
  Old.TZ <- Sys.timezone()
  Sys.setenv(TZ = "UTC")
  
  ## combine plot values, datetime information and group condition in data frame
  df <- data.frame(plotval, datetime, cond)
  
  ## identify unique group conditions and remove those with no information
  condims <- as.character(unique(cond))
  condims <- subset(condims, condims != "" | condims != NA)
  
  ## identify unique years
  uniyears <- unique(substr(df$datetime, 1, 4))
  df$years <- substr(df$datetime, 1, 4)

  ## divide data frame with respect to years and combine results into a data list 
  ldat <- split(df, df$years, drop = T)

  ## divide data list with respect to group condition 
  ldat <- sapply(seq(ldat), function(i) {
    split(ldat[[i]], ldat[[i]]$cond, drop = T)
  })
  
  ls <- lapply(seq(ldat), function(i) {

    datetime <- as.character(ldat[[i]]$datetime)
    plotval <- ldat[[i]]$plotval
    origin <- paste(substr(datetime[1], 1, 4), "01-01", sep = "-")
    unldate <- lapply(as.POSIXlt(datetime), "unlist")
    hour <- unldate$hour   

    ## calculate different datetime objects
    juldays <- as.Date(datetime, origin = as.Date(origin))
    #jul <- format(juldays, "%j")  
    
    ## create regular time series for year of origin
    date_from <- as.POSIXct(origin)
    year <- substr(origin, 1, 4)
    date_to <- as.POSIXct(paste(year, "12-31", sep = "-"))
    deltat <- 60 * 60
    tseries <- seq(from = date_from, to = date_to, 
                   by = deltat)
    strip_z <- matrix(NA, nrow = 24, ncol = length(unique(as.Date(tseries))))
  
    date_x <- as.Date(datetime)
    hour_x <- ifelse(hour < 10, paste("0", hour, sep = ""), as.character(hour))
    datetime_x <- paste(date_x, hour_x, sep = " ")
    datetime_x <- paste(datetime_x, "00", sep = ":")
    
    z_x <- aggregate(plotval ~ datetime_x, FUN = fun)

    index_hour <- substr(z_x$datetime_x, 12, 13)
    index_date <- as.Date(z_x$datetime_x)
  
    mat_x <- cbind((as.integer(index_hour) + 1), 
                   julian(index_date, origin = as.Date(origin)))
    
    strip_z[mat_x] <- z_x$plotval
    
    xblockx <- sort(julian(tseries, origin = as.Date(origin)))
    xbar <- format(tseries, "%b")
    xlabs <- format(unique(xbar, "%b"))
    xat <- seq.Date(as.Date(date_from), as.Date(date_to), by = "month")
    xat <- as.integer(julian(xat, origin = as.Date(origin))) + 15
    
    levelplot(t(strip_z), ylim = c(-0.5, 24.5), col.regions = colour,
              strip = F, ylab = "Hour of day", xlab = NULL, asp = "iso",
              strip.left = strip.custom(
                bg = "black", factor.levels = toupper(condims),
                par.strip.text = list(col = "white", font = 2, cex = 0.8)),
              as.table = T, cuts = 200, between = list(x = 0, y = 0),
              scales = list(x = list(at = xat, labels = xlabs),
                            y = list(at = c(6, 12, 18))),
              colorkey = list(space = "top", width = 1, height = 0.7),
              panel = function(x, ...) {
                panel.levelplot(x, ...)
                panel.xblocks(xblockx, y = xbar, height = unit(1, "native"),
                              col = c("black", "white"), 
                              border = "black", last.step = 1.1, lwd = 0.3)
                              #hjust = 0, vjust = -0, outside = T)
                panel.abline(h = c(6, 18), lty = 2, lwd = 0.3, col = "grey70")
                },  
              ...)
    })
  
  out <- ls[[1]]
  if(length(ldat)>1){
  for (i in 2:(length(ldat))) {
    out <- c(out, ls[[i]], x.same = T, y.same = T, 
             layout = switch(arrange,
                             "long" = c(1,length(condims)),
                             "wide" = NULL))
  }
  }
 
  
  #out <- ls[[1]]
  #for (i in 2:(length(ldat)))
  #  out <- c(out, ls[[i]], x.same = T, y.same = T, 
  #           layout = switch(arrange,
  #                           "long" = c(1,length(condims)),
  #                           "wide" = NULL))
  
  out <- update(out, scales = list(y = list(rot = list(0, 0)), tck = c(0, 0)))
  print(out)
  
  ## revert system local time zone setting to original
  Sys.setenv(TZ = Old.TZ)
  
  
}

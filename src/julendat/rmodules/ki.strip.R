ki.strip <- function(inputfilepath,
                       prm = "Ta_200",                       
                       fun = mean,
                       arrange = "long",
                       year,
                       range,
                       pattern = "*fah01_0200.dat",
                       colour = colorRampPalette(c("darkblue", "aquamarine", 
                                                   "gold", "red2"),
                                                 interpolate = "linear"),
                       project_id,
                       ...) {
  
################################################################################
##  
##  This program plots meteorological parameters as
##  a function of time of day (y-axis) and day of year (x-axis). Values are
##  colour shaded from minimum to maximum. It is possible to supply a
##  plotiditioning variable (as this function uses trellis plotting).
##  NOTE: observations must be hourly or higher frequency!
##  
##  parameters are as follows:
##  
##  x (numeric):          Object to be plotted (e.g. temperature).
##  date (character):     Date(time) of the observations.
##                        Format must be 'YYYY-MM-DD hh:mm(:ss)'
##  fun:                  The function for used aggregation to hourly 
##                        observations (if original is of higher fequency).
##  plotid (factor):        plotiditioning variable (optional).
##  arrange (character):  One of "wide" or "long". For plot layout.
##  colour (character):   Defaults to classical temperature colour palette.
##  ...                   Further arguments to be passed to levelplot
##                        (see ?lattice::leveplot for options).
##
################################################################################
##
##  Copyright (C) 2012 Tim Appelhans, Thomas Nauss
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##  Please send any comments, suggestions, criticism, or (for our sake) bug
##  reports to tim.appelhans@gmail.com
##
################################################################################

  cat("\n",
      "Module   :  ki.strip", "\n",
      "Author   :  Tim Appelhans <tim.appelhans@gmail.com>, Thomas Nauss", "\n",
      "Version  :  2012-03-15", "\n",
      "License  :  GNU GPLv3, see http://www.gnu.org/licenses/", "\n",
      "\n")
  
########## FUNCTION BODY #######################################################
  
  ## load packages needed (produce error message if not installed)
  stopifnot(require(latticeExtra))
  stopifnot(require(grid))
  stopifnot(require(reshape))
  
  source("VColList.R")
  source("as.ki.data.R")
  
  ## set system locale time zone to "UTC" for time handling w/out
  ## daylight saving - save current (old) time zone setting
  Old.TZ <- Sys.timezone()
  Sys.setenv(TZ = "UTC")
  
  flist <- inputfilepath
  #list.files(inputpath, recursive = T, pattern = glob2rx(pattern))
  test <- c(strsplit(inputfilepath, "/"))
  print (str(test))
  ki.data.list <- lapply(seq(flist), 
                         function(i) as.ki.data(flist[i]))

#   sub <- sapply(seq(ki.data.list), 
#                          function(i) ki.data.list[[i]]@StationId$Unique
#                          )
# 
#   sub <- which(sub == logger)
#   ki.data.list <- ki.data.list[sub]

  df <- lapply(seq(ki.data.list),
               function(i) data.frame(x = ki.data.list[[i]]@Parameter[[prm]], 
                                      datetime = ki.data.list[[i]]@Datetime,
                                      plotid = ki.data.list[[i]]@PlotId$Shortname,
                                      year = ki.data.list[[i]]@Date$Year)
               )

  df <- as.data.frame(do.call("rbind", df))
  df2 <- split(df, df$year, drop = T)
  df2 <- as.data.frame(df2[[year]])

  minx <- if (missing(range)) min(as.numeric(df2$x), na.rm = TRUE) else range[1]
  maxx <- if (missing(range)) max(as.numeric(df2$x), na.rm = TRUE) else range[2]

  condims <- as.character(unique(na.exclude(df2$plotid)))
  
  #Change for the station name for bexis
  if ( project_id == "be" ) {
  	condims <- as.character(unique(na.exclude(substr(df2$plotid, 4, 8))))
  }
  print (project_id)
  xlist <- split(df2, df2$plotid, drop = T)

  ls <- lapply(seq(xlist), function(i) {

    datetime <- as.character(xlist[[i]]$datetime)
    x <- xlist[[i]]$x

    origin <- paste(substr(datetime[1], 1, 4), "01-01", sep = "-")
    unldatetime <- lapply(as.POSIXlt(datetime), "unlist")
    hour <- unldatetime$hour   

    ## calculate different times objects
    juldays <- as.Date(datetime, origin = as.Date(origin))
    jul <- format(juldays, "%j")  
    
    ## create regular time series for year of origin
    datetime_from <- as.POSIXct(origin)
    year <- substr(origin, 1, 4)
    datetime_to <- as.POSIXct(paste(year, "12-31", sep = "-"))
    deltat <- 60 * 60
    tseries <- seq(from = datetime_from, to = datetime_to, 
                   by = deltat)

    strip_z <- matrix(NA, nrow = 25, ncol = length(unique(as.Date(tseries))))
  
    datetime_x <- as.Date(datetime)
    hour_x <- ifelse(hour < 10, paste("0", hour, sep = ""), as.character(hour))
    datetime_x <- paste(datetime_x, hour_x, sep = " ")
    datetime_x <- paste(datetime_x, "00", sep = ":")

    # tnauss: if x consits only of NaNs, replace NaNs with -9999.0
    if(sum(is.na(x)) == length(x)){
      x <- rep(-9999.0, length(x))
    }
    z_x <- aggregate(x ~ datetime_x, FUN = fun)

    index_hour <- substr(z_x$datetime_x, 12, 13)
    index_date <- as.Date(z_x$datetime_x)
  
    mat_x <- cbind((as.integer(index_hour) + 1), 
                   julian(index_date + 1, origin = as.Date(origin)))

    strip_z[mat_x] <- z_x$x
    
    xblockx <- sort(julian(tseries, origin = as.Date(origin)))
    xbar <- format(tseries, "%b")
    xlabs <- format(unique(xbar, "%b"))
    xat <- seq.Date(as.Date(datetime_from), as.Date(datetime_to), by = "month")
    xat <- as.integer(julian(xat, origin = as.Date(origin))) + 15
    
    # sforteva: the processlevel into header
    temp <- regexpr('\\d.*\\d', pattern, perl=TRUE)
    level <-regmatches(pattern,temp)
    
    
    levelplot(t(strip_z), ylim = c(24.5, -0.5), col.regions = colour,
              strip = F, ylab = "Hour of day", xlab = NULL, asp = "iso",
              at = seq(minx, maxx, 0.1),
              strip.left = strip.custom(
                bg = "black", factor.levels = toupper(condims),
                par.strip.text = list(col = "white", font = 2, cex = 0.8)),
              as.table = T, cuts = 200, between = list(x = 0, y = 0),
              scales = list(x = list(at = xat, labels = xlabs),
                            y = list(at = c(18, 12, 6))),
              colorkey = list(space = "top", width = 1, height = 0.7,
                              at = seq(minx, maxx, 0.1)), 
              main = paste("overview", ifelse(project_id=="be", paste(substr(condims[1], 1,3), "level -", level), ""), prm, year, sep = " "),
              panel = function(x, ...) {
                grid.rect(gp=gpar(col=NA, fill="grey50"))
                panel.levelplot(x, ...)
                panel.xblocks(xblockx, y = xbar, height = unit(1, "native"),
                              col = c("black", "white"), block.y = -0.5,
                              border = "black", last.step = 1.25, lwd = 0.3)
                              
                panel.abline(h = c(6, 18), lty = 2, lwd = 0.5, col = "grey90")
                },  
              ...)
    })

  out <- ls[[1]]
  out2 <- out
  #print(out)
  if (length(ls) > 1) {
    for (i in 2:(length(xlist)))
        out <- c(out, ls[[i]], x.same = T, y.same = T, 
                 layout = switch(arrange,
                                 "long" = c(1,length(condims)),
                                 "wide" = NULL))
  }                            
  
  out <- update(out, scales = list(y = list(rot = list(0, 0)), tck = c(0, 0)),
                ylim = c(24.5, -0.5))

  ifelse(length(ls) > 1, print(out), print(out2))
  
  ## revert system local time zone setting to original
  Sys.setenv(TZ = Old.TZ)
  
  
}

#ki.strip("/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/fa01_fah01_0200/", year = "2012")

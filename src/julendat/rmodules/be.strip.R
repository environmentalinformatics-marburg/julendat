be.strip <- function(inputpath,
                     logger = "CEMU",
                     prm = "Ta_200",                       
                     fun = mean,
                     arrange = "long",
                     year,
                     range,
                     pattern,
                     colour = colorRampPalette(c("darkblue", "aquamarine", 
                                                 "gold", "darkred"),
                                               interpolate = "linear"),
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
##	arrange (character):  One of "wide" or "long". For plot layout.
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
      "Module   :  be.strip", "\n",
      "Author   :  Tim Appelhans <tim.appelhans@gmail.com>, Thomas Nauss", "\n",
      "Version  :  2012-03-16", "\n",
      "License  :  GNU GPLv3, see http://www.gnu.org/licenses/", "\n",
      "\n")
  
########## FUNCTION BODY #######################################################
  
  ## load packages needed (produce error message if not installed)
  stopifnot(require(latticeExtra))
  stopifnot(require(grid))
  
  source("c:/tappelhans/uni/software/development/metvurst/strip/colList.R")
  source("c:/tappelhans/uni/software/development/r_be/src/be.data/as.be.data.R")
  
  ## set system locale time zone to "UTC" for time handling w/out
  ## daylight saving - save current (old) time zone setting
  Old.TZ <- Sys.timezone()
  Sys.setenv(TZ = "UTC")
  
  flist <- list.files(inputpath, recursive = T, pattern = glob2rx(pattern))
  be.data.list <- lapply(seq(flist), 
                         function(i) as.be.data(paste(inputpath,
                                                      flist[i],
                                                      sep="/")))

  sub <- sapply(seq(be.data.list), 
                         function(i) be.data.list[[i]]@StationId$Unique
                         )
  
  sub <- which(sub == logger)
  be.data.list <- be.data.list[sub]

  df <- lapply(seq(be.data.list),
               function(i) data.frame(x = be.data.list[[i]]@Parameter[[prm]], 
                                      datetime = be.data.list[[i]]@Datetime,
                                      plotid = be.data.list[[i]]@PlotId$Shortname,
                                      year = be.data.list[[i]]@Date$Year)
               )
  
  df <- do.call("rbind", df)
  
  df2 <- split(df, df$year, drop = T)
  df2 <- df2[[year]]
  
  minx <- if (missing(range)) min(na.exclude(df2$x)) else range[1]
  maxx <- if (missing(range)) max(na.exclude(df2$x)) else range[2]
 
  condims <- as.character(unique(na.exclude(df2$plotid)))
  #print(condims[2])
  xlist <- split(df2, df2$plotid, drop = T)
#   xlist <- sapply(seq(xlist), function(i) {
#     split(xlist[[i]], xlist[[i]]$plotid, drop = T)
#   }
#                   )
  
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
    
    levelplot(t(strip_z), ylim = c(-0.5, 24.5), col.regions = colour,
              strip = F, ylab = "Hour of day", xlab = NULL, asp = "iso",
              at = seq(minx, maxx, 0.1),
              strip.left = strip.custom(
                bg = "black", factor.levels = toupper(condims),
                par.strip.text = list(col = "white", font = 2, cex = 0.8)),
              as.table = T, cuts = 200, between = list(x = 0, y = 0),
              scales = list(x = list(at = xat, labels = xlabs),
                            y = list(at = c(6, 12, 18))),
              colorkey = list(space = "top", width = 1, height = 0.7,
                              at = seq(minx, maxx, 0.1)), 
              main = paste("overview", prm, logger, year, sep = " "),
              panel = function(x, ...) {
                grid.rect(gp=gpar(col=NA, fill="grey50"))
                panel.levelplot(x, ...)
                panel.xblocks(xblockx, y = xbar, height = unit(1, "native"),
                              col = c("black", "white"), block.y = 24.5,
                              border = "black", last.step = 1.1, lwd = 0.3)
                              #hjust = 0, vjust = -0, outside = T)
                panel.abline(h = c(6, 18), lty = 2, lwd = 0.5, col = "grey90")
                },  
              ...)
    })
  
  out <- ls[[1]]
  if (length(ls) > 1) {
    for (i in 2:(length(xlist)))
      out <- c(out, ls[[i]], x.same = T, y.same = T, 
               layout = switch(arrange,
                               "long" = c(1,length(condims)),
                               "wide" = NULL))
  } else out
  
  out <- update(out, scales = list(y = list(rot = list(0, 0)), tck = c(0, 0)))
  print(out)
  
  ## revert system local time zone setting to original
  Sys.setenv(TZ = Old.TZ)
  
  
}


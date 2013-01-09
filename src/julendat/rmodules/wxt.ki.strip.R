wxt.ki.strip <- function(inputpath,
                         fun = mean,
                         plotid = "nkw1",
                         year,
                         ptrn = "*fah01_200.dat",
                         ...) {

  stopifnot(require(latticeExtra))
  stopifnot(require(grid))
  
  source("/home/ede/software/development/julendat/src/julendat/rmodules/VColList.R")
  source("/home/ede/software/development/julendat/src/julendat/rmodules/as.ki.data.R")
  
  Old.TZ <- Sys.timezone()
  Sys.setenv(TZ = "UTC")
  
  flist <- list.files(inputpath, recursive = T, pattern = glob2rx(ptrn))
  flist <- grep(plotid, flist, value = T)
  flist <- grep(glob2rx("*wxt*"), flist, value = T)

  wxt.data.list <- lapply(seq(flist), 
                          function(i) as.ki.data(paste(inputpath,
                                                         flist[i],
                                                         sep="/")))

  prms <- names(wxt.data.list[[1]]@Parameter)
  prms <- prms[seq(1, length(prms), 9)]

  prmlist <- lapply(seq(wxt.data.list),
                    function(i) lapply(seq(prms),
                                       function(j)
                                         data.frame(
                                           D = wxt.data.list[[i]]@Datetime,
                                           P = wxt.data.list[[i]]@PlotId$Shortname,
                                           Y = wxt.data.list[[i]]@Date$Year,
                                           X = wxt.data.list[[i]]@Parameter[[prms[j]]])
                                       )
                    )
  
  for (i in seq(prmlist))
       for (j in seq(prms))
            names(prmlist[[i]][[j]]) <- c("Datetime", "PlotId", "Year", prms[j])
  
  dflist <- do.call("rbind", prmlist)
  
  sqnc <- rep(1:length(prms), each = length(wxt.data.list))
  dflist <- split(dflist, as.factor(sqnc))
  
  dflist <- lapply(seq(dflist), function(i) do.call("rbind", dflist[[i]]))
  dflist <- lapply(seq(dflist), function(i) split(dflist[[i]], dflist[[i]]$Year, 
                                                  drop = T))
  
  dflist <- lapply(seq(dflist), function(i) as.data.frame(dflist[[i]][[year]]))
  
  minx <- lapply(seq(dflist), function(i) min(na.exclude(dflist[[i]][4])))
  maxx <- lapply(seq(dflist), function(i) max(na.exclude(dflist[[i]][4])))
  
  aggls <- lapply(seq(dflist), function(i) {
    
    datetime <- as.character(dflist[[i]]$Datetime)
    x <- dflist[[i]][[4]]
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
    
    levelplot(t(strip_z), ylim = c(24.5, -0.5), col.regions = VColList[[i]],
              strip = F, ylab = "Hour of day", xlab = NULL, asp = "iso",
              at = seq(minx[[i]], maxx[[i]], 0.1),
              strip.left = strip.custom(
                bg = "black", factor.levels = toupper(prms),
                par.strip.text = list(col = "white", font = 2, cex = 0.8)),
              as.table = T, cuts = 200, between = list(x = 0, y = 0),
              scales = list(x = list(at = xat, labels = xlabs),
                            y = list(at = c(18, 12, 6))),
              colorkey = F, ylab.right = ".\n\n\n\n",
              main = paste("Overview", "WXT", toupper(plotid), year, sep = " "),
              panel = function(x, ...) {
                grid.rect(gp=gpar(col=NA, fill="grey50"))
                panel.levelplot(x, ...)
                panel.xblocks(xblockx, y = xbar, height = unit(1, "native"),
                              col = c("black", "white"), block.y = -0.5,
                              border = "black", last.step = 1.25, lwd = 0.3)
                
                panel.abline(h = c(6, 18), lty = 2, lwd = 0.5, col = "grey90")
              },  
              ...)
  }
                  )  
  
  out <- aggls[[1]]
  for (i in 2:length(aggls)) {
    out <- c(out, aggls[[i]], x.same = T, y.same = T, merge.legends = F)
  }

  out <- update(out, layout = c(1, length(aggls)),
                scales = list(y = list(draw = F, rot = list(0, 0)), 
                              tck = c(0, 0)),
                ylim = c(24.5, -0.5))
  print(out)
  
  addColorKey <-  function(lngth) {
    for (i in seq(lngth)) {
      trellis.focus("panel", 1, i, clip.off = T, highlight = F)
      draw.colorkey(list(space = "right", width = 2, height = 0.75,
                         at = seq(minx[[i]], maxx[[i]], 0.1), 
                         col = VColList[[prms[i]]], rot = 270),
                    draw = T, 
                    vp = viewport(x = 1.03, y = 0.5,
                                  width = unit(0.0001, "npc"), 
                                  height = unit(1, "npc"),
                                  just = c("left", "centre"),
                                  clip = "off"))
      trellis.unfocus()
    }
  }
  
  addColorKey(length(aggls))
  
  Sys.setenv(TZ = Old.TZ)
}
# png("c:/tappelhans/uni/marburg/kili/stations/ki/plots/test.png",
#     height = 768*3, width = 1024*3, res = 300)
# wxt.ki.strip(inputpath = "/home/ede/software/testing/julendat/processing/plots/ki/0000cof3/fa01_fah01_0200/",
#              plotid = "cof3",
#              year = "2011",
#              ptrn = "*fah01_0200.dat")
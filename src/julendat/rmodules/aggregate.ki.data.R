aggregate.ki.data <- function(input,
                              level = "1h",
                              plevel = 0000,
                              start.column = 9,
                              ...) {
  
  Old.TZ <- Sys.timezone()
  Sys.setenv(TZ = "UTC")

  options(warn = -1)
  
  source("as.ki.data.R")
  source("wdws2uv.R")
  source("uv2wd.R")
  stopifnot(require(reshape))

  ki.data <- as.ki.data(input, start.column = start.column)

  switch(level,
         "qh" = agglevel <- ki.data@AggregationLevels$AggQh,
         "1h" = agglevel <- ki.data@AggregationLevels$Agg1h,
         "3h" = agglevel <- ki.data@AggregationLevels$Agg3h,
         "6h" = agglevel <- ki.data@AggregationLevels$Agg6h,
         "day" = agglevel <- ki.data@AggregationLevels$AggDay,
         "month" = agglevel <- ki.data@AggregationLevels$AggMonth,
         "diurnal" = agglevel <- ki.data@Time$Hour,
         "seasonal" = agglevel <- ki.data@Season
         )
  
  switch(level,
         "qh" = aggunit <- "i",
         "1h" = aggunit <- "h",
         "3h" = aggunit <- "h",
         "6h" = aggunit <- "h",
         "day" = aggunit <- "d",
         "month" = aggunit <-"m",
         "diurnal" = aggunit <- "D",
         "seasonal" = aggunit <- "S"
         )
  
  switch(level,
         "qh" = aggint <- "15",
         "1h" = aggint <- "01",
         "3h" = aggint <- "03",
         "6h" = aggint <- "06",
         "day" = aggint <- "01",
         "month" = aggint <-"01",
         "diurnal" = aggint <- "01",
         "seasonal" = aggint <- "01"
  )
  

  qsplit <- lapply(seq(ki.data@Qualityflag), function(i) {
    substring(ki.data@Qualityflag[i], 
              first = c(seq(2, nchar(ki.data@Qualityflag[i]), 3)),
              last = c(seq(4, nchar(ki.data@Qualityflag[i]), 3)))
  })

  qsplit <- do.call("rbind", qsplit)
  qsplitind <- lapply(seq(NCOL(qsplit)), function(i) {
    which(qsplit[, i] == "002" | qsplit[, i] == "012" | qsplit[, i] == "022")
  })
  

  try(
    for (i in seq(qsplitind)) ki.data@Parameter[[i]][qsplitind[[i]]] <- NA
  )
  
  agglevel <- as.character(agglevel)
  
  timezone <- rep(ki.data@Timezone, length.out = length(unique(agglevel)))
  aggregationtime <- paste("fa", aggunit, aggint, sep = "")
  aggregationtime <- rep(aggregationtime, length.out = length(unique(agglevel)))
  plotid <- rep(ki.data@PlotId$Unique, length.out = length(unique(agglevel)))
  epplotid <- rep(ki.data@EpPlotId, length.out = length(unique(agglevel)))
  stationid <- rep(ki.data@StationId$Longname, 
                   length.out = length(unique(agglevel)))
  processlevel <- rep(sprintf("%04.f", plevel), 
                      length.out = length(unique(agglevel)))
  qualityflag <- rep(paste("q", sprintf(paste("%0", length(ki.data@Parameter) * 3, 
                                              ".f", sep = ""), 0), sep = ""), 
                     length.out = length(unique(agglevel)))
  
  prm.df <- as.data.frame(ki.data@Parameter, stringsAsFactors = F)
  
  if (any(names(ki.data@Parameter) == "WD"))
    {
    uv <- wdws2uv(prm.df[["WD"]], prm.df[["WV"]])
    prm.df$u <- uv$u
    prm.df$v <- uv$v
  }
 
  names.prm.df <- names(prm.df)
  
  aggdescr <- c("", "_min", "_max", "_median", "_stdv", 
                "_25", "_75", "_sum", "_n", "_nan")
  names.prm <- rep(names.prm.df, each = length(aggdescr))
  aggnames <- paste(names.prm, aggdescr, sep = "")

  prm.ls <- split(prm.df, agglevel)
  
  agglist <- lapply(seq(prm.ls), function(i) {
    
    lapply(seq(prm.df), function(j) {
      
      tmp <- prm.ls[[i]][[j]]
      
      tmp <- if (all(is.nan(tmp))) rep(NA, length(tmp)) else tmp[! is.na(tmp)]
      
      list(mean(prm.ls[[i]][[j]], na.rm = T),
           min(prm.ls[[i]][[j]], na.rm = T),
           max(prm.ls[[i]][[j]], na.rm = T),
           median(prm.ls[[i]][[j]], na.rm = T),
           sd(prm.ls[[i]][[j]], na.rm = T),
           quantile(prm.ls[[i]][[j]], na.rm = T, probs = 0.25, names = F),
           quantile(prm.ls[[i]][[j]], na.rm = T, probs = 0.75, names = F),
           sum(tmp, na.rm = FALSE),
           sum(complete.cases(prm.ls[[i]][[j]])),
           length(prm.ls[[i]][[j]]) - sum(complete.cases(prm.ls[[i]][[j]]))
           )
      
    }
    )

  }
  )
  
  agglist <- lapply(seq(agglist), function(i) {
    unlist(agglist[[i]])
  }
  )
  
  names(agglist) <- unique(agglevel)
  
  aggdf <- as.data.frame(do.call("rbind", agglist))
  names(aggdf) <- aggnames

  if (any(names(ki.data@Parameter) == "WD") == TRUE)
  {
    posWD <- grep(glob2rx("WD*"), aggnames)
    posu <- grep(glob2rx("u*"), aggnames)
    posv <- grep(glob2rx("v*"), aggnames)
    
    wd <- lapply(seq(posWD), function(i) {
      uv2wd(aggdf[, posu[i]], aggdf[, posv[i]])
      }
                 )
    
    for (i in 1:(length(wd) - 2)) {
      aggdf[, posWD[i]] <- uv2wd(aggdf[, posu[i]], aggdf[, posv[i]])
      }
  
    exuv <- length(ki.data@Parameter) * length(aggdescr)
    aggdf <- aggdf[, 1:exuv]
  }
  
  exsum <- grep(glob2rx("*_sum"), names(aggdf))
  
  if (any(names(ki.data@Parameter) == "P_RT_NRT") == TRUE)
  {
    prsum <- grep(glob2rx("P_RT_NRT_sum"), names(aggdf))
    prmean <- grep(glob2rx("P_RT_NRT"), names(aggdf))
    aggdf[, prmean] <- aggdf[, prsum]
  }
  
  if (any(names(ki.data@Parameter) == "P_RT_NRT_01") == TRUE)
  {
    prsum <- grep(glob2rx("P_RT_NRT_01_sum"), names(aggdf))
    prmean <- grep(glob2rx("P_RT_NRT_01"), names(aggdf))
    aggdf[, prmean] <- aggdf[, prsum]
  }
  
  if (any(names(ki.data@Parameter) == "P_RT_NRT_02") == TRUE)
  {
    prsum <- grep(glob2rx("P_RT_NRT_02_sum"), names(aggdf))
    prmean <- grep(glob2rx("P_RT_NRT_02"), names(aggdf))
    aggdf[, prmean] <- aggdf[, prsum]
  }
  
  if (any(names(ki.data@Parameter) == "F_RT_NRT_01") == TRUE)
  {
    prsum <- grep(glob2rx("F_RT_NRT_01_sum"), names(aggdf))
    prmean <- grep(glob2rx("F_RT_NRT_01"), names(aggdf))
    aggdf[, prmean] <- aggdf[, prsum]
  }
  
  if (any(names(ki.data@Parameter) == "F_RT_NRT_02") == TRUE)
  {
    prsum <- grep(glob2rx("F_RT_NRT_02_sum"), names(aggdf))
    prmean <- grep(glob2rx("F_RT_NRT_02"), names(aggdf))
    aggdf[, prmean] <- aggdf[, prsum]
  }
  
  aggdf <- aggdf[, -exsum]
  
#   wdmin <- grep(glob2rx("WD_min"), names(aggdf))
#   wdmax <- grep(glob2rx("WD_max"), names(aggdf))
#   wdq25 <- grep(glob2rx("WD_25"), names(aggdf))
#   wdq75 <- grep(glob2rx("WD_75"), names(aggdf))
  
  aggdf <- round(aggdf, 2)

  #aggdf[, c(wdmin, wdmax, wdq25, wdq75)] <- NA
#   aggdf <- aggdf[, -c(wdmin, wdmax, wdq25, wdq75)]
  
  datetime <- rownames(aggdf)
  print(datetime)
  if(nchar(datetime) == 6){
    datetime <- paste(datetime, "0101", sep="")
  } 
  if(nchar(datetime) == 8){
    datetime <- paste(datetime, "01", sep="")
  } 
  datetime <- as.POSIXct(strptime(datetime, format = "%Y%m%d%H"), 
                         origin = ki.data@Origin) 
  
  aggdf <- data.frame(Datetime = datetime, 
                      Timezone = timezone,
                      Aggregationtime = aggregationtime,
                      PlotId = plotid,
                      EpPlotId = epplotid,
                      StationId = stationid,
                      Processlevel = processlevel,
                      Qualityflag = qualityflag,
                      aggdf, stringsAsFactors = FALSE)
  
  return(aggdf)
  
  Sys.setenv(TZ = Old.TZ)

}

#    test <- aggregate.ki.data("/home/ede/software/testing/julendat/processing/plots/ki/0000cof3/qc25_fah01_0290/ki_0000cof3_000pu1_201101010000_201112310000_eat_qc25_fah01_0290.dat", "month")
#    str(test)
# setwd("/home/dogbert/workspace/julendat/src/julendat/rmodules/")

aggregate.ki.data <- function(input,
                              level = "1h",
                              plevel = 0000,
                              start.column = 9,
                              detail,
                              project = "ki",
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
         "year" = agglevel <- ki.data@AggregationLevels$AggYear,
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
         "year" = aggunit <- "y",
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
         "year" = aggint <- "01",
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
  
  if (detail) {
    aggdescr <- c("", "_min", "_max", "_median", "_stdv", 
                "_25", "_75", "_sum", "_n", "_nan")
  } else {
    aggdescr <- c("", "_sum")
  }
  names.prm <- rep(names.prm.df, each = length(aggdescr))
  aggnames <- paste(names.prm, aggdescr, sep = "")

  prm.ls <- split(prm.df, agglevel)

  agglist <- lapply(seq(prm.ls), function(i) {
    
    lapply(seq(prm.df), function(j) {
      if (detail){
#         print("detail=true")
	      list(mean(prm.ls[[i]][[j]], na.rm = T),
	           min(prm.ls[[i]][[j]], na.rm = T),
	           max(prm.ls[[i]][[j]], na.rm = T),
	           median(prm.ls[[i]][[j]], na.rm = T),
	           sd(prm.ls[[i]][[j]], na.rm = T),
	           quantile(prm.ls[[i]][[j]], na.rm = T, probs = 0.25, names = F),
	           quantile(prm.ls[[i]][[j]], na.rm = T, probs = 0.75, names = F),
	           sum(prm.ls[[i]][[j]], na.rm = T),
	           sum(complete.cases(prm.ls[[i]][[j]])),
	           length(prm.ls[[i]][[j]]) - sum(complete.cases(prm.ls[[i]][[j]]))
	           )
       } else {
#           print("detail=false")
         if (any(!is.na(prm.ls[[i]][[j]]))) {
         	list(mean(prm.ls[[i]][[j]], na.rm = T),
          		sum(prm.ls[[i]][[j]], na.rm = T)
          	)
         } else {
           list(NA, NA)
         }
       }
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

    if (detail) {
      for (i in 1:(length(wd) - 2)) {
        aggdf[, posWD[i]] <- uv2wd(aggdf[, posu[i]], aggdf[, posv[i]])
      }
    } else {
      for (i in 1:(length(wd))) {
        aggdf[, posWD[i]] <- uv2wd(aggdf[, posu[i]], aggdf[, posv[i]])
      }
    }
  
    exuv <- length(ki.data@Parameter) * length(aggdescr)
    aggdf <- aggdf[, 1:exuv]
  }
  
  exsum <- grep(glob2rx("*_sum"), names(aggdf))
  
  if (any(names(ki.data@Parameter) == "P_RT_NRT") == TRUE & project == "be" & level == "1h")
  {
    prmean <- grep(glob2rx("P_RT_NRT"), names(aggdf))
    aggdf[, prmean] <- aggdf[, prmean] * 60.0
  } else if (any(names(ki.data@Parameter) == "P_RT_NRT") == TRUE)
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
  
  aggdf <- aggdf[, -exsum, drop = FALSE]

#   wdmin <- grep(glob2rx("WD_min"), names(aggdf))
#   wdmax <- grep(glob2rx("WD_max"), names(aggdf))
#   wdq25 <- grep(glob2rx("WD_25"), names(aggdf))
#   wdq75 <- grep(glob2rx("WD_75"), names(aggdf))
  
  aggdf <- round(aggdf, 3)

  #aggdf[, c(wdmin, wdmax, wdq25, wdq75)] <- NA
#   aggdf <- aggdf[, -c(wdmin, wdmax, wdq25, wdq75)]
  
  datetime <- rownames(aggdf)

# BUG 20.02.2014
# processing level: 200 
# File: ki_0000fod2_000pu1_201310010000_201310312355_eat_qc01_cti05_0100
# Reasens: - datetime was NULL, because exsum = -2 ???
# Change Start SF ######################################################
#   if (length(datetime) == 0) {
#     aggdf <- as.data.frame(do.call("rbind", agglist))
#     datetime <- rownames(aggdf)
  }
# Change End      ######################################################


  if(nchar(datetime) == 6){
    datetime <- paste(datetime, "0101", sep="")
  } 
  if(nchar(datetime) == 8){
    datetime <- paste(datetime, "01", sep="")
  } 
  if (level == "year") datetime <- as.character((unique(ki.data@AggregationLevels$AggYear))) else {
    
     datetime <- as.POSIXct(strptime(datetime, format = "%Y%m%d%H"), 
                             origin = ki.data@Origin)
  }
                              
  
  aggdf <- data.frame(Datetime = as.character(datetime), 
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

#   test <-write.aggregate.ki.data(
#   inputfilepath="/media/dogbert/dev/BE/julendat/processing/plots/be/000AEG01/fc01_fah01_0190/be_000AEG01_00EEMU_200912010000_200912310000_mez_fc01_fah01_0190.dat",
#   outputfilepath="/media/dogbert/dev/BE/julendat/processing/plots/be/000AEG01/fa01_fah01_0200/be_000AEG01_00EEMU_200912010000_200912310000_mez_fa01_fah01_0200.dat",
#   level="1h")

#   # test <- aggregate.ki.data("/media/dogbert/dev/BE/julendat/processing/plots/be/000AEG01/fc01_fah01_0190/be_000AEG01_00EEMU_200901010000_200901310000_mez_fc01_fah01_0190.dat", "1h")
#    str(test)

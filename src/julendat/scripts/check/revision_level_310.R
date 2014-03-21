rm(list=ls())
library(zoo)
library(forecast)

compute.thv <- FALSE
if(compute.thv){
  compute.revision <- FALSE
} else {
  compute.revision <- TRUE
}

location = "AEG"
station = "CEMU"

setwd(paste("/media/jsonne/Volume/bexis/revision_level_310/310", location, 
            sep = "/"))
thvs.file <- paste("thvs_", location, "_", station, ".dat", sep = "")


# Compute THVs
if(compute.thv){
  files <- list.files(path = paste(location, "original", sep = "_"), 
                      pattern = glob2rx(paste("*", station, "*_0310.dat", 
                                              sep = "")),
                      full.names = TRUE, recursive = TRUE)
  datasets <- lapply(files, function(x){
    act.file <- x
    act.data <- read.table(act.file, sep = ",", header = TRUE)
  })
  data <- do.call("rbind", datasets)
  
  if(location == "AEG"){
    thvs.prob.t <- c(0.01, 0.995)
    thvs.prob.r <- c(0.02, 0.60)
    thvs.prob.ts <- c(0.01, 0.995)
  } else if (location == "AEW") {
    thvs.prob.t <- c(0.003, 0.995)
    thvs.prob.r <- c(0.02, 0.80)
    thvs.prob.ts <- c(0.0008, 0.995)
  } 
  thvs.ta_200 <- quantile(data$Ta_200, probs = thvs.prob.t, na.rm = TRUE)
  thvs.rh_200 <- quantile(data$rH_200, probs = thvs.prob.r, na.rm = TRUE)
  thvs.Ts_5 <- quantile(data$Ts_5, probs = thvs.prob.ts, na.rm = TRUE)
  thvs.Ts_10 <- quantile(data$Ts_10, probs = thvs.prob.ts, na.rm = TRUE)
  thvs.Ts_20 <- quantile(data$Ts_20, probs = thvs.prob.ts, na.rm = TRUE)
  thvs.Ts_50 <- quantile(data$Ts_50, probs = thvs.prob.ts, na.rm = TRUE)
  thvs.Ts_10 <- thvs.Ts_5
  thvs.Ts_20 <- thvs.Ts_5
  thvs.Ts_50 <- thvs.Ts_5
  
  thvs <- data.frame(Ta_200 = thvs.ta_200,
                     rH_200 = thvs.rh_200,
                     Ts_5 = thvs.Ts_5,
                     Ts_10 = thvs.Ts_10,
                     Ts_20 = thvs.Ts_20,
                     Ts_50 = thvs.Ts_50)
  
  write.table(thvs, thvs.file, sep = ",", row.names = FALSE)
}

# Compute revision
if(compute.revision){
  thvs <- read.table(thvs.file, sep = ",", header = TRUE)
  files <- list.files(path = paste(location, "revised", sep = "_"), 
                      pattern = glob2rx(paste("*", station, "*_0310.dat", 
                                              sep = "")),
                      full.names = TRUE, recursive = TRUE)
  sapply(files, function(x){
    act.file <- x
    print(act.file)
    act.data <- read.table(act.file, sep = ",", header = TRUE)
    back <- lapply(colnames(thvs), function(z){
      act.parameter <- z
      act.col <- which(colnames(act.data) == act.parameter)
      act.thv <- thvs[, which(colnames(thvs) == act.parameter)]
      first.non.na <- min(which(!is.na(act.data[, act.col])))
      last.non.na <- max(which(!is.na(act.data[, act.col])))
      act.data[, act.col][act.data[, act.col] < act.thv[1] |
                            act.data[, act.col] > act.thv[2]] <- NaN
      if(sum(!is.na(act.data[, act.col])) >= 2 &
           sum(is.na(act.data[, act.col])) > 0){
        act.data.zoo <- read.zoo(act.data)
        act.col.zoo <- which(colnames(act.data.zoo) == act.parameter)
        act.data.zoo.approx <- na.interp(act.data.zoo[, act.col.zoo])
        act.data.zoo.approx.df <- as.data.frame(act.data.zoo.approx)
        corrected <- as.numeric(act.data.zoo.approx.df$x)
      } else {
        corrected <- act.data[, act.col]
      }
      if(is.finite(first.non.na) & first.non.na > 1){
        corrected[1:first.non.na] <- NaN
      }
      if(is.finite(last.non.na) & last.non.na < length(corrected)){
        corrected[last.non.na:length(act.data[, act.col])] <- NaN
      }
      return(corrected)
    })
    for(i in 1:length(colnames(thvs))){
      act.parameter <- colnames(thvs)[i]
      act.col <- which(colnames(act.data) == act.parameter)
      act.data[, act.col] <- back[[i]]
    }
    write.table(act.data, act.file, sep = ",", row.names = FALSE)
#     write.table(act.data, paste(substr(act.file, 1, nchar(act.file)-4), 
#                                 "revised.csv", sep = "_"),
#                 sep = ",", row.names = FALSE)
  })
}


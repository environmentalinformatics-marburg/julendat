rm(list=ls())

# Set path environment
setwd("/media/memory01/ei_data_exploratories/processing/plots/")
level = "_0400.dat"

# Set threshold values
switch(level,
       "_0405.dat" = thv <- 0, # daily
       "_0400.dat" = thv <- 24*5, # monthly
       "_0420.dat" = thv <- 24*20 # annual
)

# Check parameters for NaN
parameters <- c("Ta_200", "Ta_10", "rH_200",
                "Ts_5", "Ts_10", "Ts_20", "Ts_50")
precipitation <- c("P_RT_NRT", "P_container_RT", "P_container_NRT")
act.path <- "revised_reloaded_0400plus/"
act.files <- list.files(path = act.path,
                        pattern = level,
                        full.names = TRUE, recursive = TRUE)

act.files.vip <- Filter(function(x) grepl("(E|A)EMU", x), act.files)
act.files.cemu <- Filter(function(x) grepl("CEMU", x), act.files)

# revision for all CEMU-files
sapply(act.files.cemu, function(x){
  act.file <- x
  print(act.file)
  act.data <- read.table(act.file, header = TRUE, sep = ",")
  for(i in seq(1, length(parameters))){
    act.parameter <- parameters[i]
    act.col <- which(colnames(act.data) == act.parameter)
    check.col <- which(colnames(act.data) == paste(act.parameter, "nan", 
                                                   sep ="_"))
    if(nrow(act.data[act.data[, check.col] > thv, ]) > 0){
      print("replacing...")
      for(c in seq(check.col - 8, check.col)){
        print(c)
        act.data[act.data[, check.col] > thv, ][, c] <- NaN  
      }
    }
  }
  
  out.file <- gsub("revised_reloaded_level_0310_plus", 
                   "revised_reloaded_level_0400_plus", act.file)
  dir.create(dirname(out.file), recursive = TRUE, showWarnings = FALSE)
  write.table(act.data, out.file, sep = ",", row.names = FALSE)
})

# revision for all AEMU-/EEMU-files
sapply(act.files.vip, function(x){
  act.file <- x
  print(act.file)
  act.data <- read.table(act.file, header = TRUE, sep = ",")
  for(i in seq(1, length(parameters))){
    act.parameter <- parameters[i]
    act.col <- which(colnames(act.data) == act.parameter)
    check.col <- which(colnames(act.data) == paste(act.parameter, "nan", 
                                                   sep ="_"))
    if(nrow(act.data[act.data[, check.col] > thv, ]) > 0){
      print("replacing...")
      for(c in seq(check.col - 8, check.col)){
        print(c)
        act.data[act.data[, check.col] > thv, ][, c] <- NaN  
      }
    }
  }
  
  for(i in seq(1, length(precipitation))){
    act.parameter <- precipitation[i]
    act.col <- which(colnames(act.data) == act.parameter)
    check.col <- which(colnames(act.data) == paste(act.parameter, "nan", 
                                                   sep ="_"))
    #The following three lines are necessary in case of "NA"-values in the columns "P_RT_NRT_nan",
    #"P_container_RT_nan" and "P_container_NRT_nan"
    #if(is.na(act.data[, check.col])){
    #  act.data[, check.col] <- 9999
    #}
    if(nrow(act.data[act.data[, check.col] > thv, ]) > 0){
      print("replacing...")
      for(c in seq(check.col - 8, check.col)){
        print(c)
        act.data[act.data[, check.col] > thv, ][, c] <- NaN  
      }
    }
  }
  
  out.file <- gsub("revised_reloaded_level_0310_plus", 
                   "revised_reloaded_level_0400_plus", act.file)
  dir.create(dirname(out.file), recursive = TRUE, showWarnings = FALSE)
  write.table(act.data, out.file, sep = ",", row.names = FALSE)
})



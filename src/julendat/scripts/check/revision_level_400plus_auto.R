rm(list=ls())

# Set path environment
setwd("/media/permanent/active/bexis/processing")
level = "_0420.dat"

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
act.path <- "revised_reloaded_level_0310_plus"
act.files <- list.files(path = act.path,
                        pattern = level,
                        full.names = TRUE, recursive = TRUE)

x <- act.files[1]
sapply(act.files, function(x){
  act.file <- x
  print(act.file)
  act.data <- read.table(act.file, header = TRUE, sep = ",")
  i <- 1
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
    if(length(check.col) > 0){
      print("replacing...")
      for(c in seq(check.col - 8, check.col)){
        print(c)
        act.data[, c] <- NaN  
      }
    }
  }
  
  out.file <- gsub("revised_reloaded_level_0310_plus", 
                   "revised_reloaded_level_0400_plus", act.file)
  dir.create(dirname(out.file), recursive = TRUE, showWarnings = FALSE)
  write.table(act.data, out.file, sep = ",", row.names = FALSE)
})

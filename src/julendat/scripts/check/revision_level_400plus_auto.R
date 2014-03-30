rm(list=ls())

# Set path environment
setwd("/media/permanent/active/bexis/processing/")
level = "_0420.dat"
thv = 24*20

# Functions
trim <- function (x) gsub("^\\s+|\\s+$", "", x)

# Check parameters for NaN
parameters <- c("Ta_200", "Ta_10", "rH_200",
                "Ts_5", "Ts_10", "Ts_20", "Ts_50")
act.path <- "revised_reloaded"
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
      act.data[act.data[, check.col] > thv, ][, act.col] <- NaN
    }
  }
  out.file <- gsub("revised_reloaded", 
                   "revised_reloaded_level0400plus", act.file)
  dir.create(dirname(out.file), recursive = TRUE, showWarnings = FALSE)
  write.table(act.data, out.file, sep = ",", row.names = FALSE)
})

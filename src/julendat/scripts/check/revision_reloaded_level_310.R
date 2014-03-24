rm(list=ls())

# Set path environment
location = "AEG"
setwd("D:/active/bexis/level_0310_hourly/processing/")
revision.file <- paste(location, "_revised_reloaded.csv",sep = "")

# Functions
trim <- function (x) gsub("^\\s+|\\s+$", "", x)

# Read revision information
revision.info <- read.csv(revision.file, header = TRUE, sep = ",")

# Revise data
sapply(seq(1, nrow(revision.info)), function(x){
  act.plotid <- paste("000", revision.info$PlotId[x], sep = "")
  act.parameter <- as.character(revision.info$Parameter[x])
  act.year <- as.character(revision.info$Year[x])
  act.range <- trim(as.character(revision.info$Range[x]))
  if(grepl("-", act.range)){
    sep <- gregexpr(pattern = "-", act.range)[[1]][1]
    act.range <- seq(substr(act.range, 1, sep-1), 
                     substr(act.range, sep+1, nchar(act.range)))
  } else {
    act.range <- as.numeric(act.range)
  }
  act.path <- paste(location, "_revised/be/", 
                    act.plotid, "/gc02_fah01_0310/", sep = "")
  act.file <- list.files(path = act.path, 
                         pattern = paste("_", act.year, sep = ""),
                         full.names = TRUE, recursive = TRUE)
  out.file <- gsub("AEG_revised", "AEG_revision_reloaded", act.file)
  if(file.exists(out.file)){
    act.file <- out.file
  }
  act.data <- read.csv(act.file, header = TRUE, sep = ",")
  act.col <- which(colnames(act.data) == act.parameter)
  for(i in seq(1, length(act.range))){
    act.datetime <- paste(act.year, sprintf("%02d", act.range[i]), sep = "-")
    act.data[grep(act.datetime, act.data$Datetime), ][, act.col] <- NaN
  }
  dir.create(dirname(out.file), recursive = TRUE, showWarnings = FALSE)
  write.table(act.data, out.file, sep = ",", row.names = FALSE)
})


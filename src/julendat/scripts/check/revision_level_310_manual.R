rm(list=ls())

# Set path environment
location = "HEW"
revision.file <- tolower(paste0(getwd(), "/", location, "_revised_reloaded.csv"))
path.prefix <- "/media/memory01/ei_data_pastprocessing/processing/plots/"
setwd(paste0(path.prefix))

# Functions
trim <- function (x) gsub("^\\s+|\\s+$", "", x)

# Copy files to working folder
act.path <- paste(location, "_revised/be", sep = "")
act.files <- list.files(path = act.path,
                        pattern = ".dat",
                        full.names = TRUE, recursive = TRUE)
sapply(act.files, function(x){
  act.file <- x
  out.file <- gsub(paste(location, "revised", sep = "_"), 
                   paste(location, "revised_reloaded", sep = "_"), act.file)
  dir.create(dirname(out.file), recursive = TRUE, showWarnings = TRUE)
  file.copy(act.file, out.file)
})

# Read revision information
revision.info <- read.csv(revision.file, header = TRUE, sep = ",")
revision.info <- subset(revision.info, revision.info$PlotId != "AEG35")
print(revision.info)
# Revise data
sapply(seq(1, nrow(revision.info)), function(x){
  act.plotid <- paste("000", revision.info$PlotId[x], sep = "")
  act.parameter <- as.character(revision.info$Parameter[x])
  act.year <- as.character(revision.info$Year[x])
  act.range <- trim(as.character(revision.info$Range[x]))
  if(grepl("-", act.range)){
    sep <- gregexpr(pattern = "-", act.range)[[1]][1]
    act.range <- seq(as.numeric(substr(act.range, 1, sep-1)),
                     as.numeric(substr(act.range, sep+1, nchar(act.range))))
  } else {
    act.range <- as.numeric(act.range)
  }
  act.path <- paste(location, "_revised_reloaded/be/",
                    act.plotid, "/gc02_fah01_0310", sep = "")
  act.file <- list.files(path = act.path,
                         pattern = paste("_", act.year, sep = ""),
                         full.names = TRUE, recursive = TRUE)
#   out.file <- gsub(paste(location, "revised", sep = "_"), 
#                    paste(location, "revised_reloaded", sep = "_"), act.file)
  print(act.file)
#   print(out.file)
  print(act.parameter)
#   if(!file.exists(out.file)){
#     dir.create(dirname(out.file), recursive = TRUE, showWarnings = TRUE)
#     file.copy(act.file, out.file)
#   }
  sapply(act.file, function(x){
    if(file.exists(x)){
      act.data <- read.csv(x, header = TRUE, sep = ",")
      act.col <- which(colnames(act.data) == act.parameter)
      for(i in seq(1, length(act.range))){
      act.datetime <- paste(act.year, sprintf("%02d", act.range[i]), sep = "-")
      act.data[grep(act.datetime, act.data$Datetime), ][, act.col] <- NaN
      }
      write.table(act.data, x, sep = ",", row.names = FALSE)
    } else {
      print(paste0("Non existing file: ", x))
    }
  })
})



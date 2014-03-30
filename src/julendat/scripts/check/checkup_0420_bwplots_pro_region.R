rm(list=ls())
library(lattice)

setwd("/media/permanent/active/bexis/processing")
files <- list.files(path = "data", pattern = "csv",
                    full.names = TRUE, recursive=T)
sapply(files, function(z){
  act.file = z
  print(act.file)
  data <- read.table(act.file, sep = ";", h=T)
  data.subset <- subset(data, data$Datetime > 2008)
  
  vars.lst <- list(vars = c("Ta_200", "rH_200",
                            "Ts_5", "Ts_10", "Ts_20", "Ts_30", "Ts_40", "Ts_50", 
                            "SM_10"),
                   ylims = list(Ta_200 = c(0, 20),
                                rH_200 = c(0, 100),
                                Ts_5 = c(0, 20),
                                Ts_10 = c(0, 20),
                                Ts_20 = c(0, 20),
                                Ts_30 = c(0, 20),
                                Ts_40 = c(0, 20),
                                Ts_50 = c(0, 20),
                                SM_10 = c(0, 65)))
  
  if(grepl("CEMU", act.file)) {
    jpg.name <- paste("check/", substr(act.file, nchar(act.file)-15,
                                       nchar(act.file)-4), sep = "")
    table.name <- paste("check/", substr(act.file, nchar(act.file)-15,
                                         nchar(act.file)-4), sep = "")
  } else {
    jpg.name <- paste("check/", substr(act.file, nchar(act.file)-14,
                                       nchar(act.file)-4), sep = "")
    table.name <- paste("check/", substr(act.file, nchar(act.file)-14,
                                         nchar(act.file)-4), sep = "")
  }
  jpeg(filename=paste(jpg.name, "_%7d.jpeg", sep=""), quality=100, width=800)
  sapply(vars.lst$vars, function(y){
    act.var <- y
    ylims <- vars.lst$ylims[[act.var]]
    if(act.var %in% colnames(data.subset)) {
      act.col <- which(colnames(data.subset) == act.var)
      print(bwplot(data.subset[,act.col] ~ data.subset$PlotId, 
                   ylim = ylims,
                   scales = list(x = list(rot = 45, cex=0.8, labels=substr(unique(data.subset$PlotId),4,8))),
                   main = paste(substr(z,6,8), substr(z,14, nchar(z)-4), sep=" "), ylab=act.var))

      print(act.col)
    }
  })
  dev.off()
})


rm(list=ls())

# just adjust the following four parameters and
# in case of editing level 0420 uncomment line 28
# in case of editing level 0310 comment line 23
level = "0310" # "0310", "0400", "0405" or "0420"
region = "SCH" # "ALB", "HAI" or "SCH"
station = "CEMU" # "CEMU" or "AEMU_EEMU"
date = "20140812" # date of today

setwd(paste("/media/dogbert/DEV/ready_for_bexis/eipastprocessing/", level, "/", region, "_",
            station, "_",level, "_original", sep=""))

scr_path = paste("/media/dogbert/DEV/ready_for_bexis/eipastprocessing/", level, "/", region, "_",
                 station, "_",level, "_original", sep="")
new_path = paste("/media/dogbert/DEV/ready_for_bexis/eipastprocessing/", level, "/", region, "_",
                station, "_",level, "_", date, sep="")
files <- list.files(pattern=paste("_", level ,".dat" ,sep=""), recursive=TRUE, full.names=TRUE)

dat.list <- lapply(files, function(i) {
  dat <- read.table(i, header = T, sep = ",", stringsAsFactors = F)
  dat <- (dat[, -grep("EpPlotId", names(dat)),])
  dat <- (dat[, -grep("Qualityflag", names(dat)),]) # not needed for level 0310
  return(dat)
})

for (activ_file in dat.list){
  #activ_file$Datetime <- paste(activ_file$Datetime, "-01-01 01:00:00", sep="") # only needed for level 0420
  year <- substr(as.Date(activ_file$Datetime[1]), 1,4)

  plotId.head <- substr(activ_file$PlotId[1], 4,6)
  plotId.numbers <- substr(activ_file$PlotId, 7,8)
  plotId.checks <- substr(activ_file$PlotId[1], 7,7)
  stationId <- substr(activ_file$StationId[1], 3,6)
    
  if(plotId.checks == "0"){
    plotId.numbers<- substr(activ_file$PlotId, 8,8)
  }
  activ_file$PlotId <- paste0(plotId.head, plotId.numbers)
  write.csv(activ_file, paste(new_path, paste0("/", plotId.head, plotId.numbers[1],"_",level,"_",stationId,"_", year,".txt"),
                              sep=""), row.names=F, na="NA")
}



  


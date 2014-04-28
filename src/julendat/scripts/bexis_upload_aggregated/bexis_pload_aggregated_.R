setwd("/media/dogbert/dev/be/julendat/processing/plots/")

level = "0400"
scr_path = "/media/dogbert/dev/be/julendat/processing/"
new_path ="/media/dogbert/dev/be/julendat/processing/"
files <- list.files(paste0(path,"plots/"), pattern=glob2rx(paste0("*", level,".dat")), recursive=TRUE, full.names=TRUE)


dat.list <- lapply(files, function(i) {
  dat <- read.table(i, header = T, sep = ",", stringsAsFactors = F)
  dat <- (dat[, -grep("EpPlotId", names(dat)),])
  return(dat[, -grep("Qualityflag", names(dat)),])
})

for (activ_file in dat.list){
  year <- substr(as.Date(activ_file$Datetime[1]), 1,4)

  plotId.head <- substr(activ_file$PlotId[1], 4,6)
  plotId.numbers <- substr(activ_file$PlotId, 7,8)
  plotId.checks <- substr(activ_file$PlotId[1], 7,7)
  stationId <- substr(activ_file$StationId[1], 3,6)
    
  if(plotId.checks == "0"){
    plotId.numbers<- substr(activ_file$PlotId, 8,8)
  }
  activ_file$PlotId <- paste0(plotId.head, plotId.numbers)
  write.csv(activ_file, paste(new_path, paste0(plotId.head, plotId.numbers[1],"_",level,"_",stationId,"_", year,".txt"), sep=""), row.names=F, na="NA")
  
}



  


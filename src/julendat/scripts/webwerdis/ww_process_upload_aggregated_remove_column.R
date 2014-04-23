setwd("/media/dogbert/dev/be/julendat/processing/plots/")

level = "0400"
files <- list.files("/media/dogbert/dev/be/julendat/processing/plots/", pattern=glob2rx(paste0("*", level,".dat")), recursive=TRUE, full.names=TRUE)


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
  if(plotId.checks == "0"){
    plotId.numbers<- substr(activ_file$PlotId, 8,8)
  }
  activ_file$PlotId <- paste0(plotId.head, plotId.numbers)
  write.csv(activ_file, paste("/media/dogbert/dev/be/julendat/processing/", paste0(plotId.head, plotId.numbers[1],"_",level,"_", year,".csv"), sep=""), row.names=F, na="nan")
  
}



  


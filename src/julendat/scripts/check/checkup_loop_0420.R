rm(list=ls())
library(lattice)

setwd("/media/jsonne/Volume/bexis/temp/mannualy_corrected_420_final")
files <- list.files(path = "data/", pattern = "csv",
                    full.names = TRUE)
# in list.files habe ich das "recursive=T" entfernt
sapply(files, function(z){
  act.file = z
  print(act.file)
  data <- read.table(act.file, sep = "\t", h=T)
  data.subset <- subset(data, data$Datetime > 2008)
  
  vars.lst <- list(vars = c("Ta_200", "rH_200",
                            "Ts_5", "Ts_10", "Ts_20", "Ts_30", "Ts_40", "Ts_50", 
                            "SM_10", "SM_15", "SM_20", "SM_30", "SM_40", "SM_50"),
                   ylims = list(Ta_200 = c(0, 20),
                                rH_200 = c(0, 100),
                                Ts_5 = c(0, 20),
                                Ts_10 = c(0, 20),
                                Ts_20 = c(0, 20),
                                Ts_30 = c(0, 20),
                                Ts_40 = c(0, 20),
                                Ts_50 = c(0, 20),
                                SM_10 = c(0, 65),
                                SM_15 = c(0, 65),
                                SM_20 = c(0, 65),
                                SM_30 = c(0, 65),
                                SM_40 = c(0, 65),
                                SM_50 = c(0, 65)),
                   thvs = list(Ta_200 = 3,
                               rH_200 = 10,
                               Ts_5 = 3,
                               Ts_10 = 3,
                               Ts_20 = 3,
                               Ts_30 = 3,
                               Ts_40 = 3,
                               Ts_50 = 3,
                               SM_10 = 10,
                               SM_15 = 10,
                               SM_20 = 10,
                               SM_30 = 10,
                               SM_40 = 10,
                               SM_50 = 10))
  
  if(grepl("CEMU", act.file)) {
    pdf.name <- paste("check/", substr(act.file, nchar(act.file)-15,
                                       nchar(act.file)-4), ".pdf", sep = "")
    table.name <- paste("check/", substr(act.file, nchar(act.file)-15,
                                         nchar(act.file)-4), sep = "")
  } else {
    pdf.name <- paste("check/", substr(act.file, nchar(act.file)-14,
                                       nchar(act.file)-4), ".pdf", sep = "")
    table.name <- paste("check/", substr(act.file, nchar(act.file)-14,
                                         nchar(act.file)-4), sep = "")
  }
  pdf(pdf.name)
  sapply(vars.lst$vars, function(y){
    act.var <- y
    ylims <- vars.lst$ylims[[act.var]]
    thv <- vars.lst$thvs[[act.var]]
    if(act.var %in% colnames(data.subset)) {
      act.col <- which(colnames(data.subset) == act.var)
      print(bwplot(data.subset[,act.col] ~ data.subset$PlotId, 
                   ylim = ylims,
                   scales = list(x = list(rot = 45)),
                   main = z, sub = paste(act.var, thv, sep = " THV:")))
      test <- aggregate(data.subset[,act.col], by = list(data.subset$PlotId) , FUN=quantile, na.rm = TRUE)
      test <- as.data.frame(test)
      colnames(test) <- c("PlotId", "Q")
      test$check <- test$Q[,5] - test$Q[,1]
      critical <- subset(test, test$check > thv)
      if(nrow(critical) > 0) {
        out <- do.call("rbind", lapply(critical$PlotId, function(x) {
          df <- data.frame(PlotId = x,
                           Years = data.subset[grepl(x, data.subset$PlotId), ]$Datetime,
                           act.var = data.subset[grepl(x, data.subset$PlotId), ][,act.col],
                           Q000 = test[grepl(x, test$PlotId), ]$Q[,1],
                           Q100 = test[grepl(x, test$PlotId), ]$Q[,5],
                           QDiff = test[grepl(x, test$PlotId), ]$check)
        }))
        colnames(out) <- c("PlotId", "Years", act.var, "Q000", "Q100", "QDiff")
        write.table(out, file=paste(table.name, "_", act.var, ".dat", 
                                    sep = ""), sep=";", row.names=F, 
                    append = FALSE)
      }        
      out.all <- do.call("rbind", lapply(test$PlotId, function(x) {
        df <- data.frame(PlotId = x,
                         Years = data.subset[grepl(x, data.subset$PlotId), ]$Datetime,
                         act.var = data.subset[grepl(x, data.subset$PlotId), ][,act.col],
                         Q000 = test[grepl(x, test$PlotId), ]$Q[,1],
                         Q100 = test[grepl(x, test$PlotId), ]$Q[,5],
                         QDiff = test[grepl(x, test$PlotId), ]$check)
      }))
      colnames(out.all) <- c("PlotId", "Years", act.var, "Q000", "Q100", "QDiff")
      
      write.table(out.all, file=paste(table.name, "_", act.var, "_all.dat", 
                                      sep = ""), sep=";", row.names=F,
                  append = FALSE)
      print(act.col)
    }
  })
  dev.off()
})


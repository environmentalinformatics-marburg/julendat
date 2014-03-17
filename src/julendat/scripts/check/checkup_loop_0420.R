rm(list=ls())
library(lattice)

setwd("/media/permanent/development/test/julendat/aggregated/")
files <- list.files(path = ".", pattern = ".csv", recursive = TRUE,
                    full.names = TRUE)
sapply(files, function(z){
  act.file = z
  print(act.file)
  data <- read.table(act.file, sep = "\t", h=T)
  data.subset <- subset(data, data$Datetime > 2008)
  vars <- c("Ta_200", "rH_200",
            "Ts_5", "Ts_10", "Ts_20", "Ts_30", "Ts_40", "Ts_50", 
            "SM_10", "SM_15", "SM_20", "SM_30", "SM_40", "SM_50")
  if(grepl("CEMU", act.file)) {
    pdf.name <- paste(substr(act.file, nchar(act.file)-15,nchar(act.file)-4),
                      ".pdf", sep = "")
    table.name <- paste(substr(act.file, nchar(act.file)-15,nchar(act.file)-4),
                        sep = "")
  } else {
    pdf.name <- paste(substr(act.file, nchar(act.file)-14,nchar(act.file)-4),
                      ".pdf", sep = "")
    table.name <- paste(substr(act.file, nchar(act.file)-14,nchar(act.file)-4),
                        sep = "")
  }
  pdf(pdf.name)
  sapply(vars, function(y){
    act.var <- y
    if(act.var %in% colnames(data.subset)) {
      act.col <- which(colnames(data.subset) == act.var)
      print(bwplot(data.subset[,act.col] ~ data.subset$PlotId, 
                   scales = list(x = list(rot = 45)),
                   main = z, sub = act.var))
      test <- aggregate(data.subset[,act.col], by = list(data.subset$PlotId) , FUN=quantile, na.rm = TRUE)
      test <- as.data.frame(test)
      colnames(test) <- c("PlotId", "Q")
      test$check <- test$Q[,5] - test$Q[,1]
      critical <- subset(test, test$check > 10.0)
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


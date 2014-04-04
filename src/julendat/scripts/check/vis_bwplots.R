rm(list=ls())
library(lattice)
# Set path environment
wdpath <- "/media/permanent/active/bexis/processing/revised_reloaded_level_0400_plus"
setwd(wdpath)

level = "_0420"

parameters <- c("Ta_200", "rH_200",
                "Ts_5", "Ts_10", "Ts_20", "Ts_30", "Ts_40", "Ts_50", 
                "SM_10")
                 
regions <- c("AEG", "AEW", "HEG", "HEW", "SEG", "SEW")

ylims = list(ylims_0400 = list(Ta_200 = c(-20, 40),
                               rH_200 = c(20, 100),
                               Ts_5 = c(-20, 40),
                               Ts_10 = c(-20, 40),
                               Ts_20 = c(-20, 40),
                               Ts_30 = c(-20, 40),
                               Ts_40 = c(-20, 40),
                               Ts_50 = c(-20, 40),
                               SM_10 = c(0, 90)),
             ylims_0420 = list(Ta_200 = c(0, 17),
                               rH_200 = c(60, 100),
                               Ts_5 = c(0, 17),
                               Ts_10 = c(0, 17),
                               Ts_20 = c(0, 17),
                               Ts_30 = c(0, 17),
                               Ts_40 = c(0, 17),
                               Ts_50 = c(0, 17),
                               SM_10 = c(0, 65)))


act.ylims.col <- act.vis.col <- which(substr(names(ylims), 6, 10) == level)
act.ylims <- ylims[act.ylims.col][[1]]

files <- list.files(path = ".",
                    pattern = glob2rx(paste("*", level, ".dat", sep = "")),
                    full.names = TRUE, recursive = TRUE)

x <- parameters[1]
sapply(parameters, function(x){
  act.parameter <- x
  y <- regions[1]
  sapply(regions, function(y){
    act.region <- y
    region.files <- subset(files, grepl(act.region, unlist(files)))
    act.vis.data <- lapply(region.files, function(z){
      act.file <- z
      act.data <- read.csv(act.file, header = TRUE, sep = ",")
      act.col <- which(colnames(act.data) == act.parameter)
      act.df <- data.frame(PlotId = act.data$PlotId,
                           Year = act.data$Datetime,
                           Value = act.data[, act.col])
    })
    act.vis.data <- do.call("rbind", act.vis.data)
    act.vis.col <- which(names(act.ylims) == act.parameter)
    act.plot <- bwplot(act.vis.data$Value ~ act.vis.data$PlotId,
                       ylim = unlist(act.ylims[act.vis.col]),
                       par.settings = list(box.rectangle = list(col = "black"),
                                           box.umbrella = list(col = "black",
                                                               lty = 1),
                                           plot.symbol = list(col = "black",
                                                              pch = 4)), 
                       scales = list(x = list(rot = 45, cex=0.8, 
                                              labels = substr(unique(act.vis.data$PlotId), 4, 8))),
                       main = paste(act.region, act.parameter, 
                                    "level", substr(level, 2, 5),
                                    sep=" "), 
                       ylab = act.parameter)
    out.filepath <- paste(wdpath, "/vis/bwplots/level_", substr(level, 2, 5),"/", 
                          act.region, "_", act.parameter, "_",
                          "level_", substr(level, 2, 5),
                          ".jpg", sep="")
    dir.create(dirname(out.filepath), recursive = TRUE, showWarnings = FALSE)
    jpeg(out.filepath, quality=100, width=800)
    print(act.plot)
    dev.off()
    
  })
})
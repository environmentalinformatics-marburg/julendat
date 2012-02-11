source("VStationData.R")
source("VColList.R")
#inpath <- "D:/development/test/julendat/processing/plots/be"
inpath <- "/media/permanent/development/test/julendat/processing/plots/be"

verbose <- T

## list all file in input path (and sub folders) justifying pattern definition
files <- list.files(inpath, recursive = T, pattern = "mez_ca05_nai30_0050.dat$")
files <- grep("CEMU_2009", files, value = T)
print("HALLO")
print(files)
## read all files into a list
ldat <- lapply(1:length(files), function(i) {
  read.table(paste(inpath,files[i],sep="/"),header = T, sep = ",", fill = T)
})

## remove data from data list if no plot id is available
ldat <- lapply(seq(ldat), function(i) subset(ldat[[i]], ldat[[i]]$PlotId != ""))

## set data values used for visualization
datetime <- lapply(seq(ldat), function(i) ldat[[i]]$Datetime)
plotID <- lapply(seq(ldat), function(i) ldat[[i]]$PlotId)
plotval <- lapply(seq(ldat), function(i) ldat[[i]]$Ta_200)

## combine data list entries
datetime <- unlist(datetime)
plotID <- unlist(plotID)
plotID <- substr(plotID, 1, 8)
plotval <- unlist(plotval)
plotval <- ifelse(plotval > 50, NA, ifelse(plotval < -20, NA, plotval))

plotname <- paste("overview", "Ta_200", format(Sys.time(), "%Y-%m-%d_%H%M%S"),
                  "wide.png", sep = "_")

## call function
png(paste(inpath, plotname, sep = "/"), width = 1000, height = 3000)
VStationData(
  plotval = plotval,         # x = t
  datetime = datetime,       # date = datetime
  cond = plotID,          # cond = plot
  fun = mean,                # fun = mean
  arrange = "long",          # arrange = "long"
  main = "Temperature (AEG)",      # main = "Temperature"
  colour = colList$colPrec  # colour = colList$colPrec
  )
dev.off()
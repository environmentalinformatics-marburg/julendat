# only VIP-stations

rm(list=ls())
setwd("/media/memory01/ei_data_exploratories/processing/plots/revised_reloaded_0400plus/level0420_annual/")

subfolders <- c("AEG","HEG","SEG")
datlist <- lapply(seq(subfolders), function(i) {
  list.files(subfolders[i], recursive=T, pattern="(E|A)EMU", full.names=T)
})
# str(datlist)
dat <- lapply(seq(datlist), function(i) {
  tmp <- do.call("rbind", lapply(seq(datlist[[i]]), function(j) {
    tmp2 <- read.csv(datlist[[i]][j])
  }))
  return(tmp)
})
# str(dat)

regions <- c("AEG", "HEG", "SEG")
lapply(seq(dat), function(i) {
  write.table(dat[[i]], file=paste("/media/memory01/ei_data_exploratories/processing/plots/revised_reloaded_0400plus/",
  regions[i], "_420_VIP.csv", sep = ""), na="NA", sep=";", row.names=F)
})

#################################################################################

# CEMU-stations

rm(list=ls())
setwd("/media/memory01/ei_data_exploratories/processing/plots/revised_reloaded_0400plus/level0420_annual/")

subfolders <- c("AEG", "AEW", "HEG", "HEW", "SEG", "SEW")
datlist <- lapply(seq(subfolders), function(i) {
  list.files(subfolders[i], recursive=T, pattern="CEMU", full.names=T)
})
# str(datlist)

dat <- lapply(seq(datlist), function(i) {
  tmp <- do.call("rbind", lapply(seq(datlist[[i]]), function(j) {
    tmp2 <- read.csv(datlist[[i]][j])
    tmp3 <- tmp2[,c(1:134)]
  }))
  return(tmp)
})
# str(dat)

regions <- c("AEG", "AEW", "HEG", "HEW", "SEG", "SEW")
lapply(seq(dat), function(i) {
  write.table(dat[[i]], file=paste("/media/memory01/ei_data_exploratories/processing/plots/revised_reloaded_0400plus/",
  regions[i], "_420_CEMU.csv", sep = ""), na="NA", sep=";", row.names=F)
})



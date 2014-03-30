#setwd("/media/jsonne/Volume/bexis/temp")
#filepath.data <- "/media/jsonne/Volume/bexis/temp/420"

#subfolders <- list.dirs(filepath.data, recursive=F)
#datlist <- lapply(seq(subfolders), function(a) {
  #list.files(subfolders[a], recursive=T, full.names=T)
#})
# str(datlist)

# use lapply to read in all files and bind them together into one data frame
#dat <- lapply(seq(datlist), function(i) {
  #tmp <- do.call("rbind", lapply(seq(datlist[[i]]), function(j) {
    #tmp2 <- read.csv(datlist[[i]][j])
    #tmp3 <- tmp2[,c(1:135)]
    #return(tmp3)
  #}))
  #return(tmp)
#})
# str(dat)

#regions <- c("AEG", "AEW", "HEG", "HEW", "SEG", "SEW")
#lapply(seq(dat), function(i) {
  #write.table(dat[[i]], file=paste(regions[i], "_420_all.csv", sep = ""), sep=";", na="NA", row.names=F)
#})

#################################################################################

# the same for ALL parameters (only VIP-stations)

rm(list=ls())
setwd("/media/permanent/active/bexis/processing/revised_reloaded_level0420")
filepath.data <- "/media/permanent/active/bexis/processing/revised_reloaded_level0420"

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
  write.table(dat[[i]], file=paste("/media/permanent/active/bexis/processing/revised_reloaded_level0420", regions[i], "_420_VIP.csv", sep = ""), na="NA", sep=";", row.names=F)
})

#################################################################################

# the same for CEMU-stations only

rm(list=ls())
setwd("/media/permanent/active/bexis/processing/revised_reloaded_level0420")
filepath.data <- "/media/permanent/active/bexis/processing/revised_reloaded_level0420"

subfolders <- list.dirs(filepath.data, recursive=F)
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
  write.table(dat[[i]], file=paste("/media/permanent/active/bexis/processing/revised_reloaded_level0420/", regions[i], "_420_CEMU.csv", sep = ""), na="NA", sep=";", row.names=F)
})



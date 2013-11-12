setwd("/media/permanent/development/test/julendat/processing/plots")

files <- list.files("/media/permanent/development/test/julendat/processing/plots", pattern=glob2rx("*0050.dat"), recursive=TRUE, full.names=TRUE)

test <- do.call("rbind", lapply(seq(files), function(i){
  actfile <- read.csv(files[i])
  act.test.min <- min(actfile$Ta_200, na.rm=TRUE)
  act.test.max <- max(actfile$Ta_200, na.rm=TRUE)
  return(data.frame(file=files[i], min=act.test.min, max=act.test.max))
}))

thv.min <- -40.0
thv.max <- 40.0
critical <- test[test$min<thv.min|test$max>thv.max,]
write.csv(critical, file="critical_0050.csv", row.names=FALSE)
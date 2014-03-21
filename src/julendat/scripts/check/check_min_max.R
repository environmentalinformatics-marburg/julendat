setwd("/media/data/ei_data_exploratories/download/aggregated")

files <- list.files("/media/data/ei_data_exploratories/download/aggregated/AEG/_420_Y/", pattern=glob2rx("*420*.csv"), recursive=TRUE, full.names=TRUE)

test <- do.call("rbind", lapply(seq(files), function(i){
  actfile <- read.csv(files[i])
  #print(actfile)
  act.test.min.ta <- min(actfile$Ta_200, na.rm=TRUE)
  act.test.max.ta <- max(actfile$Ta_200, na.rm=TRUE)
  
  act.test.min.rh <- min(actfile$rH_200, na.rm=TRUE)
  act.test.max.rh <- max(actfile$rH_200, na.rm=TRUE)
  
  act.test.min.sm10 <- min(actfile$SM_10, na.rm=TRUE)
  act.test.max.sm10 <- max(actfile$SM_10, na.rm=TRUE)
  act.test.min.sm15 <- min(actfile$SM_15, na.rm=TRUE)
  act.test.max.sm15 <- max(actfile$SM_15, na.rm=TRUE)
  act.test.min.sm20 <- min(actfile$SM_20, na.rm=TRUE)
  act.test.max.sm20 <- max(actfile$SM_20, na.rm=TRUE)
  act.test.min.sm30 <- min(actfile$SM_30, na.rm=TRUE)
  act.test.max.sm30 <- max(actfile$SM_30, na.rm=TRUE)
  act.test.min.sm40 <- min(actfile$SM_40, na.rm=TRUE)
  act.test.max.sm40 <- max(actfile$SM_40, na.rm=TRUE)
  act.test.min.sm50 <- min(actfile$SM_50, na.rm=TRUE)
  act.test.max.sm50 <- max(actfile$SM_50, na.rm=TRUE)
  
  return(data.frame(file=files[i], 
                    min.ta=act.test.min.ta, 
                    max.ta=act.test.max.ta, 
                    
                    min.rh=act.test.min.rh, 
                    max.rh=act.test.max.rh,
                    
                    min.sm10=act.test.min.sm10, 
                    max.sm10=act.test.max.sm10,
                    min.sm15=act.test.min.sm15, 
                    max.sm15=act.test.max.sm15,
                    min.sm20=act.test.min.sm20, 
                    max.sm20=act.test.max.sm20,
                    min.sm30=act.test.min.sm30, 
                    max.sm30=act.test.max.sm30,
                    min.sm40=act.test.min.sm40, 
                    max.sm40=act.test.max.sm40,
                    min.sm50=act.test.min.sm50, 
                    max.sm50=act.test.max.sm50
                    ))
}))

thv.min.ta <- -40.0
thv.max.ta <- 40.0

thv.min.rh <- 0.0
thv.max.rh <- 101.0

thv.min.sm10 <- 0.0
thv.max.sm10 <- 101.0
thv.min.sm15 <- 0.0
thv.max.sm15 <- 101.0
thv.min.sm20 <- 0.0
thv.max.sm20 <- 101.0
thv.min.sm30 <- 0.0
thv.max.sm30 <- 101.0
thv.min.sm40 <- 0.0
thv.max.sm40 <- 101.0
thv.min.sm50 <- 0.0
thv.max.sm50 <- 101.0

critical <- test[test$min.ta<thv.min.ta|
                   test$max.ta>thv.max.ta|
                   
                   test$min.rh<thv.min.rh|
                   test$max.rh>thv.max.rh|
                   
                   test$min.sm10<thv.min.sm10|
                   test$max.sm10>thv.max.sm10|
                   test$min.sm15<thv.min.sm15|
                   test$max.sm15>thv.max.sm15|
                   test$min.sm20<thv.min.sm20|
                   test$max.sm20>thv.max.sm20|
                   test$min.sm30<thv.min.sm30|
                   test$max.sm30>thv.max.sm30|
                   test$min.sm40<thv.min.sm40|
                   test$max.sm40>thv.max.sm40|
                   test$min.sm50<thv.min.sm50|
                   test$max.sm50>thv.max.sm50,]

write.csv(critical, file="critical_0420.csv", row.names=FALSE)
write.csv(test, file="all_420.csv", row.names=FALSE)


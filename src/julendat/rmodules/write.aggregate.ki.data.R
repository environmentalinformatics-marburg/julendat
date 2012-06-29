write.aggregate.ki.data <- function(inputfilepath, 
                                    outputfilepath,
                                    level = "1h",
                                    ...) 
{
  
  source("aggregate.ki.data.R")
  
  out <- aggregate.ki.data(inputfilepath,
                           level = level,
                           ...)
  
  write.table(out, outputfilepath, sep = ",", col.names = T, row.names = F)
  
}

#write.aggregate.ki.data("/media/permanent/development/test/julendat/processing/plots/ki/0000cof3/ca05_cti05_0050/ki_0000cof3_000rug_201111010000_201111302355_eat_ca05_cti05_0050.dat",
#                       "/media/permanent/development/test/julendat/processing/plots/ki/0000cof3/ca05_cti05_0050/test.dat",
#                         level = "1h")
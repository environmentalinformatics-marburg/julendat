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

# write.aggregate.ki.data("C:/tappelhans/uni/marburg/kili/testing/kili_data/ki_0000cof3_000wxt_201112010000_201112312355_eat_ca05_cti05_0005.dat",
#                         "c:/tappelhans/uni/marburg/kili/testing/kili_data/test1.dat",
#                         level = "1h")
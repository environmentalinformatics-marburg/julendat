print.ki.strip <- function(inputpath,
                             outputpath = inputpath,
                             logger = "rug",
                             prm = "Ta_200",                       
                             fun = mean,
                             arrange = "long",
                             year,
                             range = c(-10, 50),
                             pattern,
                             colour = colList$colTa,
                             ...) {
  
  source("ki.strip.R")
  
  plotname <- paste(Sys.Date(), "Overview", prm, logger, year, arrange, sep = "_")
  plotname <- paste(plotname, ".png", sep = "")
  
  png(paste(outputpath, plotname, sep = "/"), 
      width = ifelse(arrange == "wide", 1024*6, 768*6), 
      height = ifelse(arrange == "wide", 768*6, 1024*6),
      res = 600)
  ki.strip(inputpath = inputpath,
             prm = prm,
             logger = logger,
             arrange = arrange,
             fun = fun,
             year = year,
             range = range,
             pattern = pattern,
             colour = colour)
  dev.off()
}

# system.time(print.ki.strip("/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/",
#                  logger = "rug",
#                  prm = "Ta_200",
#                  fun = mean,
#                  arrange = "long",
#                  #range = c(0, 40),
#                  pattern  = "*fah01_0200.dat",
#                  colour = VColList$Ta_200,
#                  year = "2012"))

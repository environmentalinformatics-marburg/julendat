print.wxt.ki.strip <- function(inputpath,
                               outputfilepath,
                               plotid = "cof3",
                               year,
                               ptrn = "*fah01_0200.dat",
                               ...) {
  
  source("wxt.ki.strip.R")
  
  plotname <- paste(Sys.Date(), "Overview", "wxt", plotid, year, sep = "_")
  plotname <- paste(plotname, ".png", sep = "")
  
  png(paste(outputfilepath, plotname, sep = "/"), 
      width = 1200*6, 
      height = 1024*6,
      res = 300)
  wxt.ki.strip(inputpath = inputpath,
               outputfilepath = outputfilepath,
               plotid = plotid,
               year = year,
               ptrn = ptrn)
  dev.off()
}

# system.time(print.wxt.ki.strip("/home/ede/software/testing/julendat/processing/plots/ki/0000cof3/",
#                  outputfilepath = "/home/ede/software/testing/julendat/processing/vis/",
#                  plotid = "cof3",
#                  ptrn = "*fah01_0200.dat",
#                  year = "2012"))

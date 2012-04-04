print.kili.strip <- function(inputpath,
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
  
  source("c:/tappelhans/uni/software/development/r_kili/src/kili.strip/kili.strip.R")
  
  plotname <- paste("overview", prm, logger, year, arrange, Sys.Date(), sep = "_")
  plotname <- paste(plotname, ".png", sep = "")
  
  png(paste(outputpath, plotname, sep = "/"), 
      width = ifelse(arrange == "wide", 1024*6, 768*6), 
      height = ifelse(arrange == "wide", 768*6, 1024*6),
      res = 300)
  kili.strip(inputpath = inputpath,
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

print.kili.strip("f:/kili_data/plots/ki",
                 logger = "wxt",
                 prm = "WV",
                 fun = mean,
                 arrange = "long",
                 range = c(0, 5),
                 pattern  = "*cti05_0005.dat",
                 colour = colList$colWV,
                 year = "2011")

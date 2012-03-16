print.kili.strip <- function(inputpath,
                             outputpath = inputpath,
                             logger = "rug",
                             prm,                       
                             fun = mean,
                             arrange = c("long", "wide"),
                             year,
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
             year = year,
             colour = colour)
  dev.off()
}

# print.kili.strip("f:/kili_data/testing/overview/ki",
#                  logger = "wxt",
#                  prm = "p_200",
#                  fun = mean,
#                  arrange = "long",
#                  colour = colList$colTa,
#                  year = "2011")
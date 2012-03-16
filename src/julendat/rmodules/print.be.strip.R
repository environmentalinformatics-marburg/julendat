print.be.strip <- function(inputpath,
                           outputpath = inputpath,
                           logger = "CEMU",
                           prm,                       
                           fun = mean,
                           arrange = c("long", "wide"),
                           year,
                           colour = colList$colTa,
                           ...) {
  
  source("c:/tappelhans/uni/software/development/r_be/src/be.strip/be.strip.R")
  
  plotname <- paste("overview", prm, logger, year, arrange, Sys.Date(), sep = "_")
  plotname <- paste(plotname, ".png", sep = "")
  
  png(paste(outputpath, plotname, sep = "/"), 
      width = ifelse(arrange == "wide", 1024*6, 768*6), 
      height = ifelse(arrange == "wide", 768*6, 1024*6),
      res = 300)
  be.strip(inputpath = inputpath,
           prm = prm,
           logger = logger,
           arrange = arrange,
           year = year,
           colour = colour)
  dev.off()
}

# print.be.strip("c:/tappelhans/uni/marburg/kili/testing/be_data",
#                logger = "CEMU",
#                prm = "Ta_200",
#                fun = mean,
#                arrange = "long",
#                colour = colList$colTa,
#                year = "2011")

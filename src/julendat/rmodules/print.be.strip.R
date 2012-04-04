print.be.strip <- function(inputpath,
                           outputpath = inputpath,
                           logger = "CEMU",
                           prm = "Ta_200",                       
                           fun = mean,
                           arrange = "long",
                           year,
                           range = c(-10, 50),
                           pattern,
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
           fun = fun,
           year = year,
           range = range,
           pattern = pattern,
           colour = colour)
  dev.off()
}

print.be.strip("c:/tappelhans/uni/marburg/kili/testing/be_data",
               logger = "CEMU",
               prm = "Ta_200",
               fun = mean,
               arrange = "long",
               range = c(-30, 40),
               pattern = "*HE*0005.dat",
               colour = colList$colPrec,
               year = "2009")

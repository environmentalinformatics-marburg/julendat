print.ki.strip <- function(inputfilepath,
                             outputpath,
                             prm = "Ta_200",                       
                             fun = mean,
                             arrange = "long",
                             year,
                             range = c(-10, 50),
                             pattern,
                             colour = colList$colTa,
			                 resolution = 400,
			                 project_id = "ki",
                             ...) 
{
  
			  source("ki.strip.R")
			  
			  plotname <- paste(Sys.Date(), "Overview", prm, year, arrange, sep = "_")
			  plotname <- paste(plotname, ".png", sep = "")
			  
			  png(paste(outputpath, plotname, sep = "/"), 
			      width = ifelse(arrange == "wide", 1024*8, 768*8), 
			      height = ifelse(arrange == "wide", 768*8, 1024*8),
			      res = resolution)
			  ki.strip(inputfilepath = inputfilepath,
			             prm = prm,
			             arrange = arrange,
			             fun = fun,
			             year = year,
			             range = range,
			             pattern = pattern,
			             colour = colour,
			             project_id = project_id,)
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

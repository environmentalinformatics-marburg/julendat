rm(list=ls())

library(XML)

# Set path environment and read files
setwd("/media/permanent/active/bexis/webverdis/test")
files <- list.files(path = ".",
                    pattern = "xml",
                    full.names = TRUE, recursive = TRUE)

x <- files[1]
cds <- lapply(files, function(x){
  act.file <- x
  act.data <- xmlParse(act.file)
  act.data <- xmlToList(act.data)
  str(act.data)
  
  as.list(act.data[["stationname"]])
  str(act.data)
  temps <- act.data[["stationname"]]
  temps <- temps[names(temps) == "v"]
  
  temps <- temps[sapply(temps$v, function(x) any(unlist(x) == "text"))]
  temps <- unlist(temps[[1]][sapply(temps, names) == "date"])
  xmlGetAttr
  })


bexis <- read.table("14526.txt", header = TRUE, sep = "\t")
str(bexis)
unique(bexis$Station)
summary(bexis$lat)
sort(unique(bexis$lon))

update <- read.table("stations.txt", header = TRUE, sep = ",")
unique(update$Station)


plot(sort(unique(bexis$lat)))
48.15, 48.73
50.7500, 51.70
52.65, 53.40

plot(sort(unique(bexis$lon)))
8.90, 9.90 
9.85, 11.10
13.20, 14.40
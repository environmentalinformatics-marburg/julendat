### Environmental settings


# Clear workspace
rm(list=ls(all=TRUE))

# Set working directory
setwd("C:/Users/detsch/Documents/r_mulreg")

# Required libraries for parallelization
library(foreach)
library(doSNOW)
library(parallel)

# Required functions
source("as.ki.data.r")
source("gfImputeMissingValue.r")



### Paths, files and objects for input and output


# Data directory
path.data <- "data/"

# Available data sets
files <- list.files(paste(path.data, "ki", sep=""), full.names=TRUE, recursive=TRUE, 
                    pattern="rug_201112010000_201112312355_eat_ca05_cti05_0050.dat$")

# Select dependent station at random
plot.art <- sample(seq(files), 1)

# Dependent data set
files.dep <- files[plot.art]
# Independent data sets
files.indep <- files[-plot.art]

# Plot coordinates
plot.coords <- read.csv("stations_master_20121103.csv", header=TRUE)
plot.coords <- plot.coords[,c("PlotID", "Lon", "Lat")]



### Parallelization


# Number of cores
n.cores <- detectCores() 

# Initialize and register SNOW parallel backend
clstr <- makeCluster(n.cores, type="SOCK")
registerDoSNOW(clstr)

# Export function 'as.kili.data' to cluster
temp <- clusterEvalQ(clstr, c(source("as.ki.data.r")))



### Data import


# Import dependent data set
ki.data.dep <- as.ki.data(files.dep)

# Paralellized import of independent data sets
ki.data.indep <- foreach(i = seq(files.indep), .packages = "reshape") %dopar% {
  as.ki.data(files.indep[i])
}

# Stop cluster
stopCluster(clstr)



### Imputation of missing values


# Output list
data.imputation <- list()

# Missing value(s) to be imputed
pos.na <- ki.data.dep@Valid$NAIndex

# Impute missing value(s)
if (length(pos.na) > 0) {
  data.imputation.2 <- lapply(seq(pos.na), function(i) {
    gfImputeMissingValue(data.dep = ki.data.dep, 
                       data.indep = ki.data.indep,
                       na.limit = 0.05, 
                       pos.na = pos.na[i], 
                       data.coords = plot.coords, 
                       n.plot = 10, 
                       prm.dep = "rH_200", 
                       prm.indep = "Ta_200")
  })
}

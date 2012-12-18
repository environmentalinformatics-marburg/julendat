gfrun <- function(files.dep,
                  files.indep,
                  na.limit = na.limit,
                  data.coords = data.coords,
                  n.plot = n.plot,
                  prm.dep = prm.dep, 
                  prm.indep = prm.indep) {
  # Clear workspace
  rm(list=ls(all=TRUE))
  
  # Required libraries for parallelization
  library(foreach)
  
  library(doSNOW)
  library(parallel)
  
  # Required functions
  source("as.ki.data.R")
  source("gfImputeMissingValue.R")
  
  ### Parallelization
  # Number of cores
  n.cores <- detectCores() 
  
  # Initialize and register SNOW parallel backend
  clstr <- makeCluster(n.cores, type="SOCK")
  registerDoSNOW(clstr)
  
  # Export function 'as.kili.data' to cluster
  temp <- clusterEvalQ(clstr, c(source("as.ki.data.R")))
  
  
  
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
  
  
  # Missing value(s) to be imputed
  pos.na <- ki.data.dep@Valid$NAIndex
  
  # Impute missing value(s)
  if (length(pos.na) > 0) {
    data.imputation <- lapply(seq(pos.na), function(i) {
      gfImputeMissingValue(data.dep = ki.data.dep, 
                           data.indep = ki.data.indep,
                           na.limit = na.limit, 
                           pos.na = pos.na[i], 
                           data.coords = data.coords, 
                           n.plot = n.plot, 
                           prm.dep = prm.dep, 
                           prm.indep = prm.indep)
    })
  }
}

gfrun(files.dep = "/home/ede/software/testing/julendat/processing/plots/ki/0000flm1/ca05_fah01_0050/ki_0000flm1_000rug_201109010000_201109302355_eat_ca05_fah01_0050.dat",
      files.indep = c("/home/ede/software/testing/julendat/processing/plots/ki/0000fod1/ca05_fah01_0050/ki_0000fod1_000rug_201109010000_201109302355_eat_ca05_fah01_0050.dat",
                      "/home/ede/software/testing/julendat/processing/plots/ki/0000mai2/ca05_fah01_0050/ki_0000mai2_000rug_201109010000_201109302355_eat_ca05_fah01_0050.dat"),
      na.limit = 0.1,
      data.coords = plot.coords,
      n.plot = 10,
      prm.dep = "Ta_200", 
      prm.indep = NULL)
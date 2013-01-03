gfRun <- function(files.dep,
                  files.indep,
                  filepath.coords, 
                  quality.levels, 
                  na.limit,
                  data.coords,
                  n.plot,
                  prm.dep, 
                  prm.indep) {

  # Required libraries for parallelization
  library(foreach)
  library(doSNOW)
  library(parallel)
  
  # Required functions
  source("as.ki.data.R")
  source("gfRejectLowQuality.R")
  source("gfImputeMissingValue.R")
  source("gfOutputData.R")
  
#   ### Parallelization
#   # Number of cores
#   n.cores <- detectCores() 
#   
#   # Initialize and register SNOW parallel backend
#   clstr <- makeCluster(n.cores, type="SOCK")
#   registerDoSNOW(clstr)
#   
#   # Export function 'as.kili.data' to cluster
#   temp <- clusterEvalQ(clstr, c(source("as.ki.data.R")))
#   
#   
  
  ### Data import
  
  
  # Import plot coordinates
  data.coords <- read.csv(filepath.coords, header=TRUE)
  data.coords <- data.coords[,c("PlotID", "Lon", "Lat")]
  
  
  # Import dependent data set
  ki.data.dep <- as.ki.data(files.dep)

  # Paralellized import of independent data sets
#   clusterExport(clstr, "files.indep")
#   ki.data.indep <- foreach(i = seq(files.indep), .packages = "reshape") %dopar% {
#     as.ki.data(files.indep[i])
#   }
  
  ki.data.indep <- lapply(seq(files.indep), function(i) {
    as.ki.data(files.indep[i])
  })
  
  # Stop cluster
#  stopCluster(clstr)
  
  
  ### Rejection of records with bad quality flags
  
  
  # Dependent plot

  for (i in seq(prm.dep)) {
    ki.data.dep <- gfRejectLowQuality(data = ki.data.dep, 
                                      prm.dep = prm.dep[i], 
                                      quality.levels = quality.levels)

    
    # Independent plots
    ki.data.indep <- gfRejectLowQuality(data = ki.data.indep, 
                                        prm.dep = prm.dep[i], 
                                        quality.levels = quality.levels)
    
    
    
    ### Imputation of missing values
    
    
    # Output list
    model.output <- list()
    
    # Missing value(s) to be imputed
    pos.na <- which(is.na(ki.data.dep@Parameter[[prm.dep[i]]]))
    
    # Impute missing value(s)
    if (length(pos.na) > 0) {
      model.output <- lapply(seq(pos.na), function(j) {
        print(paste(prm.dep[i], prm.indep[i], pos.na[j], sep = ", "))
        gfImputeMissingValue(data.dep = ki.data.dep, 
                             data.indep = ki.data.indep,
                             na.limit = na.limit, 
                             pos.na = pos.na[j], 
                             data.coords = data.coords, 
                             n.plot = n.plot, 
                             prm.dep = prm.dep[i], 
                             prm.indep = prm.indep[i])
      })
    }
    
    # Replace NA values by predicted values
    ki.data.dep@Parameter[[prm.dep[i]]][pos.na] <- unlist(lapply(seq(model.output), function(k) {
      ki.data.dep@Parameter[[prm.dep[i]]][pos.na[k]] <- model.output[[k]][[4]]
    }))
  }
  
  
  
  ### Gap-filled output data frame
  
  
  data.output <- gfOutputData(data.dep = ki.data.dep)
  
  
  # Return output
  return(list(model.output, data.output))
}

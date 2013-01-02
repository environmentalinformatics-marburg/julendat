gfWrite <- function(files.dep, 
                    files.indep, 
                    filepath.output, 
                    filepath.coords, 
                    quality.levels, 
                    na.limit, 
                    n.plot,
                    prm.dep, 
                    prm.indep,  
                    ...) {
  
  # Load function 'gfRun'
  source("gfRun.R")
  
  # Perform imputation
  imputation.data <- gfRun(files.dep = files.dep,
                           files.indep = files.indep,
                           filepath.coords = filepath.coords, 
                           quality.levels = quality.levels,
                           na.limit = na.limit,
                           n.plot = n.plot,
                           prm.dep = prm.dep, 
                           prm.indep = prm.indep)
  
  # Write output table
  write.table(imputation.data[[2]], 
              filepath.output, 
              sep = ",", row.names = FALSE, col.names = TRUE)

}
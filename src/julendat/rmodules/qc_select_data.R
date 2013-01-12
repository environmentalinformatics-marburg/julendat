qc_select_data <- function(datalist,para_list) {

################################################################################  
##  This functions selects and extracts parameter vectors. This can be done for
##  several datasets.
##  
################################################################################  

datlist <- lapply(1:length(datalist), function(i) {

## select dataset create data.frame
  
    data <- datalist[[i]]
    dat <- data.frame(data[[para_list[[1]]]])
    dat[[para_list[[1]]]] <- dat[,1]
    
   
## select and extract parameter vectors
    
    for (j in 1:length(para_list)) {
    dat[[para_list[[j]]]] <- data[[para_list[[j]]]]
    }
    
## delete first row
    
  if (length(para_list) > 1) dat <- dat[,-1] else dat

################################################################################    
  })

################################################################################
}

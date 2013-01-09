qc_datetime <- function(datalist,pos) {

################################################################################  
##  This function extracts a column from each dataset in a list  
##  
##  datalist = input list of datasets
##  pos = number of the column to be extracted
################################################################################  
  
	datlist <- lapply(1:length(datalist), function(i) {
		
		data <- datalist[[i]]
		dat <- data[[pos]]
	})
	
}

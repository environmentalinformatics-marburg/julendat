qc_readin <- function(filepath) {
  
################################################################################
##  This function reads in a variable number of datasets
##
##  filepath = list of filepaths (character)
################################################################################  
datalist <- lapply(1:length(filepath), function(i) {
		read.table(filepath[[i]], header = T, fill = T,
		           sep = ",", stringsAsFactors = F,
				   dec = ".",
				   na.strings = c("nan","NAN","na","NA"))
								}							
								)								
################################################################################
}

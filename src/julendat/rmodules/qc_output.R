qc_output <- function(datalist,output_filepath, plevel) {

################################################################################  
##  This function writes out tables from a list of datasets.
##  
##  datalist = list of datasets (list)
##  ouput_filepath = list of output filepaths (character)
##  
##
################################################################################
  
	for (i in 1:length(datalist)) {
      datalist[[i]]$Processlevel <- rep(sprintf("%04.f", plevel), 
                      length.out =  datalist[[i]]$Datetime)
			write.table(datalist[[i]],output_filepath[[i]],
      col.names = T, row.names = F,	sep = ",")
	}
  
################################################################################
}

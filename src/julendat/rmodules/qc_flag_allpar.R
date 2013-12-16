qc_flag_allpar <- function(data,parameter,limits,qfvalues,qfpos,flag_col) {

################################################################################
##  This function puts a loop around the qc_maxmin functions and checks all
##  parameter of the dataset.
##	
################################################################################  
##  source functions from working directory ####################################
  
source("qc_maxmin.R")


################################################################################
  
	for (i in 1:length(parameter)) {
		data[[flag_col]] <- 
				qc_maxmin(data,parameter[[i]], limits[[i,2]], limits[[i,1]], 
				qfvalues[[1]], qfvalues[[2]], qfpos[[i]], flag_col)
			
	}

	return(data)
	
}


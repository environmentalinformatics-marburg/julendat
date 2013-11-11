qc_output_limits <- function(datlist, output_tab, limit_output, check) {

################################################################################
##  This function writes out tables of limits, calculated from qc_limits.
##  
##  datlist = list of datasets
##  output_tab = table with maximum and minimum limits (all given parameters)
##  limit_output = output filepath (without filename)
##  check = filename (depends on check)  
##  
################################################################################
## names #######################################################################
list_names <- list(names(datlist[[1]]))
list_names <- list_names[[1]]

################################################################################
## format output_tab ###########################################################
## -Inf to NA
	output_tab[[1]] <- ifelse(output_tab[[1]] == -Inf | output_tab[[1]] == Inf,
														NA, output_tab[[1]])
	output_tab[[2]] <- ifelse(output_tab[[2]] == -Inf | output_tab[[2]] == Inf,
														NA, output_tab[[2]])

################################################################################

## output ##
  if (is.null(limit_output)) NULL else
    write.table(output_tab, file = paste(limit_output, check , sep = "/"), 
                col.names = F, row.names = list_names, sep = ",")

################################################################################
}

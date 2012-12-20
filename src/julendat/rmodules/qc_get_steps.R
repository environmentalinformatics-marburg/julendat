qc_get_steps <- function(input,para) {

################################################################################
##  This function returns differences
##  additional:
##  additional rows are added at column top to remain the same column lengts
##  before it checks if there is data in every timestep to decide how much
##  rows have to be added
##  
##  input = input dataset (dataframe)
##  para = name of parameter to process
##  
################################################################################  
  
	cases <- which(complete.cases(input[[para]]))
	
  if(min(diff(cases))<2) 
		difference<-c(NaN,diff(input[[para]], lag = 1)) else
			difference<-c(NaN,NaN,diff(input[[para]], lag = 2))
	
	return(abs(difference))
	
}



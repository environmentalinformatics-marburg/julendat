qc_maxmin <- function (data,para,max,min,flagp,flagf,digit,flag_col) {
	
  
################################################################################
##  This program checks a vector against given minimum and maximum limits and
##  updates a qualityflag.
##  
##  parameters are as follows:
##  data = input dataset (dataframe)
##  para = name of parameter to be checked (character)
##  max = maximum limit (numeric)
##  min = minimum limit (numeric)
##  flagp = flag: check passed (numeric)
##  flagf = flag: check failed (numeric)
##  digit = start position for the flag (depends on parameter, numeric)
##  flag_col = name of qualityflag column  
##  
################################################################################  
## test ########################################################################
## select columns (parameter, flag)
	dat <- data[[para]]
	qual <- as.character(data[[flag_col]])
	


## devide existing quality flag  
  
  qualleft <- substr(qual, 1, (digit - 1))
	qualact <- substr(qual, digit, (digit + 2))
	qualright <- substr(qual, (digit + 3), length(qual))


## check and flag  
  
  

qualact <- ifelse(qualact!="", ifelse(!is.na(dat), ifelse(dat > max |
            dat < min, as.numeric(qualact) + as.numeric(flagf),
            as.numeric(qualact)+as.numeric(flagp)),qualact),qualact)
	
## format: complete flag with additional "0" or "00"
  
	qualadd <- ifelse(!is.na(dat),ifelse(qualact!="",ifelse(as.numeric(qualact) < 100, ifelse(as.numeric(qualact) < 10, "00", "0")
										,""),""),"")

## assemble qualityflag (parameter)
  
	qualend <- (paste(qualadd, as.character(qualact), sep=""))
  
## flag "NAs"	
  
	#qualend <- ifelse (is.na(dat),"nan",qualend)

## assemble whole qualityflag  
	
	qual <- paste(qualleft,qualend,qualright, sep = "")
	
#################################################################################	

}

#################################################################################

qc_limit <- function(datlist, percentil,datetime) {

################################################################################
##  This function creates limits for a following limit check.
##  It calculates the daily minima and maxima, and sets a limitvalue at a
##  given percentil limit. 
##
################################################################################
## combine datetime and parameter ##############################################

datlist <- lapply(1:length(datlist), function(i) {
		
	datlist[[i]]$Datetime <- datetime[[i]]
		
	datlist[[i]]
		
	})

################################################################################
## create daily maxima #########################################################

datlist_max <- lapply(1:length(datlist), function(i) {
		
		dat <- datlist[[i]]
		date <- as.character(dat[["Datetime"]])
		index <- list(substr(date, 9, 10))
		
		aggregate(dat, by = index, FUN = max, na.rm = T)
		})

################################################################################
## create daily minima #########################################################
	
datlist_min <- lapply(1:length(datlist), function(i) {
		
		dat <- datlist[[i]]
		date <- as.character(dat[["Datetime"]])
		index <- list(substr(date, 9, 10))
		
    aggregate(dat, by = index, FUN = min, na.rm = T)
		})

################################################################################
## set limitvalues #############################################################
## maxima 
	
	datmax <- do.call("rbind", datlist_max)
	
	outputmax <- lapply(1:length(datmax), function(i) {

	data <- if(is.numeric(datmax[1,i])) 
		quantile(datmax[i], probs = c(1-percentil[[1]]/100), na.rm = T, names = F)	
		}
			)

## minima 	

	datmin <- do.call("rbind", datlist_min)
	
	outputmin <- lapply(1:length(datmin), function(i) {

	data <- if(is.numeric(datmin[1,i])) 
		quantile(datmin[i], probs = c(percentil[[1]]/100), na.rm = T, names = F)	
		}
			)
################################################################################
## output ######################################################################
## format NA
	
  output_tab <- data.frame(unlist(outputmin),unlist(outputmax))
	output_tab[[1]] <- ifelse(output_tab[[1]] == -Inf | output_tab[[1]] == Inf,
														NA, output_tab[[1]])
	output_tab[[2]] <- ifelse(output_tab[[2]] == -Inf | output_tab[[2]] == Inf,
														NA, output_tab[[2]])

return(output_tab)

################################################################################
}
################################################################################
################################################################################
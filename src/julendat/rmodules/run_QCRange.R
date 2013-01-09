run_QCRange <- function(input_filepath, parameter, thv_min, thv_max, qfpos,
  											qfvalues, output_filepath = input_filepath,
												flag_col = "Qualityflag", plevel = 0000) {
	

################################################################################
##
##	Meterological Quality Control - Physical limit check (Messbereichscheck)
##
##	This program checks a variable amount of datasets against physical limits
##	and flags the values. 
## 	You can choose and input the maximum and minimum limits, the flag values 
##	and the meteorological parameters you want to check.
##
##	parameters are as follows:
##	input_filepath = a list of dataset filepaths (character,
##										no default)
##	parameter = a list of parameter names, to be tested (character,
##							no default)
## 	thv_min = a list of minimum limits (numeric, no default)
##	thv_max = a list of maximum limits (numeric, no default)
##	qfpos = a list of (start) positions for the flags in the qualityflag 
##					string (numeric, no default)
##	qfvalues = a list of flagvalues to be added to the existing values in the 
##							qualityflag column (numeric, no default)
##	output_filepath = a list of  output filepaths;
##										default = input_filepaths (character)
##	flag_col = name of the qualityflag column (character); 
##							default = "Qualityflag"
##
##
##	The lists of thv_min, thv_max, qfpos and qfvalues have to be 
##	in the same order as the parameter list to ensure a distinct correlation.
##	The dataset has to contain a qualityflag column. This column must be 
##	character string (!) and has to be as long as the amount of parameter multiplied
##	with the number der flagpositions.
##	The quality flag has three positions, the flag values will be added to the
##	existing values.
## 	
##	IMPORTANT: the functions have to be in the working directory
##
################################################################################
##
##  Copyright (C) 2012 Sascha Homburg
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##  Please send any comments, suggestions, criticism, or (for our sake) bug
##  reports to sascha.homburg@gmail.com
##
################################################################################

## source functions from working directory #####################################

source("qc_readin.R")
source("qc_flag_allpar.R")
source("qc_maxmin.R")
source("qc_output.R")

################################################################################
## read in data ################################################################

datalist <- qc_readin(input_filepath)

#print("readin")

################################################################################
## format input parameter ######################################################
# format limits

limits <- data.frame(do.call("cbind", list(thv_min, thv_max)))
#print("limits")
################################################################################
## checking and flagging #######################################################

datlist <- lapply(1:length(datalist), function(j) {
	
	datalist[[j]] <- qc_flag_allpar(datalist[[j]],parameter,limits,qfvalues,qfpos,
																	flag_col)
	
})

################################################################################
## output ######################################################################

qc_output(datlist,output_filepath, plevel)

################################################################################

}

################################################################################
################################################################################
run_QCExtremes <- function(input_filepath, parameter, percentil, qfpos,
												qfvalues, output_filepath = input_filepath, 
                        limit_output = getwd(), pos_date = 1,
												flag_col = "Qualityflag", plevel = 0000) {

################################################################################
##
##	Meterological Quality Control - Range Check
##
##	This program checks a variable amount of datasets against calculated 
##	extremevalues.
##	The program calculates the limits, checks and flags the values.
##	For the limit calculation, daily minima and maxima are calculated. The 
##  program produces sample quantiles corresponding to the given probabilities.
##  These are the limits for the check. The limits are calculated with all input 
##  datasets, then every single dataset is checked.
## 	You can input the flag values and the meteorological parameters you want 
##  to check.
##	The limits are written in a table in the working directory to have the 
##	possibility to check them afterwards.
##
##	parameters are as follows:
##	input_filepath = a list of dataset filepaths (character,
##										no default)
##
##	parameter = a list of parameter names, to be checked (character,
##							no default)
##
##	percentil = the probability for the quantile calculation (%) (numeric,
##								no default)
##
##	qfpos = a list of (start) positions for the flags in the qualityflag 
##					string (numeric, no default)
##
##	qfvalues = a list of flagvalues to be added to the existing values in the 
##							qualityflag column (numeric, no default)
##
##	output_filepath = a list of output filepaths;
##										default = input_filepaths (character)
##
##	limit_output = filepath for the limit output table
##									default = getwd() (character)
##
##	pos_date = the column number of the datetime column, which is necessary to
##							calculate the limits 
##							default = 1 (numeric)
##
##	flag_col = name of the qualityflag column (character); 
##							default = "Qualityflag"
##
##
##	The lists of qfpos and qfvalues have to be in the same order as the 
##	parameter list to to ensure a distinct correlation.
##  The dataset has to contain a qualityflag column. This column must be 
##	character string (!) and has to be as long as the amount of parameter multiplied
##	with the number der flagpositions.
##  The quality flag has three positions, the flag values will be added to the
##	existing values.
##	The format of your date column has to be like this: "YYYY-MM-DD HH:MM:SS".
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
source("qc_select_data.R")
source("qc_datetime.R")
source("qc_limit.R")
source("qc_output_limits.R")
source("qc_flag_allpar.R")
source("qc_maxmin.R")
source("qc_output.R")

################################################################################
## read in data ################################################################

datalist <- qc_readin(input_filepath)

#print("readin")
################################################################################
## limit calculation ###########################################################
## select parameter 

datalist_sel <- qc_select_data(datalist, parameter)

## select datetime

datetime <- qc_datetime(datalist, pos_date)

## get limits 

limits <- qc_limit(datalist_sel,percentil,datetime)



## set output table filename

check <- "limits_extremes.txt"

#print("limits")

## write output table

qc_output_limits(datalist_sel, limits, limit_output, check)

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

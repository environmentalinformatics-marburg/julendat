gfCompleteMonthlyCases <- function(data.dep, 
                                 data.indep,
                                 data.indep.avl,
                                 n.plot = 10,
                                 prm.dep = "Ta_200",
                                 prm.indep = NULL,
                                 ...) {
  
################################################################################
##  
##  This program imports information about plots providing valid records for a
##  known NA position in a monthly data set of a dependent plot. Based upon this
##  information, monthly data sets of a defined number of nearest independent 
##  plots and the dependent plot are being merged and filtered for complete 
##  cases.
##  
##  parameters are as follows:
##  
##  data.dep (ki.data):       Monthly data set of dependent plot.
##  data.indep (list):        List of monthly data sets of independent plots.
##                            Must be composed of ki.data objects.
##  data.indep.avl (logical): Logical vector indicating whether a plot provides 
##                            a valid record for a given NA position.
##  n.plot (numeric):         Number of independent plots for linear regression.
##  prm.dep (character):      Parameter under investigation.
##  prm.indep (character):    Single character object or Character vector with 
##                            independent parameters.
##  ...                       Further arguments to be passed
##
################################################################################
##
##  Copyright (C) 2012 Florian Detsch, Tim Appelhans
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
##  reports to florian.detsch@geo.uni-marburg.de
##
################################################################################

cat("\n",
    "Module   :  gfCompleteMonthlyCases", "\n",
    "Author   :  Florian Detsch <florian.detsch@geo.uni-marburg.de>, Tim Appelhans <tim.appelhans@gmail.com>",
    "Version  :  2012-12-17", "\n",
    "License  :  GNU GPLv3, see http://www.gnu.org/licenses/", "\n",
    "\n")

########## FUNCTION BODY #######################################################

  # Merge lists containing ki.data objects
  data <- append(data.dep, data.indep)

#   # Reject plots due to difference in altitude
#   if (!is.null(height.limit))
#     data.indep.avl[which(abs(data.indep.avl[,2]) > height.limit),1] <- FALSE

  # Convert data.indep.avl to list
  data.indep.avl <- lapply(seq(data.indep.avl), function(i) {
    data.indep.avl[i]
  })
  # Merge logical lists indicating which stations should be considered
  data.avl <- append(list(TRUE), data.indep.avl)

  # Reassign n.plot in case number of valid plots < n.plot
  if (sum(unlist(data.avl)) < n.plot)
    n.plot <- sum(unlist(data.avl))

  # List measured values for each valid station
  data.avl.prm <- lapply(which(unlist(data.avl))[1:(n.plot+1)], function(i) {
      data[[i]]@Parameter[prm.dep]
  })

  # Retrieve dates
  data.avl.date <- list(data[[1]]@Datetime)

  # Measured values of independent parameters
  if (!is.null(prm.indep)) {
    data.prm.indep <- list(data[[1]]@Parameter[prm.indep])
  } else {
    data.prm.indep <- list()
  }

  # Merge dates and measured values
  data.temp <- append(data.avl.date, data.prm.indep)
  data.avl.comp <- append(data.temp, data.avl.prm)

  # Merge time series into data.frame
  data.avl.prm.merge <- do.call("data.frame", data.avl.comp)
  # Select complete cases only
  data.avl.prm.merge.cc <- data.avl.prm.merge[complete.cases(data.avl.prm.merge),]

  # Return data.frame containing complete cases of monthly data sets
  return(list(data.avl.prm.merge, data.avl.prm.merge.cc))
}

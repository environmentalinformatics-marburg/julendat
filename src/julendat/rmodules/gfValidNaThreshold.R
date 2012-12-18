gfValidNaThreshold <- function(data.indep, 
                          na.limit = 0.2, 
                          ...) {
  
  ################################################################################
  ##  
  ##  This program computes the percentage amount of NA values in the independent 
  ##  monthly data sets and rejects those plots that exceed a user-defined limit.
  ##  
  ##  parameters are as follows:
  ##  
  ##  data.indep (list):    List of monthly data sets of independent plots.
  ##                        Must be composed of ki.data objects.
  ##  na.limit (numeric):   Accepted threshold percentage of NA values in monthly 
  ##                        data set of independent plots.
  ##  ...                   Further arguments to be passed
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
      "Module   :  gfValidNaThreshold", "\n",
      "Author   :  Florian Detsch <florian.detsch@geo.uni-marburg.de>, Tim Appelhans <tim.appelhans@gmail.com>",
      "Version  :  2012-12-14", "\n",
      "License  :  GNU GPLv3, see http://www.gnu.org/licenses/", "\n",
      "\n")
  
  ########## FUNCTION BODY #######################################################
  
  
  # Proportion of NA values in monthly data set
  na.ratio <- lapply(seq(data.indep), function(h) {
    1 - data.indep[[h]]@Valid$N / length(data.indep[[h]]@Datetime)
  })
  
  # Reject plots with too high number of NA values
  data.indep <- data.indep[unlist(na.ratio) <= na.limit]
  return(data.indep)
}  
  

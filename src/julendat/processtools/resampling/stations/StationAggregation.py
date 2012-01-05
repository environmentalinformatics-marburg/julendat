"""Aggregate time series station data
Copyright (C) 2011 Thomas Nauss, Tim Appelhans

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Please send any comments, suggestions, criticism, or (for our sake) bug
reports to nausst@googlemail.com
"""

__author__ = "Thomas Nauss <nausst@googlemail.com>, \
              Tim Appelhans <tim.appelhans@gmail.com>"
__version__ = "2010-10-02"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import os
import sys
import shutil
import Tkinter
from julendat.filetools.stations.dkstations.DKStationDataFile import \
    DKStationDataFile
from julendat.metadatatools.stations.StationDataFilePath import \
    StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.guitools.stations.GUIAutoPlotSelection import GUIAutoPlotSelection
from julendat.guitools.stations.GUIManualPlotSelection import \
    GUIManualPlotSelection


class StationAggregation:   
    """Instance for date/time aggregation of time series files.
    """

    def __init__(self, input_filepath, input_variables, r_filepath, \
                 aggregation_mode="auto", \
                 input_start_time = None, input_end_time= None, \
                 input_time_step = None, \
                 output_start_time = None, output_end_time = None, \
                 output_time_step = None, \
                 out_filepath = None):
        """Inits StationAggregation.
        The instance is initialized by the arguments and a configuration file
        defining the type of the input variables to be considered. 
        If the run mode is set to "auto", all implemented aggregation functions
        will be computed. If only a specific aggregation function should be
        computed, the respective function name should be provided as run mode.  
        
        Args:
            aggregation_mode: Aggregation mode (auto, min, mean, max, median, \
                sum, sd, circular_mean)
            input_filepath: Full path and name of the input data file
            input_variables: Variable names  (=columns) to be processed 
            input_start_time: Start time of the input data set
            input_end_time: End time of the input data set
            input_time_step: Time step of the input data set
            output_start_time: Start time of the ouput data set
            output_end_time: End time of the output data set
            output_time_step: Time stept of the output data set
            out_filepath: Full path and name of the output data file
        """
        self.r_filepath = r_filepath
        self.input_variables = input_variables
        self.set_aggregation_mode(aggregation_mode)
        #self.configure(config_file_path, config_file_values)
        self.set_output_time_step(output_time_step)
        if input_start_time == None or input_end_time == None or \
           input_time_step == None:
            self.input_file = StationDataFilePath(filepath=input_filepath)

        self.compute()
        print "...finished."        

    def set_run_mode(self,run_mode):
        """Sets run mode.
        
        Args:
            run_mode: Running mode (default: auto)
        """
        self.run_mode = run_mode

    def get_run_mode(self):
        """Gets run mode.
        
        Returns:
            Running mode
        """
        return self.run_mode

    def set_aggregation_mode(self, aggregation_mode):
        """Sets aggregation mode.
        
        Args:
            aggregation_mode: Aggregation mode (default: auto)
        """
        if aggregation_mode != "auto":
            self.aggregation_mode = aggregation_mode
        else:
            self.aggregation_mode = ('min', 'mean', 'max', 'median', 'sum', \
                             'sd', 'circular_mean')

    def get_aggregation_mode(self):
        """Gets aggregation mode.
        
        Returns:
            Aggregation mode
        """
        return self.aggregation_mode

    def set_output_time_step(self, output_time_step):
        """Sets output time step.
        
        Args:
            output_time_step: Time step of the output data set
        """
        self.output_time_step = output_time_step

    def get_output_time_step(self):
        """Gets output time step.
        
        Returns:
            Output time step
        """
        return self.output_time_step

    def compute(self):
        """Compute aggregation functions as defined by input parameters. 
        """
        r_source = 'source("' + self.r_filepath + os.sep + \
            'TimeSeriesAggregation.R")'
        r_keyword = "compute_time_series_aggregation"
        r_input_filepath = \
           'input_path="' + \
            self.input_file.get_filepath() + '",'
        r_input_start_time = \
            'start_in="' + \
            self.input_file.get_start_datetime_eifc() + '00",'
        r_input_end_time = \
            'end_in="' + \
            self.input_file.get_end_datetime_eifc() + '01",'
        r_input_time_step = \
            'time_step_in=' + \
            str(self.input_file.get_time_step_delta()) + ','
        r_output_time_step = \
            'time_step_out=' + \
            self.get_output_time_step()  + ','

        r_variable = 'c('
        r_function = 'c('
        for aggregation_mode in self.get_aggregation_mode():
            for variable in self.input_variables:
                self.check_aggregation_mode(aggregation_mode, variable)
                if self.get_run_mode() == True:
                    r_variable = r_variable + '"' + variable[0] + '",'
                    r_function = r_function + '"' + aggregation_mode + '",' 
        r_variable = r_variable[:-1] + '),'
        r_function = r_function[:-1] + ')'
        r_cmd = r_source + "\n" + \
        r_keyword + "(\n" + \
        r_input_filepath + "\n" + \
        r_input_start_time + "\n" + \
        r_input_end_time + "\n" + \
        r_input_time_step + "\n" + \
        r_output_time_step + "\n" + \
        r_variable + "\n" + \
        r_function + ")"
        r_script = "compute_time_series_aggregation.R" 
        f = open(r_script,"w")
        f.write(r_cmd)
        f.close()
        print r_cmd
        #r_cmd = "R --no-save < " + r_script
        #os.system(r_cmd)

    def check_aggregation_mode(self, aggregation_mode, variable):
        """Check if aggregation mode is usefull for actual variable.
        
        Args:
            aggregation_mode: Aggregation mode for actual variable
            variable: Variable name (=columns) to be processed 
        """
        #wxt_temp = temperature
        #wxt_wdir = wind_direction
        #('auto', 'min', 'mean', 'max', 'median', 'sum', \
        #                     'sd', 'circular_mean')
        if variable[1] == 'none':
            self.set_run_mode(False)            
        elif variable[1] == 'wind_direction' and \
            aggregation_mode != 'circular_mean':
            self.set_run_mode(False)            
        elif variable[1] != 'wind_direction' and \
            aggregation_mode == 'circular_mean':
            self.set_run_mode(False)
        else:
            self.set_run_mode(True)
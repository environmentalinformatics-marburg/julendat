"""Visualize level 0050 datasets.
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

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2012-01-17"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import sys
import csv
import os
import string
import ConfigParser
from julendat.processtools import time_utilities
from julendat.filetools.stations.dkstations.DKStationDataFile import DKStationDataFile
import shutil
import time
import datetime
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.metadatatools.stations.Level01Standards import Level01Standards


class VISLevel0050:   
    """Instance for visualizing level 0050 datasets.
    """

    def __init__(self, config_file, pattern="*fah01_0250.dat", run_mode="auto"):
        """Inits VISLevel0050. 
        
        Args:
            Toplevel directory of the datasets
            config_file: Configuration file.
            run_mode: Running mode (auto, manual)
        """
        self.pattern = pattern
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.input_path = self.tl_data_path + self.project_id
        self.output_path = self.toplevel_vis_path + self.project_id
        if not os.path.isdir(self.output_path):
            os.makedirs(self.output_path)
        self.run_flag = True
        if self.get_run_flag():
            self.run()
        else:
            raise Exception, "Run flag is false."

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
    
    def get_run_flag(self):
        """Gets runtime flag information.
        
        Returns:
            Runtime flag.
        """
        return self.run_flag    

    def configure(self,config_file):
        """Reads configuration settings and configure object.
    
        Args:
            config_file: Full path and name of the configuration file.
        """
        self.config_file = config_file
        config = ConfigParser.ConfigParser()
        config.read(self.config_file)
        self.tl_data_path = config.get('repository', 'toplevel_processing_plots_path')
        self.toplevel_vis_path = config.get('repository', 'toplevel_vis_path')
        self.project_id = config.get('project','project_id')
        self.r_filepath = config.get('general','r_filepath')

    def run(self):
        """Executes class functions according to run_mode settings. 
        """
        if self.get_run_mode() == "manual":
            pass
        elif self.get_run_mode() == "auto":
            self.auto()

    def auto(self):
        """Executes class functions in default auto mode.
        """
        self.main()

    def main(self):
        """Processes level 0000 station files to level 0050.
        """
        
        os.chdir(self.r_filepath)
        r_source = 'source("print.ki.strip.R")'
        r_script = 'print.ki.strip('
        r_inputpath = 'inputpath = "' + self.input_path + '",'
        r_outputpath = 'outputpath = "' + self.output_path + '",'
        r_arrange = 'arrange = "long",'
        r_pattern = 'pattern  = "' + self.pattern + '",'
        r_year = 'year = "2011"'
        
        loggers = ['rug', 'pu1', 'pu2', 'rad', 'wxt']
        #loggers = ['rug']
        parameters_rug = ['Ta_200', 'rH_200']
        parameters_pu1 = ['P_RT_NRT']
        parameters_pu2 = ['P_RT_NRT', 'F_RT_NRT']
        parameters_rad = ['Ta_200', 'rH_200',
                          'par_01', 'par_02', 'par_03', 'par_04', 
                          'par_05', 'par_06', 'par_07', 'par_08', 
                          'par_09', 'par_10', 'par_11', 'par_12', 
                          'swdr_13', 'swdr_14', 'swdr_15', 'swdr_16',
                          'swdr_17', 'swdr_18,', 'swdr_19', 'swdr_20', 
                          'swdr_21,', 'swdr_22', 'swdr_23', 'swdr_24']
        parameters_wxt = ['P_RT_NRT', 'SWDR_300', \
                      'SWUR_300', 'LWDR_300', 'LWUR_300', 'Ts_10']
        par_range = {'Ta_200': [-10,50],'rH_200': [0,100], 'P_RT_NRT': [0,60], \
                     'P_RT_NRT': [0,60],
                     'SWDR_300': [0,1400], 'SWUR_300': [0,500], \
                     'LWDR_300': [200,500], 'LWUR_300': [200,500], \
                     'Ts_10': [10, 50], \
                     'par_01': [0, 5000], 'par_02': [0, 5000], \
                     'par_03': [0, 5000], 'par_04': [0, 5000], \
                     'par_05': [0, 5000], 'par_06': [0, 5000], \
                     'par_07': [0, 5000], 'par_08': [0, 5000], \
                     'par_09': [0, 5000], 'par_10': [0, 5000], \
                     'par_11': [0, 5000], 'par_12': [0, 5000], \
                     'swdr_13': [0, 5000], 'swdr_14': [0, 5000], \
                     'swdr_15': [0, 5000], 'swdr_16': [0, 5000], \
                     'swdr_17': [0, 5000], 'swdr_18,': [0, 5000], \
                     'swdr_19': [0, 5000], 'swdr_20': [0, 5000], \
                     'swdr_21,': [0, 5000], 'swdr_22': [0, 5000], \
                     'swdr_23': [0, 5000], 'swdr_24': [0, 5000]}
        
        for logger in loggers:
            r_logger = 'logger = "' + logger + '",'
            if logger == 'rug':
                parameters = parameters_rug
            elif logger == 'wxt':
                parameters = parameters_wxt
            elif logger == 'pu1':
                parameters = parameters_pu1
            elif logger == 'pu2':
                parameters = parameters_pu2
            elif logger == 'rad':
                parameters = parameters_rad
            for parameter in parameters:
                r_prm = 'prm = "' + parameter + '",'
                r_range = 'range = c(' + str(par_range[parameter][0]) + ', ' + \
                           str(par_range[parameter][1]) + '),'
                r_colour = 'colour = VColList$' + str(parameter) + ', '
                r_fun = 'fun = mean,'
                if parameter == 'P_RT_NRT':
                    r_fun = 'fun = sum,'
                for year in range(2011, 2013):
                    r_year = 'year = "' + str(year) + '"'
                    r_cmd = r_source + "\n" + \
                        r_script + "\n" + \
                        r_inputpath + "\n" + \
                        r_outputpath + "\n" + \
                        r_logger + " \n" + \
                        r_prm + " \n" + \
                        r_fun + " \n" + \
                        r_arrange + " \n" + \
                        r_range + " \n" + \
                        r_pattern + " \n" + \
                        r_colour + " \n" + \
                        r_year + ")\n"
    
                    script = "vis0050.rscript" 
                    f = open(script,"w")
                    f.write(r_cmd)
                    f.close()
                    r_cmd = "R CMD BATCH " + script + " " + script + ".log"
                    print r_cmd
                    os.system(r_cmd)

    def get_level0005_standards(self):
        """Sets format standards for level 1 station data files
        """
        level0005_standard = Level01Standards(\
            filepath=self.level0050_standards, \
            station_id=self.filenames.get_station_id())
        self.level0000_column_headers = \
            level0005_standard.get_level0000_column_headers()
        self.level0005_column_headers = \
            level0005_standard.get_level0005_column_headers()
        self.level0050_column_headers = \
            level0005_standard.get_level0050_column_headers()

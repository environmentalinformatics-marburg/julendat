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
import fnmatch
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.metadatatools.stations.Level01Standards import Level01Standards


class VISLevel0050:   
    """Instance for visualizing datasets.
    """

    def __init__(self, config_file, pattern="*fah01_0250.dat", \
                 loggers = ['rug', 'pu1', 'pu2', 'rad', 'wxt'], \
                 self.start_year = None, end_year = None, run_mode="auto"):
        """Inits VISLevel0050. 
        
        Args:
            config_file: Configuration file.
            pattern: Pattern of files to be visualized
            loggers: Loggers to be visualized
            run_mode: Running mode (auto, manual)
        """
        self.loggers = loggers
        self.pattern = pattern
        
        if self.start_year == None: 
            self.start_year = datetime.datetime.now().year
        else:
            self.start_year = start_year
        if end_year == None: 
            self.end_year = datetime.datetime.now().year
        else:
            self.end_year = end_year
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.get_level0050_settings()
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
        self.level0050_standards = config.get('general','level0050_standards')
        self.r_filepath = config.get('general','r_filepath')
        self.tl_processing_path = self.tl_data_path +  self.project_id


    def get_level0050_settings(self):
        """Gets settings for station data files
        """
        self.level0100_quality_parameters = []
        self.level0050_column_headers = []
        for logger in self.loggers:
            temp = Level01Standards(filepath=self.level0050_standards, \
                                    station_id= (6-len(logger))*"0" + logger)
            self.level0050_column_headers.append(\
                temp.get_level0050_column_headers())
            for item in temp.get_level0100_quality_settings()\
                ['quality_parameter']:
                if not "," in item:
                    self.level0100_quality_parameters.append(item.strip())
                else:
                    subitem =  item.split(",")
                    for subsubitem in subitem:
                        self.level0100_quality_parameters.\
                            append(subsubitem.strip())
        self.level0100_quality_parameters = \
            set(self.level0100_quality_parameters)

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
        
        if "wxt" in self.loggers:
            loggers = self.loggers 
            self.loggers = ["wxt"]
            self.visualize_wxt()
            self.loggers = loggers
            self.loggers.remove('wxt')            

        self.visualize_stations()
        
    def visualize_stations(self):
        """Visualize station datasets
        """
        os.chdir(self.r_filepath)
        r_source = 'source("print.ki.strip.R")'
        r_script = 'print.ki.strip('
        r_outputpath = 'outputpath = "' + self.output_path + '",'
        r_arrange = 'arrange = "long",'
        r_pattern = 'pattern  = "' + self.pattern + '",'
        r_year = 'year = "2011"'
        '''
        self.loggers = ['rug', 'pu1', 'pu2', 'rad', 'wxt']
        self.parameters_rug = ['Ta_200', 'rH_200']
        self.parameters_pu1 = ['P_RT_NRT']
        self.parameters_pu2 = ['P_RT_NRT_01', 'P_RT_NRT_02', \
                              'F_RT_NRT_01', 'F_RT_NRT_02']
        self.parameters_rad = ['Ta_200', 'rH_200',
                          'par_01', 'par_02', 'par_03', 'par_04', 
                          'par_05', 'par_06', 'par_07', 'par_08', 
                          'par_09', 'par_10', 'par_11', 'par_12', 
                          'swdr_13', 'swdr_14', 'swdr_15', 'swdr_16',
                          'swdr_17', 'swdr_18,', 'swdr_19', 'swdr_20', 
                          'swdr_21,', 'swdr_22', 'swdr_23', 'swdr_24']
        self.parameters_wxt = ['P_RT_NRT', 'SWDR_300', \
                      'SWUR_300', 'LWDR_300', 'LWUR_300', 'Ts_10']
        '''
        par_range = {'Ta_200': [-10,50],'rH_200': [0,100], \
                     'P_RT_NRT': [0,60], \
                     'P_RT_NRT_01': [0,60], 'P_RT_NRT_02': [0,60],
                     'F_RT_NRT_01': [0,60], 'F_RT_NRT_02': [0,60],
                     'SWDR_300': [0,1400], 'SWUR_300': [0,500], \
                     'LWDR_300': [200,500], 'LWUR_300': [200,500], \
                     'WD': [0,360], 'WV': [0,10], \
                     'Ts_10': [10, 50], \
                     'p_200': [750, 1100], \
                     'par_01': [0, 5000], 'par_02': [0, 5000], \
                     'par_03': [0, 5000], 'par_04': [0, 5000], \
                     'par_05': [0, 5000], 'par_06': [0, 5000], \
                     'par_07': [0, 5000], 'par_08': [0, 5000], \
                     'par_09': [0, 5000], 'par_10': [0, 5000], \
                     'par_11': [0, 5000], 'par_12': [0, 5000], \
                     'swdr_13': [0, 5000], 'swdr_14': [0, 5000], \
                     'swdr_15': [0, 5000], 'swdr_16': [0, 5000], \
                     'swdr_17': [0, 5000], 'swdr_18': [0, 5000], \
                     'swdr_19': [0, 5000], 'swdr_20': [0, 5000], \
                     'swdr_21': [0, 5000], 'swdr_22': [0, 5000], \
                     'swdr_23': [0, 5000], 'swdr_24': [0, 5000]}
        
        print self.level0100_quality_parameters
        for parameter in self.level0100_quality_parameters:
           for year in range(self.start_year, self.end_year):
                print parameter
                self.inputfilepath = []
                for i in range(0, len(self.loggers)):
                    if parameter in self.level0050_column_headers[i]:
                        for path, dirs, files in os.walk(os.path.abspath(\
                                             self.tl_processing_path)):
                            for filename in fnmatch.filter(files, \
                                                    "*" + self.loggers[i] + \
                                                    "*" + str(year) + "*" + \
                                                    self.pattern):
                                self.inputfilepath.append(\
                                                os.path.join(path, filename))
                self.inputfilepath = sorted(self.inputfilepath)
                inputfilepath = 'c('
                for station in self.inputfilepath:
                    inputfilepath = inputfilepath + '"' + \
                                           station + '", \n' 
                inputfilepath = inputfilepath[:-3]
            
                r_inputfilepath = 'inputfilepath = ' + inputfilepath + '),'
                r_prm = 'prm = "' + parameter + '",'
                r_range = 'range = c(' + str(par_range[parameter][0]) + ', ' + \
                          str(par_range[parameter][1]) + '),'
                r_colour = 'colour = VColList$' + str(parameter) + ', '
                r_fun = 'fun = mean,'
                if 'RT_NRT' in parameter:
                    r_fun = 'fun = sum,'
                r_year = 'year = "' + str(year) + '"'
                r_cmd = r_source + "\n" + \
                r_script + "\n" + \
                r_inputfilepath + "\n" + \
                r_outputpath + "\n" + \
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
                os.system(r_cmd)
   
   
    def visualize_wxt(self):
        """Visualize station datasets
        """
        os.chdir(self.r_filepath)
        r_source = 'source("print.wxt.ki.strip.R")'
        r_script = 'print.wxt.ki.strip('
        r_outputpath = 'outputfilepath = "' + self.output_path + '",'
        r_pattern = 'ptrn  = "' + self.pattern + '",'
        r_minx = 'minx = list(-10, 0, -10, 0, 0, 200, 200, 0, 0, 750, 0),'
        r_maxx = 'maxx = list(50, 100, 50, 1400, 500, 500, 600, 360, 10, 1100, 60)'
        par_range = {'Ta_200': [-10,50],'rH_200': [0,100], \
                     'P_RT_NRT': [0,60], \
                     'P_RT_NRT_01': [0,60], 'P_RT_NRT_02': [0,60],
                     'F_RT_NRT_01': [0,60], 'F_RT_NRT_02': [0,60],
                     'SWDR_300': [0,1400], 'SWUR_300': [0,500], \
                     'LWDR_300': [200,500], 'LWUR_300': [200,500], \
                     'WD': [0,360], 'WV': [0,10], \
                     'Ts_10': [10, 50], \
                     'p_200': [750, 1100], \
                     'par_01': [0, 5000], 'par_02': [0, 5000], \
                     'par_03': [0, 5000], 'par_04': [0, 5000], \
                     'par_05': [0, 5000], 'par_06': [0, 5000], \
                     'par_07': [0, 5000], 'par_08': [0, 5000], \
                     'par_09': [0, 5000], 'par_10': [0, 5000], \
                     'par_11': [0, 5000], 'par_12': [0, 5000], \
                     'swdr_13': [0, 5000], 'swdr_14': [0, 5000], \
                     'swdr_15': [0, 5000], 'swdr_16': [0, 5000], \
                     'swdr_17': [0, 5000], 'swdr_18': [0, 5000], \
                     'swdr_19': [0, 5000], 'swdr_20': [0, 5000], \
                     'swdr_21': [0, 5000], 'swdr_22': [0, 5000], \
                     'swdr_23': [0, 5000], 'swdr_24': [0, 5000]}
        
        for year in range(self.start_year, self.end_year):
            self.inputpath = []
            for i in range(0, len(self.loggers)):
                for path, dirs, files in os.walk(os.path.abspath(\
                                         self.tl_processing_path)):
                        for filename in fnmatch.filter(files, \
                                                "*" + self.loggers[i] + \
                                                "*" + str(year) + "*" + \
                                                self.pattern):
                            self.inputpath.append(\
                                            os.path.join(path))
            self.inputpath = sorted(set(self.inputpath))
            for station in self.inputpath:
                r_inputfilepath = 'inputpath = "' + station + '/",'
                r_year = 'year = "' + str(year) + '",'
                r_pid = 'plotid = "' + station [-20:-16] + '",'
                r_cmd = r_source + "\n" + \
                r_script + "\n" + \
                r_inputfilepath + "\n" + \
                r_outputpath + "\n" + \
                r_pid + " \n" + \
                r_year + " \n" + \
                r_pattern + " \n" + \
                r_minx + " \n" + \
                r_maxx + ")\n"
    
                script = "vis0050wxt.rscript" 
                f = open(script,"w")
                f.write(r_cmd)
                f.close()
                r_cmd = "R CMD BATCH " + script + " " + script + ".log"
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

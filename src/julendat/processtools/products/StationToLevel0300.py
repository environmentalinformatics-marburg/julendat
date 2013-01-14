"""Process level 0200 station data to gap-filled level 0300.
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
__version__ = "2012-01-18"
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
import fnmatch
import datetime
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.metadatatools.stations.Level01Standards import Level01Standards


class StationToLevel0300:   
    """Instance for processing station level 0200 to level 0300 data.
    """

    def __init__(self, filepath, config_file, \
                 parameters = ["Ta_200", "rH_200"], level = "300", \
                 run_mode="auto"):
        """Inits StationToLevel0300. 
        
        Args:
            filepath: Full path and name of the level 0050 file
            config_file: Configuration file.
            parameters: Meteorological parameters that should be processed
            level: Target level
            run_mode: Running mode (auto, manual)
        """
        self.level = level
        self.set_parameters(parameters)
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.init_filenames(filepath)
        if self.get_run_flag():
            self.run()
        else:
            raise Exception, "Run flag is false."

    def set_parameters(self,parameters):
        """Set meteorological parameters to be processed.
        
        Args:
            parameters: Meteorological parameters that should be processed
        """
        self.parameters = parameters

    def get_parameters(self):
        """Gets meteorological parameters to be processed.
        
        Returns:
            parameters: Meteorological parameters that should be processed
        """
        return self.parameters
    
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

    def configure(self,config_file):
        """Reads configuration settings and configure object.
    
        Args:
            config_file: Full path and name of the configuration file.
        """
        self.config_file = config_file
        config = ConfigParser.ConfigParser()
        config.read(self.config_file)
        self.tl_data_path = config.get('repository', 'toplevel_processing_plots_path')
        self.station_inventory = config.get('inventory','station_inventory')
        self.station_master = config.get('inventory', 'station_master')
        self.project_id = config.get('project','project_id')
        self.level0050_standards = config.get('general','level0050_standards')
        self.r_filepath = config.get('general','r_filepath')
        self.tl_processing_path = self.tl_data_path +  self.project_id

    def init_filenames(self, filepath):
        """Initializes D&K station data file.
        
        Args:
            filepath: Full path and name of the level 0 file
        """
        try:
            self.filenames = StationDataFilePath(filepath=filepath, \
                toplevel_path=self.tl_data_path)
            self.start_datetime = self.filenames.get_start_datetime_eifc()
            self.filenames.build_filename_dictionary()
            self.run_flag = True
        except:
            raise Exception, "Can not compute station data filepath"
            self.run_flag = False

    def get_run_flag(self):
        """Gets runtime flag information.
        
        Returns:
            Runtime flag.
        """        

        return self.run_flag

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
        """Processes level 0050 station files to level 0100.
        """
        self.get_level0100_quality_settings()
        self.set_independent_files()
        self.process_gap_filling()


    def get_level0100_quality_settings(self):
        """Sets quality settings for level 0100 station data files
        """
        level0100_standard = Level01Standards(\
            filepath=self.level0050_standards, \
            station_id=self.filenames.get_station_id())
        self.level0100_quality_settings = \
            level0100_standard.get_level0100_quality_settings()


    def set_independent_files(self):
        """Sets a list of independent files used for gap filling
        """
        if self.level == "0300":
            wildcard = self.filenames.get_filename_dictionary()\
                ['level_0290_wildcard']
            wildcard_rug = self.filenames.get_filename_dictionary()\
                ['level_0290_wildcard_rug']
        elif self.level == "0310":
            wildcard = self.filenames.get_filename_dictionary()\
                ['level_0300_wildcard']
            wildcard_rug = self.filenames.get_filename_dictionary()\
                ['level_0300_wildcard_rug']

        self.independent_files = []
        for path, dirs, files in os.walk(os.path.abspath(\
                                         self.tl_processing_path)):
            for filename in fnmatch.filter(files, wildcard):
                    self.independent_files.append(os.path.join(path, filename))

        if "wxt" in self.filenames.get_station_id():
            for path, dirs, files in os.walk(os.path.abspath(\
                                         self.tl_processing_path)):
                for filename in fnmatch.filter(files, wildcard_rug):
                    self.independent_files.append(os.path.join(path, filename))

            
    def process_gap_filling(self):
        """Process gap filling on level 0200 file.
        
        """
        if self.level == "0300":
            output_path = self.filenames.get_filename_dictionary()\
                                  ["level_0300_ascii-path"]
            output_filepath = self.filenames.get_filename_dictionary()\
                                  ["level_0300_ascii-filepath"]
            input_filepath = self.filenames.get_filename_dictionary()\
                                  ["level_0290_ascii-filepath"]
        elif self.level == "0310":
            output_path = self.filenames.get_filename_dictionary()\
                                  ["level_0310_ascii-path"]
            output_filepath = self.filenames.get_filename_dictionary()\
                                  ["level_0310_ascii-filepath"]
            input_filepath = self.filenames.get_filename_dictionary()\
                                  ["level_0300_ascii-filepath"]

        if not os.path.isdir(output_path):
                os.makedirs(output_path)
        
        r_source = 'source("' + self.r_filepath + os.sep + \
                'gfWrite.R")'
        r_keyword = "gfWrite"
        r_fd = 'files.dep = "' +  input_filepath + '"'
        print r_fd
        print self.independent_files 
        self.independent_files.remove(input_filepath)
        
        independent_stations = 'c('
        for station in self.independent_files:
            independent_stations = independent_stations + '"' + \
                                   station + '", \n' 
        independent_stations = independent_stations[:-3]
        r_fid = 'files.indep = ' + independent_stations  + ')'
        r_fop = 'filepath.output = "' +  output_filepath + '"'
        r_fcp = 'filepath.coords = "' + self.station_master + '"'
        r_ql = 'quality.levels = c(12,22)'
        r_gl = 'gap.limit = 9000' 
        r_nal = 'na.limit = 0.99'
        r_tw = 'time.window = 1000'
        r_nplot = 'n.plot = 10'
        r_pdp = 'prm.dep = c('
        for parameter in self.get_parameters():
            r_pdp = r_pdp + '"' + parameter + '", ' 
        r_pdp = r_pdp[:-2] + ')'
        r_pid = 'prm.indep = c(NA, "Ta_200")'
        r_plevel = 'plevel = 0300'
        r_family = 'family = gaussian'

        act_wd = os.getcwd()
        os.chdir(self.r_filepath)
        r_cmd = r_source + '\n' + \
                r_keyword + '(\n' + \
                r_fd + ',\n' + \
                r_fid + ',\n' + \
                r_fop + ',\n' + \
                r_fcp + ',\n' + \
                r_ql + ',\n' + \
                r_gl + ',\n' + \
                r_nal + ',\n' + \
                r_tw + ',\n' + \
                r_nplot + ',\n' + \
                r_pdp + ',\n' + \
                r_pid + ',\n' + \
                r_plevel + ',\n' + \
                r_family + ')\n'
        r_script = "gfcall.rscript" 
        f = open(r_script,"w")
        f.write(r_cmd)
        f.close()
        r_cmd = 'R CMD BATCH ' + r_script  + ' ' + r_script + '.log'
        os.system(r_cmd)
        os.chdir(act_wd)

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
import datetime
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.metadatatools.stations.Level01Standards import Level01Standards


class StationToLevel0300:   
    """Instance for processing station level 0200 to level 0300 data.
    """

    def __init__(self, filepath, config_file,run_mode="auto"):
        """Inits StationToLevel0100. 
        
        Args:
            filepath: Full path and name of the level 0050 file
            config_file: Configuration file.
            run_mode: Running mode (auto, manual)
        """
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.init_filenames(filepath)
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
        self.process_gap_filling()


    def get_level0100_quality_settings(self):
        """Sets quality settings for level 0100 station data files
        """
        level0100_standard = Level01Standards(\
            filepath=self.level0050_standards, \
            station_id=self.filenames.get_station_id())
        self.level0100_quality_settings = \
            level0100_standard.get_level0100_quality_settings()

    def process_gap_filling(self):
        """Process gap filling on level 0200 file.
        
        """
        if not os.path.isdir(self.filenames.get_filename_dictionary()\
            ["level_0300_ascii-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()\
                ["level_0300_ascii-path"])
        
        output_filepath = self.filenames.get_filename_dictionary()\
            ["level_0300_ascii-filepath"]
        
        r_source = 'source("' + self.r_filepath + os.sep + \
                'gfWrite.R")'
        r_keyword = "gfWrite"
        r_fd = 'files.dep = list.files("' + self.tl_processing_path + \
            '", pattern = glob2rx("*' + \
            self.filenames.get_filename_dictionary()['level_0200_wildcard'] + \
            '"), recursive = TRUE, full.names = TRUE)[1]'
        r_fid = 'files.indep = c(list.files("' + self.tl_processing_path + \
            '", pattern = glob2rx("*' + \
            self.filenames.get_filename_dictionary()['level_0200_wildcard'] + \
            '"), recursive = TRUE, full.names = TRUE)[-1])'
        r_fop = 'filepath.output = "' + output_filepath + '"'
        r_fcp = 'filepath.coords = "' + self.station_master + '"'
        r_ql = 'quality.levels = c(12, 21)'
        r_nal = 'na.limit = 0.1'
        r_nplot = 'n.plot = 10'
        r_pdp = 'prm.dep = c("Ta_200", "rH_200")' 
        r_pid = 'prm.indep = c(NA, "Ta_200")'


        
        act_wd = os.getcwd()
        os.chdir(self.r_filepath)
        r_cmd = r_source + '\n' + \
                r_keyword + '(\n' + \
                r_fd + ',\n' + \
                r_fid + ',\n' + \
                r_fop + ',\n' + \
                r_fcp + ',\n' + \
                r_ql + ',\n' + \
                r_nal + ',\n' + \
                r_nplot + ',\n' + \
                r_pdp + ',\n' + \
                r_pid + ')\n'
        r_script = "gfcall.rscript" 
        f = open(r_script,"w")
        f.write(r_cmd)
        f.close()
        r_cmd = 'R CMD BATCH ' + r_script  + ' ' + r_script + '.log'
        os.system(r_cmd)
        sys.exit()
        os.chdir(act_wd)

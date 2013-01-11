"""Process level 0250 station data to concatenated level 0290.
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
__version__ = "2013-01-07"
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


class StationToLevel0290:   
    """Instance for processing station level 0250 to level 0290 data.
    """

    def __init__(self, filepath, config_file,run_mode="auto"):
        """Inits StationToLevel0200. 
        
        Args:
            filepath: Full path and name of the level 0100 file
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
        self.project_id = config.get('project','project_id')
        self.level0050_standards = config.get('general','level0050_standards')
        self.r_filepath = config.get('general','r_filepath')

    def init_filenames(self, filepath):
        """Initializes D&K station data file.
        
        Args:
            filepath: Full path and name of the level 0 file
        """
        try:
            self.filenames = StationDataFilePath(filepath=filepath, \
                toplevel_path=self.tl_data_path)
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
        if self.get_run_mode() == "concatenate":
            self.concatenate()
        else:
            pass

    def move_data(self):
        """Moves files.
        """
        shutil.move(self.source,self.destination)

    def concatenate(self):
        """Concatenate level 0250 station files.
        """
        aggregation_level = "fah01"
        self.filenames.build_filename_dictionary(aggregation_level)
        output_path = self.filenames.get_filename_dictionary()\
                      ["level_0290_ascii-path"]
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        infile = open(self.filenames.get_filepath(), "r")
        if os.path.isfile(self.filenames.get_filename_dictionary()\
                      ["level_0290_ascii-filepath"]):
            infile.readline()
        infile_content = infile.read()
        infile.close()
        outfile = open(self.filenames.get_filename_dictionary()\
                      ["level_0290_ascii-filepath"], "a")
        outfile.write(infile_content)
        outfile.close()


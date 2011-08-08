"""Convert D&K level 0 logger data to level 1.
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
__version__ = "2010-08-07"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"


import ConfigParser
from julendat.filetools.stations.dkstations.DKStationDataFile import DKStationDataFile
import os
import shutil
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.guitools.stations.GUIAutoPlotSelection import GUIAutoPlotSelection
from julendat.guitools.stations.GUIManualPlotSelection import GUIManualPlotSelection
import Tkinter

class DKStationLevel02Level1:   
    """Instance for converting D&K logger level 0 to level 1data.
    """

    def __init__(self, filepath, config_file,run_mode="auto"):
        """Inits DKStationLevel02Level1. 
        
        Args:
            filepath: Full path and name of the level 0 file
            config_file: Configuration file.
            run_mode: Running mode (auto, manual)
        """
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.init_filenames(filepath)
        if self.get_run_flag():
            self.run()
            
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
        self.tl_data_path = config.get('repository', 'toplevel_repository_path')
        self.station_inventory = config.get('inventory','station_inventory')
        self.project_id = config.get('project','project_id')

    def init_filenames(self, filepath):
        """Initializes D&K station data file.
        
        Args:
            filepath: Full path and name of the level 0 file
        """
        try:
            self.filenames = StationDataFilePath(filepath=filepath, \
                                tl_data_path = self.tl_data_path)
            self.run_flag = True
        except:
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
        
    def move_data(self):
        """Moves files.
        """
        shutil.move(self.source,self.destination)

    def main(self):
        """Maps logger files to level 0 filename and directory structure.
        """
        print self.filenames.get_filename_dictionary()["level_000_bin-filename"]
        print self.filenames.get_filename_dictionary()["level_000_bin-path"]
        print self.filenames.get_filename_dictionary()["level_000_bin-filepath"]
        print self.filenames.get_filename_dictionary()["level_001_ascii-filename"]
        print self.filenames.get_filename_dictionary()["level_001_ascii-path"]
        print self.filenames.get_filename_dictionary()["level_001_ascii-filepath"]

        # Check if path for level 0 files exists, otherwise create it        
        if not os.path.isdir(self.filenames.get_filename_dictionary()["level_000_bin-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()["level_000_bin-path"])
        if not os.path.isdir(self.filenames.get_filename_dictionary()["level_001_ascii-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()["level_001_ascii-path"])
        
        # Set full path and names of ASCII data files and move them
        self.source = self.level0_file.get_filepath()
        self.destination =  self.filenames.get_filename_dictionary()["level_001_ascii-filepath"]
        print self.source
        print self.destination
        self.move_data()
        
        if os.path.isfile(self.binary_logger_file.get_filepath()) and \
                          self.level0_file.get_file_exists():
            # Move binary data
            self.source = self.binary_logger_file.get_filepath()
            self.destination = self.filenames.get_filename_dictionary()["level_000_bin-filepath"]
            print self.source
            print self.destination
            self.move_data()

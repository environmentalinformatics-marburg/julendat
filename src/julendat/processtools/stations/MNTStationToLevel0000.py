"""Move downloaded MayerNT logger data to level 0 folder structure.
Copyright (C) 2011 Thomas Nauss, Insa Otte, Falk Haensel

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

__author__ = "Thomas Nauss <nausst@googlemail.com> , Insa Otte, Falk Haensel"
__version__ = "2012-01-08"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import os
import sys
import shutil
import Tkinter
from julendat.filetools.stations.dkstations.MNTStationDataFile import \
    MNTStationDataFile
from julendat.metadatatools.stations.StationDataFilePath import \
    StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.guitools.stations.GUIAutoPlotSelection import GUIAutoPlotSelection
from julendat.guitools.stations.GUIManualPlotSelection import \
    GUIManualPlotSelection


class MNTStationToLevel0000:   
    """Instance for moving downloaded D&K logger data to level 0 folders.
    """

    def __init__(self, input_filepath, config_file,run_mode="auto"):
        """Inits MNTStationToLevel0000.
        The instance is initialized by reading a configuration file and the 
        initialization of the proprietary station data file instance.
        If the run mode is set to "auto", this is followed by an automatic
        configuration of filenames and filepathes and the movement of the
        station data file to the processing path structure.  
        
        Args:
            input_filepath: Full path and name of the level 0 file
            config_file: Configuration file.
            run_mode: Running mode (auto, manual)
        """
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.init_StationFile(input_filepath)
        if self.get_run_flag():
            self.auto_configure()
            self.run()
        else:
            print "Nothing to do..."
            print "...finished."        

    def set_run_mode(self, run_mode):
        """Sets run mode.
        
        Args:
            run_mode: Running mode (default: auto-gui)
        """
        self.run_mode = run_mode

    def get_run_mode(self):
        """Gets run mode.
        
        Returns:
            Running mode
        """
        return self.run_mode

    def configure(self, config_file):
        """Reads configuration settings and configure object.
    
        Args:
            config_file: Full path and name of the configuration file.
            
        """
        self.config_file = config_file
        config = ConfigParser.ConfigParser()
        config.read(self.config_file)
        self.initial_logger_filepath = \
            config.get('repository', 'toplevel_processing_logger_path') + \
            config.get('logger', 'initial_logger_file')
        self.logger_time_zone = config.get('logger', 'logger_time_zone')
        self.tl_data_path = config.get('repository', 'toplevel_processing_plots_path')
        self.project_id = config.get('project', 'project_id')
        self.station_inventory = config.get('inventory', 'station_inventory')

    def init_StationFile(self, input_filepath):
        """Initializes D&K station data file.

        Args:
            input_filepath: Full path and name of the level 0 file
        """
        #try:
        self.logger_file = MNTStationDataFile(\
                                         filepath=input_filepath)
        self.logger_file.set_time_range_ascii()
                
        self.run_flag = self.logger_file.get_file_exists()
        #except:
            #TODO(tnauss): Handle exception more properly.
        #self.run_flag = False

    def get_run_flag(self):
        """Gets runtime flag information.
        
        Returns:
            Runtime flag.
        """
        return self.run_flag

    def auto_configure(self):
        """Set necessary attributes automatically.
        """
        pass
        self.inventory = StationInventory(filepath=self.station_inventory, \
            logger_start_time = self.logger_file.get_start_datetime(), \
            logger_end_time = self.logger_file.get_end_datetime(), \
            plot_id=self.logger_file.get_plot_id())
        
        if self.inventory.get_found_station_inventory():
            self.plot_id = self.inventory.get_plot_id()
            self.station_id = self.inventory.get_station_id()
    
    def run(self):
        """Executes class functions according to run_mode settings. 
        """
        if self.get_run_mode() == "manual":
            pass
        elif self.get_run_mode() == "auto":
            self.set_level0_filenames(project_id=self.project_id)
            self.main()            
        
    def move_data(self):
        """Moves files.
        """
        shutil.move(self.source, self.destination)

    def get_plot_id(self):
        """Gets coded plot id flag information.
        
        Returns:
            Runtime coded plot ID 
        """
        return self.plot_id
    
    def set_level0_filenames(self, project_id=None, \
                             plot_id=None, postexflag=None):
        """Sets level0 filenames and path information
        """
        if plot_id == None:
            plot_id = self.logger_file.get_plot_id()
        self.filenames = StationDataFilePath(\
                        toplevel_path=self.tl_data_path, \
                        project_id=project_id, \
                        plot_id=plot_id, \
                        station_id=self.station_id, \
                        start_datetime=self.logger_file.get_start_datetime(), \
                        end_datetime=self.logger_file.get_end_datetime(), \
                        time_step_delta = self.logger_file.get_time_step_delta(), \
                        logger_time_zone=self.logger_time_zone, \
                        aggregation_level="na", \
                        postexflag=postexflag)  
        self.filenames.build_filename_dictionary()

    def main(self):
        """Maps logger files to level 0 filename and directory structure.
        """
        print self.filenames.get_filename_dictionary()["level_000_bin-filename"]
        print self.filenames.get_filename_dictionary()["level_000_bin-path"]
        print self.filenames.get_filename_dictionary()["level_000_bin-filepath"]
        print self.filenames.get_filename_dictionary()["level_0000_ascii-filename"]
        print self.filenames.get_filename_dictionary()["level_0000_ascii-path"]
        print self.filenames.get_filename_dictionary()["level_0000_ascii-filepath"]

        # Check if path for level 0 files exists, otherwise create it        
        if not os.path.isdir(self.filenames.get_filename_dictionary()["level_000_bin-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()["level_000_bin-path"])
        if not os.path.isdir(self.filenames.get_filename_dictionary()["level_0000_ascii-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()["level_0000_ascii-path"])
        
        # Set full path and names of ASCII data files and move them
        self.source = self.logger_file.get_filepath()
        self.destination = self.filenames.get_filename_dictionary()["level_0000_ascii-filepath"]
        print self.source
        print self.destination
        self.move_data()
        
        #if os.path.isfile(self.binary_logger_file.get_filepath()) and \
        #                  self.logger_file.get_file_exists():
        #    # Move binary data
        #    self.source = self.binary_logger_file.get_filepath()
        #    self.destination = self.filenames.get_filename_dictionary()["level_000_bin-filepath"]
        #    print self.source
        #    print self.destination
        #   self.move_data()

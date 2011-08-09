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
from julendat.metadatatools.stations.StationEntries import StationEntries
from julendat.metadatatools.stations.Level01Standards import Level01Standards
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
        self.station_entries = config.get('logger', 'station_entries')

        
        self.tl_data_path = config.get('repository', 'toplevel_repository_path')
        self.station_inventory = config.get('inventory','station_inventory')
        self.project_id = config.get('project','project_id')
        self.level01_standards = config.get('general','level01_standards')

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
            self.filenames = StationDataFilePath(filepath=filepath, \
                                toplevel_path=self.tl_data_path)
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
        print self.filenames.get_filename_dictionary()["level_00_ascii-filepath"]
        #print self.filenames.get_filename_dictionary()["level_05_ascii-filepath"]
        #for i in range(0,len(self.filenames.get_filename_dictionary()["level_06_ascii-filepath"])):
        #    print self.filenames.get_filename_dictionary()["level_06_ascii-filepath"][i]
        #print self.filenames.get_filename_dictionary()["level_06_ascii-filepath"]
        #print self.filenames.get_filename_dictionary()["level_10_ascii-filepath"]
        
        self.get_calibartion_coefficients()
        self.get_station_entries()
        self.get_level01_standards()
        self.level_05()

    def get_calibartion_coefficients(self):
        filepath=self.filenames.get_filename_dictionary()[\
                                                "level_00_ascii-filepath"]
        print filepath
        try:
            level_00_ascii_file = DKStationDataFile(filepath=filepath)
            self.run_flag = level_00_ascii_file.get_file_exists()
        except:
            self.run_flag = False
        
        if self.get_run_flag():
            inventory = StationInventory(filepath=self.station_inventory, \
                    serial_number = level_00_ascii_file.get_serial_number())
            if self.filenames.get_raw_plot_id() != inventory.get_plot_id():
                self.run_flag = False
            elif self.filenames.get_station_id() != inventory.get_station_id():
                print self.filenames.get_station_id()
                print inventory.get_station_id()
                self.run_flag = False
        if self.get_run_flag():
            self.calib_coefficients_headers, self.calib_coefficients = \
            inventory.get_calibration_coefficients()
        
    def get_station_entries(self):
        station_entries = StationEntries(filepath=self.station_entries, \
                                    station_id=self.filenames.get_station_id())
        self.line_skip = station_entries.get_line_skip()
        self.station_column_entries = \
            station_entries.get_station_column_entries()

    def get_level01_standards(self):
        level01_standards = Level01Standards(\
                                    filepath=self.level01_standards)
        self.level01_column_entries = \
            level01_standards.get_level01_column_entries()
        
    def level_05(self):
            print 'source("D:/kili_data/testing/individual.r")'
            print "individual("
            print 'asciipath="' + self.filenames.get_filename_dictionary()["level_00_ascii-filepath"] + '",'
            print 'outpath="' + self.filenames.get_filename_dictionary()["level_05_ascii-filepath"] + '",'
            print 'plotID="' + self.filenames.get_raw_plot_id() + '",'
            print 'loggertype="' + self.filenames.get_station_id() + '",'
            print "cf=c(" , [float(li) for li in self.calib_coefficients] , "),"
            print "reorder=c(1,2,"
            for e in range (2,len(self.station_column_entries)):
                for i in range(0,len(self.level01_column_entries)):
                    if self.level01_column_entries[i] ==  \
                        self.station_column_entries[e]:
                            print i+1 
            print "),"
            print  "skip=" + self.line_skip + ","
            print "order_out=c(" , self.level01_column_entries[:] , "))"
            #print self.station_column_entries
            #print self.level01_column_entries
            
            
            

        

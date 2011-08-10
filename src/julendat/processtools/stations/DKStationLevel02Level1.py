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


import os
import ConfigParser
from julendat.filetools.stations.dkstations.DKStationDataFile import DKStationDataFile
import shutil
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.metadatatools.stations.StationEntries import StationEntries
from julendat.metadatatools.stations.Level01Standards import Level01Standards
from julendat.filetools.DataFile import DataFile

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
        #print self.filenames.get_filename_dictionary()["level_000_ascii-filepath"]
        #print self.filenames.get_filename_dictionary()["level_005_ascii-filepath"]
        #for i in range(0,len(self.filenames.get_filename_dictionary()["level_010_ascii-filepath"])):
        #    print self.filenames.get_filename_dictionary()["level_010_ascii-filepath"][i]
        #print self.filenames.get_filename_dictionary()["level_010_ascii-filepath"]
        #print self.filenames.get_filename_dictionary()["level_010_ascii-filepath"]
        
        self.set_calibration_coefficients()
        self.set_station_entries()
        self.set_level01_standards()
        self.level_005()
        self.level_010()
        print "...finished."

    def set_calibration_coefficients(self):
        """Sets calibration coefficients for the recorded logger parameters
        """
        filepath=self.filenames.get_filename_dictionary()[\
                                                "level_000_ascii-filepath"]
        try:
            level_000_ascii_file = DKStationDataFile(filepath=filepath)
            self.run_flag = level_000_ascii_file.get_file_exists()
        except:
            self.run_flag = False
        
        if self.get_run_flag():
            inventory = StationInventory(filepath=self.station_inventory, \
                    serial_number = level_000_ascii_file.get_serial_number())
            if self.filenames.get_raw_plot_id() != inventory.get_plot_id():
                self.run_flag = False
            elif self.filenames.get_station_id() != inventory.get_station_id():
                print self.filenames.get_station_id()
                print inventory.get_station_id()
                self.run_flag = False
        if self.get_run_flag():
            self.calib_coefficients_headers, self.calib_coefficients = \
            inventory.get_calibration_coefficients()
        
    def set_station_entries(self):
        """Sets station logger entries (meaning of coloumns)
        """
        station_entries = StationEntries(filepath=self.station_entries, \
                                    station_id=self.filenames.get_station_id())
        self.line_skip = station_entries.get_line_skip()
        self.station_column_entries = \
            station_entries.get_station_column_entries()

    def set_level01_standards(self):
        """Sets format standards for level 1 station data files
        """
        level01_standards = Level01Standards(\
                                    filepath=self.level01_standards)
        self.level10_column_entries = \
            level01_standards.get_level01_column_entries()
        
    def level_005(self):
        """Compute level 0.5 station data sets
        """
        r_source = 'source("D:/kili_data/testing/compute_level_005_file.r")'
        r_keyword = "compute_level_005_file"
        r_input_filepath = \
           'asciipath="' + \
            self.filenames.get_filename_dictionary()\
            ["level_000_ascii-filepath"] + '",'
        r_output_filepath = 'outpath="' + \
            self.filenames.get_filename_dictionary()\
            ["level_005_ascii-filepath"] + '",'
        r_plot_id = 'plotID="' + self.filenames.get_raw_plot_id() + '",'
        r_station_id = 'loggertype="' + \
            self.filenames.get_station_id() + '",'
        r_calibration_coefficients = 'cf=c('  + \
           self.convert_floatlist2string(self.calib_coefficients) + '),'
        self.reorder_station_coloumn_entries()
        r_reorder = 'reorder=c('+ self.convert_floatlist2string(self.reorder) + ')'
        r_skip = 'skip=' + self.line_skip + ','
        r_order_out = 'order_out=c(' + \
            self.convert_list2string(self.level10_column_entries) + ')'
            
        r_cmd = r_source + "\n" + \
            r_keyword + " (\n" + \
            r_input_filepath + "\n" + \
            r_output_filepath + "\n" + \
            r_plot_id + "\n" + \
            r_station_id + "\n" + \
            r_calibration_coefficients + "\n" + \
            r_reorder + "\n" + \
            r_skip + "\n" + \
            r_order_out  + ") \n"
        f = open("compute_level_005_file.r","w")
        f.write(r_cmd)
        f.close()
        print r_cmd
            
    def level_010(self):
        """Compute level 1.0 station data sets
        """
        #Check if monthly combined target file for level 0.6 already exists
        filenumber = len(self.filenames.get_filename_dictionary()\
                         ["level_010_ascii-filepath"])
        level_010_file = []
        for act_file in range(0, filenumber):
            print "Act_File, ", act_file
            level_010_file.append(DataFile(\
                 self.filenames.get_filename_dictionary()\
                 ["level_010_ascii-filepath"][act_file]))
            if level_010_file[act_file].check_file_exists() != True:
                self.init_level_010_file(level_010_file[act_file].get_filepath())
            if not os.path.isdir(self.filenames.get_filename_dictionary()["level_010_ascii-path"][act_file]):
                os.makedirs(self.filenames.get_filename_dictionary()["level_010_ascii-path"][act_file])
                
            self.compute_level_010_file(\
                 self.filenames.get_filename_dictionary()\
                 ["level_005_ascii-filepath"], \
                 level_010_file[act_file].get_filepath())
            
    def init_level_010_file(self, filepath):
        """Init level 1.0 file
        """
        r_source = 'source("D:/kili_data/testing/init_level_010_file.r")'
        r_keyword = "init_level_010_file"
        r_output_filepath = 'outpath="' + filepath + '",'
        r_start_time = 'start_time=' + os.path.split(filepath)[1][16:28] + ','
        r_end_time = 'end_time=' + os.path.split(filepath)[1][29:41] + ','
        r_time_step = 'time_step=' + str(float(self.filenames.get_time_step())*60.0) + ''
            
        r_cmd = r_source + "\n" + \
            r_keyword + " (\n" + \
            r_output_filepath + "\n" + \
            r_start_time + "\n" + \
            r_end_time + "\n" + \
            r_time_step + ")\n"
        f = open("init_level_010_file.r","w")
        f.write(r_cmd)
        f.close()
        print r_cmd

    def compute_level_010_file(self,station_file,level_010_file):
        """Fill level 1.0 file
        """
        r_source = 'source("D:/kili_data/testing/compute_level_010_file.r")'
        r_keyword = "compute_level_010_file"
        r_station_file = 'station_file="' + station_file + '",'
        r_level_010_file = 'level_010_file="' + level_010_file + '"'
        r_cmd = r_source + "\n" + \
            r_keyword + " (\n" + \
            r_station_file + "\n" + \
            r_level_010_file + ")\n"
        f = open("compute_level_010_file.r","w")
        f.write(r_cmd)
        f.close()
        print r_cmd
           
    def convert_list2string(self,list):
        """Convert list of strings to one string.
        
        Returns:
            Combined string extracted from list.
        """
        output = list[0]
        for i in range(1, len(list)):
            output = output + "," + list[i]
        return output

    def convert_floatlist2string(self,list):
        """Convert list of floats to one string.
        
        Returns:
            Combined string extracted from float value list.
        """
        output = str(list[0])
        for i in range(1, len(list)):
            output = output + "," + str(list[i])
        return output
            
    def reorder_station_coloumn_entries(self):
        """Reorder station coloumn entries to match the level 1 standards.
        """
        reorder = [1,2]
        for entry_sce in range (2,len(self.station_column_entries)):
            for entry_lce in range(0,len(self.level10_column_entries)):
                if self.level10_column_entries[entry_lce] ==  \
                    self.station_column_entries[entry_sce]:
                        reorder.append(entry_lce+1) 
        self.reorder = reorder

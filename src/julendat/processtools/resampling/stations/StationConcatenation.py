"""Process level 0250 station data to concatenated files.
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
from julendat.processtools.products.StationToLevel0050 import StationToLevel0050



class StationConcatenation:   
    """Instance for processing station data to concatenated files.
    """

    def __init__(self, filepath, config_file, level = "0290", run_mode="auto"):
        """Inits StationConcatenation. 
        
        Args:
            filepath: Full path and name of the level 0100 file
            config_file: Configuration file.
            run_mode: Running mode (auto, manual)
        """
        self.level = level
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.init_filenames(filepath)
        self.get_level_standards()
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
        self.level_0005_timezone = config.get('project','level_0005_timezone')
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
            
    def get_level_standards(self):
        """Sets format standards for level x station data files
        """
        level_standard = Level01Standards(\
            filepath=self.level0050_standards, \
            station_id=self.filenames.get_station_id())
        self.level0290_column_headers = \
            level_standard.get_level0200_column_headers()

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
            if self.level == "0290":
                self.concatenate_level0290()
            elif self.level == "0415":
                self.concatenate_level0415()
        else:
            pass

    def move_data(self):
        """Moves files.
        """
        shutil.move(self.source,self.destination)

    def concatenate_level0290(self):
        """Concatenate level 0250 station files.
        """
        #aggregation_level = "fah01"
        self.filenames.build_filename_dictionary()
        self.get_actual_filenames()
        self.init_level_0290()
        
        level_0290_file = open(self.output_filepath)
        for level_0290_lines in range (0,1):
            level_0290_header = level_0290_file.next()
        reader = csv.reader(level_0290_file,delimiter=',', \
                            quoting=csv.QUOTE_NONNUMERIC)
        level_0290_input =[]
        for row in reader:
            level_0290_input.append(row)
        level_0290_file.close()

        #Convert NA to nan
        level_0250_file = open(self.filenames.get_filepath())
        level_0250_file_conv = open(self.filenames.get_filepath() + ".con", "w")
        for inline in level_0250_file:
            level_0250_file_conv.write(inline.replace("NA", "nan"))
        level_0250_file.close()
        level_0250_file_conv.close()
        
        level_0250_file = open(self.filenames.get_filepath() + ".con")
        for level_0250_lines in range (0,1):
            temp = level_0250_file.next()
        level_0250_header = []
        for item in temp.split(","):
            level_0250_header.append(item[1:-1])
        
        reader = csv.reader(level_0250_file,delimiter=',', \
                            quoting=csv.QUOTE_NONNUMERIC)
        level_0250_input =[]
        for row in reader:
            level_0250_input.append(row)
        level_0250_file.close()

        calibration_level_index = \
            self.level0290_column_headers.index("Processlevel")
        qualtiy_flag_index = \
            self.level0290_column_headers.index("Qualityflag")

        self.reorder_station_coloumn_entries(\
                                self.level0290_column_headers, level_0250_header)
        
        level_0290_counter = 0
        out = []
        for level_0290_row in level_0290_input:
            found = False
            level_0250_counter = 0
            for level_0250_10_row in level_0250_input:
                if level_0290_input[level_0290_counter][0] == \
                    level_0250_input[level_0250_counter][0]:
                    act_out = []
                    for entry in self.reorder:
                        act_out.append(level_0250_input[level_0250_counter][entry-1])
                    act_out[calibration_level_index] = \
                        self.output_processing
                    if len(act_out) < len(self.level0290_column_headers):
                        act_out = act_out + [float('nan')]*(len(self.level0290_column_headers)-len(act_out))    
                    out.append(act_out)
                    found = True
                    break
                level_0250_counter = level_0250_counter + 1
            if found != True:
                if len(level_0290_input[level_0290_counter]) > 1:
                    out.append(level_0290_input[level_0290_counter])
                else:
                    if self.project_id == "be":
                        act_out = [level_0290_input[level_0290_counter][0], \
                                   self.level_0005_timezone, \
                                   self.filenames.get_aggregation(), \
                                   self.filenames.get_plot_id(), \
                                   'xxx', \
                                   self.filenames.get_station_id(), \
                                   self.output_processing, \
                                   'q' + '000' * (len(self.level0290_column_headers)-8)]
                    else:
                        act_out = [level_0290_input[level_0290_counter][0], \
                                   self.level_0005_timezone, \
                                   self.filenames.get_aggregation(), \
                                   self.filenames.get_plot_id()[4:], \
                                   'xxx', \
                                   self.filenames.get_station_id(), \
                                   self.output_processing, \
                                   'q' + '000' * (len(self.level0290_column_headers)-8)]

                    if len(act_out) < len(self.level0290_column_headers):
                        act_out = act_out + [float('nan')]*(len(self.level0290_column_headers)-len(act_out))    
                    out.append(act_out)
            level_0290_counter = level_0290_counter + 1


        
        outfile = open(self.output_filepath, "w")
        outfile.write(', '.join(str(i) for i in self.level0290_column_headers) + '\n')
        writer = csv.writer(outfile,delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in out:
            writer.writerow(row)
        outfile.close()       

    def concatenate_level0415(self):
        """Concatenate level 0400 station files.
        """
        #aggregation_level = "fah01"
        self.filenames.build_filename_dictionary()
        self.get_actual_filenames()
        if not os.path.isdir(self.output_path):
            os.makedirs(self.output_path)
        
        input_file = open(self.filenames.get_filepath())
        if os.path.isfile(self.output_filepath) != True:
            output_file = open(self.output_filepath, 'w')
            for inline in input_file:
                output_file.write(inline.replace(',"0400",', ',"0415",'))
            output_file.close()
        else:
            input_file.next()
            output_file = open(self.output_filepath, 'a')
            for inline in input_file:
                output_file.write(inline.replace(',"0400",', ',"0415",'))
            output_file.close()
                
    def get_actual_filenames(self):
        """Get actual output filenames and metadata
        """
        if self.level == "0290":
            self.output_filepath = self.filenames.get_filename_dictionary()\
                          ["level_0290_ascii-filepath"]
            self.output_path = self.filenames.get_filename_dictionary()\
                                 ["level_0290_ascii-path"]
            self.output_startdatetime = self.filenames.get_filename_dictionary()\
                          ['level_0290_startdatetime']
            self.output_enddatetime = self.filenames.get_filename_dictionary()\
                          ['level_0290_enddatetime']
            self.output_timestep = '3600'
            self.output_processing = self.filenames.get_filename_dictionary()\
                        ['level_0290_processing']

        elif self.level == "0415":
            self.output_filepath = self.filenames.get_filename_dictionary()\
                          ["level_0415_ascii-filepath"]
            self.output_path = self.filenames.get_filename_dictionary()\
                                 ["level_0415_ascii-path"]
            self.output_startdatetime = self.filenames.get_filename_dictionary()\
                          ['level_0415_startdatetime']
            self.output_enddatetime = self.filenames.get_filename_dictionary()\
                          ['level_0415_enddatetime']
            self.output_timestep = '3600'
            self.output_processing = self.filenames.get_filename_dictionary()\
                        ['level_0415_processing']

    def init_level_0290(self):
        """Init level 0290 file
        """
        if os.path.isfile(self.output_filepath) != True:
            if not os.path.isdir(self.output_path):
                os.makedirs(self.output_path)

            r_source = 'source("' + self.r_filepath + os.sep + \
                'InitLevel050File.R")'
            r_keyword = "init_level_010_file"
            r_ofp = 'outpath="' + self.output_filepath + '",'
            r_st = 'start_time="' + self.output_startdatetime + '",'
            r_et = 'end_time="' + self.output_enddatetime + '",'
            r_ts = 'time_step= ' + self.output_timestep
            r_cmd = r_source + "\n" + \
                    r_keyword + " (\n" + \
                    r_ofp + "\n" + \
                    r_st + "\n" + \
                    r_et + "\n" + \
                    r_ts + ")\n"
            r_script = "il0050.rscript" 
            f = open(r_script,"w")
            f.write(r_cmd)
            f.close()
            r_cmd = "R CMD BATCH " + r_script + " " + r_script + ".log"
            os.system(r_cmd)

    def reorder_station_coloumn_entries(self,input_headers,output_headers):
        """Reorder station column entries to match the level 1 standards.
        """
        reorder = []
        for entry_sce in range (0,len(input_headers)):
            match = False
            for entry_lce in range(0,len(output_headers)):
                if string.strip(output_headers[entry_lce]) ==  \
                    string.strip(input_headers[entry_sce]):
                        reorder.append(entry_lce+1)
                        match = True
            if match == False:
                reorder.append(-1)
        self.reorder = reorder
        print "Reorder of input columns:    ", reorder

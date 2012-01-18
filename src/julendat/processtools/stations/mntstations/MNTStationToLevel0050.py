"""Convert MayerNT level 0 logger data to level 1.
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

__author__ = "Thomas Nauss <nausst@googlemail.com>, Insa Otte, Falk Haensel"
__version__ = "2012-01-17"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import sys
import csv
import os
import string
import ConfigParser
from julendat.processtools import time_utilities
from julendat.filetools.stations.mntstations.MNTStationDataFile import \
    MNTStationDataFile
import shutil
import time
import datetime
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.metadatatools.stations.Level01Standards import Level01Standards


class MNTStationToLevel0050:   
    """Instance for converting MayerNT logger level 0 to level 1data.
    """

    def __init__(self, filepath, config_file,run_mode="auto"):
        """Inits MNTStationToLevel0050. 
        
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
        self.logger_time_zone = config.get('logger', 'logger_time_zone')
        self.tl_data_path = config.get('repository', 'toplevel_processing_plots_path')
        self.station_inventory = config.get('inventory','station_inventory')
        self.project_id = config.get('project','project_id')
        self.level_0005_timezone = config.get('project','level_0005_timezone')
        self.level0050_standards = config.get('general','level0050_standards')
        self.r_filepath = config.get('general','r_filepath')

    def init_filenames(self, filepath):
        """Initializes MNT station data file.
        
        Args:
            filepath: Full path and name of the level 0 file
        """
        try:
            self.filenames = StationDataFilePath(filepath=filepath, \
                                toplevel_path=self.tl_data_path, \
                                logger_time_zone=self.logger_time_zone, \
                                level_0005_time_zone=self.level_0005_timezone)
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

    def move_data(self):
        """Moves files.
        """
        shutil.move(self.source,self.destination)

    def main(self):
        """Processes level 0000 station files to level 0050.
        """
        self.init_level_0000_ascii_file()
        if self.get_run_flag():
            self.get_station_inventory_information()
        
        if self.get_run_flag():
            self.process_level_0005()

        if self.get_run_flag():
            self.process_level_0050()
        
        print "...finished."

    def init_level_0000_ascii_file(self):
        """Initializes level 000 ascii file.
        """
        try:
            self.level_0000_ascii_file = MNTStationDataFile(filepath= \
                self.filenames.get_filename_dictionary()[\
                "level_0000_ascii-filepath"])
            self.run_flag = self.level_0000_ascii_file.get_file_exists()
        except:
            raise Exception, "Can not initialize level 0000 ascii file"
            print "Error: level 0000 ascii file could not be read"
            self.run_flag = False

    def get_station_inventory_information(self):
        """Get meta-information from station inventory.
        """
        inventory = StationInventory(filepath=self.station_inventory, \
            logger_start_time = self.level_0000_ascii_file.get_start_datetime(), \
            logger_end_time = self.level_0000_ascii_file.get_end_datetime(), \
            plot_id = self.filenames.get_plot_id())
        if inventory.found_station_inventory != True:
            raise Exception, "Serial number has not been found in station inventory"
        self.level_0000_ascii_file.set_header_line(inventory.get_header_line())
        self.level_0000_ascii_file.set_first_data_line(inventory.get_first_data_line())
        self.calibration_coefficients_headers = \
            inventory.get_calibration_coefficients_headers()
        self.calibration_coefficients = inventory.get_calibration_coefficients()
        if self.filenames.get_raw_plot_id() != inventory.get_plot_id():
            print "Error: plot-id does not match"
            print "File:       ", self.filenames.get_raw_plot_id()
            print "Inventory:, ", inventory.get_plot_id()
            raise Exception, "Error: plot-id does not match."
            self.run_flag = False
            
        elif self.filenames.get_station_id() != inventory.get_station_id():
            print "Error: station-id does not match"
            self.run_flag = False
            raise Exception, "Error: station-id does not match."

    def process_level_0005(self):
        """Process level 0000 to level 0005 data set
        """
        self.get_level0005_standards()
        self.rename_level0000_headers()

        self.reorder_station_coloumn_entries(\
            self.level_0000_ascii_file.get_column_headers(), \
            self.level0005_column_headers)
        print "Reorder of input columns:    ", self.reorder

        self.write_level_0005()

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

        if self.project_id == "be":
            sp_id = self.filenames.get_plot_id()
            if sp_id != "000HEG06" and \
               sp_id != '000SEG39' and \
               sp_id != '000SEG39':
                sp_id = sp_id[:-2] + "xx" 
            soil_parameter_headers = \
                level0005_standard.get_level0000_soil_headers(sp_id)
            self.level0000_column_headers = self.level0000_column_headers + \
                soil_parameter_headers

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

    def rename_level0000_headers(self):
        """Rename level 0000 headers to 0005+ convention
        """
        ascii_headers = self.level_0000_ascii_file.get_column_headers()
        print "Original level 0000 headers: ", ascii_headers
        for col_old in range(0, len(ascii_headers)):
            for col_new in self.level0000_column_headers:
                if col_new[0].rsplit(" ")[0] == str.lower(ascii_headers[col_old].rsplit(" ")[0]):
                    if str.lower(ascii_headers[col_old].rsplit(" ")[0]) != "temp.":
                        ascii_headers[col_old] = col_new[1]
                    else:
                        if col_new[0].rsplit(" ")[1] == str.lower(ascii_headers[col_old].rsplit(" ")[1]):
                            ascii_headers[col_old] = col_new[1]
        
        if self.filenames.get_station_id().find("wxt") != -1:
            if self.level_0000_ascii_file.get_start_datetime().year == 2011 and\
               self.level_0000_ascii_file.get_start_datetime().month <= 8 and \
               self.level_0000_ascii_file.get_start_datetime().day <= 20:
                ascii_headers[8] = 'SWDR_300_U'
                ascii_headers[9] = 'SWUR_300_U'
                ascii_headers[10] = 'LWDR_300_U'
                ascii_headers[11] = 'LWUR_300_U'
            else:
                ascii_headers[8] = 'LWDR_300_U'
                ascii_headers[9] = 'LWUR_300_U'
                ascii_headers[10] = 'SWDR_300_U'
                ascii_headers[11] = 'SWUR_300_U'

        self.level_0000_ascii_file.set_column_headers(ascii_headers)
        print "New level 0000 headers:      ", ascii_headers

    def write_level_0005(self):
        """Write level 0005 dataset.
        """
        self.level_0000_data = self.level_0000_ascii_file.get_data()
        output=[]
        for row in self.level_0000_data:
            if len(row[0]) == 16:
                act_time = time_utilities.convert_timezone( \
                    datetime.datetime.strptime(row[0],"%d.%m.%Y %H:%M"), \
                    self.level_0005_timezone).strftime("%Y-%m-%d %H:%M:%S")
            else:
                act_time = time_utilities.convert_timezone( \
                    datetime.datetime.strptime(row[0],"%d.%m.%Y %H:%M:%S"), \
                    self.level_0005_timezone).strftime("%Y-%m-%d %H:%M:%S")
            try:
                act_out=      [act_time, \
                               self.level_0005_timezone, \
                               self.filenames.get_aggregation(), \
                               self.filenames.get_plot_id(), \
                               'xxx', \
                               self.filenames.get_station_id(), \
                               self.filenames.get_filename_dictionary()['level_0005_process_level'], \
                               self.filenames.get_filename_dictionary()['level_0005_quality']]
                for i in range(9, max(self.reorder)+1):
                    try:
                        index =  self.reorder.index(i)
                        act_out = act_out + [float(row[index].replace(',','.'))]
                    except:
                        act_out = act_out + [float('nan')]
                output.append(act_out)
            except:
                continue

        output_path = self.filenames.get_filename_dictionary()\
                      ["level_0005_ascii-path"]
        if not os.path.isdir(output_path):
            os.makedirs(output_path)

        outfile = open(self.filenames.get_filename_dictionary()\
                       ["level_0005_ascii-filepath"],"w")
        
        outfile.write(', '.join(str(i) for i in self.level0005_column_headers) + '\n')
        writer = csv.writer(outfile,delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in output:
            writer.writerow(row)
        outfile.close()

            
    def process_level_0050(self):
        """Compute level 1.0 station data sets
        """
        self.get_level0050_standards()
        self.reorder_station_coloumn_entries(\
            self.level0005_column_headers, \
            self.level0050_column_headers)
        
        filenumber = len(self.filenames.get_filename_dictionary()\
                         ["level_0050_ascii-filepath"])

        for act_file in range(0, filenumber):
            self.act_level_0050_filepath = \
                self.filenames.get_filename_dictionary()\
                ["level_0050_ascii-filepath"][act_file]        
            self.act_level_0050_path = \
                self.filenames.get_filename_dictionary()\
                ["level_0050_ascii-path"][act_file]
            self.act_level_0050_start_time_isostr = \
                self.filenames.get_filename_dictionary()\
                ['level_0050_start_time_isostr'][act_file]
            self.act_level_0050_end_time_isostr = \
                self.filenames.get_filename_dictionary()\
                ['level_0050_end_time_isostr'][act_file]
            self.init_path(self.act_level_0050_path)        
            self.init_level_0050()   
            self.write_level_0050()

    def get_level0050_standards(self):
        """Sets format standards for level 1 station data files
        """
        level0050_standard = Level01Standards(\
            filepath=self.level0050_standards, \
            station_id=self.filenames.get_station_id())
        self.level0005_column_headers = \
            level0050_standard.get_level0005_column_headers()
        self.level0050_column_headers = \
            level0050_standard.get_level0050_column_headers()
                    
    def init_path(self, path):
        """Init path
        
        Args:
            path: Path
        """
        if not os.path.isdir(path):
            os.makedirs(path)
        
    def init_level_0050(self):
        """Init level 1.0 file
        """
        if os.path.isfile(self.act_level_0050_filepath) != True:
            r_source = 'source("' + self.r_filepath + os.sep + \
                'InitLevel050File.R")'
            r_keyword = "init_level_010_file"
            r_ofp = 'outpath="' + self.act_level_0050_filepath + '",'
            r_st = 'start_time="' + self.act_level_0050_start_time_isostr + '",'
            r_et = 'end_time="' + self.act_level_0050_end_time_isostr + '",'
            r_ts = 'time_step=' + self.filenames.get_time_step_delta_str() + ''
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
            print r_cmd
            os.system(r_cmd)

    def write_level_0050(self):
        """Fill level 0050 file
        """
        station_file = open( \
            self.filenames.get_filename_dictionary()["level_0005_ascii-filepath"])
        for header_lines in range (0,1):
            station_header = station_file.next()
        reader = csv.reader(station_file,delimiter=',', \
                            quoting=csv.QUOTE_NONNUMERIC)
        station_input =[]
        for row in reader:
            station_input.append(row)
        station_file.close()

        level_010_file = open(self.act_level_0050_filepath)
        for header_lines in range (0,1):
            level_010_header = level_010_file.next()
        reader = csv.reader(level_010_file,delimiter=',', \
                            quoting=csv.QUOTE_NONNUMERIC)
        level_10_input =[]
        for row in reader:
            level_10_input.append(row)
        level_010_file.close()

        process_level_index = self.level0005_column_headers.index("Processlevel")
        qualtiy_flag_index = self.level0005_column_headers.index("Qualityflag")

        level_10_counter = 0
        out = []
        for level_10_row in level_10_input:
            found = False
            station_counter = 0
            for station_10_row in station_input:
                if level_10_input[level_10_counter][0] == station_input[station_counter][0]:
                    
                    act_out = station_input[station_counter][0:8]
                    act_out[process_level_index] = self.filenames.get_filename_dictionary()['level_0050_process_level']
                    act_out[qualtiy_flag_index] = self.filenames.get_filename_dictionary()['level_0050_quality']
                    for i in range(9, max(self.reorder)+1):
                        try:
                            index =  self.reorder.index(i)
                            act_out = act_out + [float(station_input[station_counter][index])]
                        except:
                            act_out = act_out + [float('nan')]
                    out.append(act_out)
                    #out.append(station_input[station_counter])
                    found = True
                    break
                station_counter = station_counter + 1
            if found != True:
                out.append(level_10_input[level_10_counter])
            level_10_counter = level_10_counter + 1


        outfile = open(self.act_level_0050_filepath,"w")
        outfile.write(', '.join(str(i) for i in self.level0050_column_headers) + '\n')
        writer = csv.writer(outfile,delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in out:
            writer.writerow(row)
        outfile.close()

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
            


    def check_wxt(self):
        """Check level 0 wxt logger file for comment lines within the data rows.
        """
        original_file = open(self.filenames.get_filename_dictionary()\
                            ["level_0000_ascii-filepath"],'r')
        target_file = open(\
            self.filenames.get_filename_dictionary()["temp_filepath"],'w')
        row_counter = 0
        
        for row in original_file:
            if row_counter < 7:
                target_file.write(row)
                row_counter = row_counter + 1
            try:
                time.strptime(row[0:8], "%d.%m.%y")
                target_file.write(row)
            except:
                continue

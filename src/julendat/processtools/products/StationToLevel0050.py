"""Convert D&K as well as UI level 0000 logger data to level 0050.
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
__version__ = "2013-01-13"
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


class StationToLevel0050:   
    """Instance for converting logger level 0000 to level 0050 data.
    """

    def __init__(self, filepath, config_file,run_mode="auto"):
        """Inits StationToLevel0050. 
        
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
        self.station_entries = config.get('logger', 'station_entries')
        self.logger_time_zone = config.get('logger', 'logger_time_zone')
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
            if "tfi" in filepath:
                self.logger_time_zone = self.level_0005_timezone
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
            self.calibration_level_0005()
        if self.get_run_flag():
            self.calibration_level_0050()
        
        print "...finished."

    def init_level_0000_ascii_file(self):
        """Initializes level 000 ascii file.
        """
        try:
            self.level_0000_ascii_file = DKStationDataFile(filepath= \
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
            serial_number=self.level_0000_ascii_file.get_serial_number())
        if inventory.found_station_inventory != True:
            raise Exception, "Serial number has not been found in station inventory"
        self.level_0000_ascii_file.set_header_line(inventory.get_header_line())
        self.level_0000_ascii_file.set_first_data_line(inventory.get_first_data_line())
        self.calibration_coefficients_headers = \
            inventory.get_calibration_coefficients_headers()
        self.calibration_coefficients = inventory.get_calibration_coefficients()
        self.module_serial_numbers_headers = \
            inventory.get_module_serial_numbers_headers()
        self.module_serial_numbers = inventory.get_module_serial_numbers()
        self.module_pu2_metadata = inventory.get_module_pu2_metadata()
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

    def calibration_level_0005(self):
        """Process level 0000 to level 0005 data set
        """
        self.get_level0005_standards()
        self.rename_level0000_headers()
        
        self.calibrate_level_0005()
        
        self.convert_P_container_RT()

        self.reorder_station_coloumn_entries(\
            self.level_0000_ascii_file.get_column_headers(), \
            self.level0005_column_headers)
        
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
        self.level0050_column_headers = \
            level0005_standard.get_level0050_column_headers()

        
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
        
        if self.filenames.get_station_id().find("pu2") != -1:
            self.rename_pu2_sensor_headers()

        self.level_0000_ascii_file.set_column_headers(ascii_headers)

        if self.filenames.get_station_id().find("rad") != -1:
            self.rename_rad_sensor_headers()
        print self.level0005_column_headers

        print "New level 0000 headers:      ", \
            self.level_0000_ascii_file.get_column_headers()

    def rename_pu2_sensor_headers(self):
        """Rename headers of pu2 sensors (multiple "Impulse" entries)
        """
        level_0000_column_headers = \
            self.level_0000_ascii_file.get_column_headers()
        level_0000_column_headers[2] = self.module_pu2_metadata [2]
        level_0000_column_headers[3] = self.module_pu2_metadata [3]
        self.level_0000_ascii_file.set_column_headers(level_0000_column_headers)
                
    def rename_rad_sensor_headers(self):
        """Rename headers of rad sensors (multiple "Voltage" entries)
        """

        headers  = ['SERIAL_PYR01', 'SERIAL_PYR02', \
                      'SERIAL_PAR01', 'SERIAL_PAR02']
        for header in headers:
            header_index = self.module_serial_numbers_headers.index(header)
            module_serial_number = self.module_serial_numbers[header_index]
            if module_serial_number != 'NaN':
                if int(module_serial_number) <= 11:
                    sensor_type = 'par_'
                elif int(module_serial_number) >= 12:
                    sensor_type = 'swdr_'

                level_0000_column_headers = self.level_0000_ascii_file.get_column_headers()
                level0000_column_headers_index = level_0000_column_headers.index('radx')
                level_0000_column_headers[level0000_column_headers_index] = sensor_type + str(int(module_serial_number)).zfill(2)

                #level0005_column_headers_index = self.level0005_column_headers.index('radx')
                #self.level0005_column_headers[level0005_column_headers_index] = sensor_type + str(int(module_serial_number)).zfill(2)

                #level0050_column_headers_index = self.level0050_column_headers.index('radx')
                #self.level0050_column_headers[level0050_column_headers_index] = sensor_type + str(int(module_serial_number)).zfill(2)

        self.level_0000_ascii_file.set_column_headers(level_0000_column_headers)


    def calibrate_level_0005(self):
        """Calibrate level 0000 datasets
        """
        if self.filenames.get_station_id().find("wxt") != -1:
            
            parameters = ["SWDR_300","SWUR_300","LWDR_300","LWUR_300"]
            self.level_0000_data = []
            for row in self.level_0000_ascii_file.get_data():
                act_row = row
                for parameter in parameters:
                    try:
                        raw_value_index = self.level_0000_ascii_file.get_column_headers().index(parameter + "_U")
                        raw_value = float(row[raw_value_index])
                        calib_coefficient_index = self.calibration_coefficients_headers.index(self.filenames.get_station_id()[-3:] + "_" + parameter)
                        calib_coefficient = float(self.calibration_coefficients[calib_coefficient_index])
                        if parameter[0:2] == "SW": 
                            param_value = raw_value * 1000.0 / calib_coefficient
                        elif parameter[0:2] == "LW":
                            t_cnr_index = self.level_0000_ascii_file.get_column_headers().index("T_CNR")
                            t_cnr = float(row[t_cnr_index])
                            param_value = raw_value * 1000.0 / calib_coefficient + \
                            5.672E-08 * (t_cnr + 273.15)**4
                        act_row = act_row + [param_value]
                    except:
                        continue
                self.level_0000_data.append(act_row)

            new_header = self.level_0000_ascii_file.get_column_headers() + parameters
            self.level_0000_ascii_file.set_column_headers(new_header)

        elif self.filenames.get_station_id().find("pu1") != -1:
            parameters = ["P_RT_NRT"]
            self.level_0000_data = []
            for row in self.level_0000_ascii_file.get_data():
                act_row = row
                for parameter in parameters:
                    try:
                        raw_value_index = self.level_0000_ascii_file.get_column_headers().index(parameter + "_I")
                        raw_value = float(row[raw_value_index])
                        calib_coefficient_index = self.calibration_coefficients_headers.index(self.filenames.get_station_id()[-3:] + "_" + parameter)
                        calib_coefficient = float(self.calibration_coefficients[calib_coefficient_index])
                        param_value = raw_value * calib_coefficient
                        act_row = act_row + [param_value]
                    except:
                        continue
                self.level_0000_data.append(act_row)

            new_header = self.level_0000_ascii_file.get_column_headers() + parameters
            self.level_0000_ascii_file.set_column_headers(new_header)

        elif self.filenames.get_station_id().find("pu2") != -1:
            parameters = [self.module_pu2_metadata [2][:-2], \
                          self.module_pu2_metadata [3][:-2]]
            self.level_0000_data = []
            for row in self.level_0000_ascii_file.get_data():
                act_row = row
                counter = 0
                for parameter in parameters:
                    counter = counter + 1
                    try:
                        raw_value_index = self.level_0000_ascii_file.get_column_headers().index(parameter + "_I")
                        raw_value = float(row[raw_value_index])
                        calib_coefficient_index = self.calibration_coefficients_headers.index(self.filenames.get_station_id()[-3:] + "_" + str(counter))
                        calib_coefficient = float(self.calibration_coefficients[calib_coefficient_index])
                        param_value = raw_value * calib_coefficient
                        act_row = act_row + [param_value]
                    except:
                        continue
                self.level_0000_data.append(act_row)

            new_header = self.level_0000_ascii_file.get_column_headers() + parameters
            self.level_0000_ascii_file.set_column_headers(new_header)

        elif self.filenames.get_station_id().find("rad") != -1:
            templates  = ['par_', 'swdr_']
            print self.level_0000_ascii_file.get_column_headers()
            parameters = []
            for entry in self.level_0000_ascii_file.get_column_headers():
                for template in templates:
                    if entry.startswith(template):   
                        parameters.append(entry)
                    
            self.level_0000_data = []
            for row in self.level_0000_ascii_file.get_data():
                act_row = row
                for parameter in parameters:
                    try:
                        raw_value_index = self.level_0000_ascii_file.get_column_headers().index(parameter)
                        calib_coefficient = float(10)
                        row[raw_value_index] = float(row[raw_value_index]) * calib_coefficient
                    except:
                        continue
                self.level_0000_data.append(act_row)
        
        elif self.filenames.get_station_id().find("tfi") != -1:
            templates  = ['B_', 'Fog', 'Rainfall']
            coefficients = {'B_': 'pu1_P_RT_NRT', \
                            'Ra': 'pu2_1', 'Fo': 'pu2_2'}
            parameters = []
            for entry in self.level_0000_ascii_file.get_column_headers():
                for template in templates:
                    
                    if entry.strip().startswith(template):   
                        parameters.append(entry)
            self.level_0000_data = []
            for row in self.level_0000_ascii_file.get_data():
                act_row = row
                for parameter in parameters:
                    act_coefficient = coefficients[parameter.strip()[0:2]]
                    try:
                        raw_value_index = self.level_0000_ascii_file.get_column_headers().index(parameter)
                        raw_value = float(row[raw_value_index])
                        calib_coefficient_index = self.calibration_coefficients_headers.index(act_coefficient)
                        calib_coefficient = float(self.calibration_coefficients[calib_coefficient_index])
                        param_value = raw_value * calib_coefficient
                        act_row[raw_value_index] = param_value
                    except:
                        continue
                self.level_0000_data.append(act_row)


        elif self.filenames.get_station_id().find("gp1") != -1:
            parameters = ["WD","WV"]
            calib_coefficient_index_wd = self.calibration_coefficients_headers.index('pu2_1')
            calib_coefficient_index_wv = self.calibration_coefficients_headers.index('pu2_2')
            calib_coefficient_wd = float(self.calibration_coefficients[calib_coefficient_index_wd])
            calib_coefficient_wv = float(self.calibration_coefficients[calib_coefficient_index_wv])
            self.level_0000_data = []
            for row in self.level_0000_ascii_file.get_data():
                act_row = row
                for parameter in parameters:
                    try:
                        if parameter == "WD": 
                            raw_value_index = self.level_0000_ascii_file.get_column_headers().index(parameter + "_R")
                            raw_value = float(row[raw_value_index])
                            param_value = raw_value * calib_coefficient_wd
                        elif parameter == "WV":
                            raw_value_index = self.level_0000_ascii_file.get_column_headers().index(parameter + "_I")
                            raw_value = float(row[raw_value_index])
                            param_value = raw_value * calib_coefficient_wv
                        act_row = act_row + [param_value]
                    except:
                        continue
                self.level_0000_data.append(act_row)

            new_header = self.level_0000_ascii_file.get_column_headers() + parameters
            self.level_0000_ascii_file.set_column_headers(new_header)        

        else:
            self.level_0000_data = self.level_0000_ascii_file.get_data()

    def convert_P_container_RT(self):
        """Convert precipitation sums of wxt to precipitation per time slot
        """
        if self.filenames.get_station_id().find("wxt") != -1:
            parameters = ["P_container_RT","P_RT_NRT"]
            for i in range(1,len(self.level_0000_data)):
                try:
                    p_container_index = self.level_0000_ascii_file.get_column_headers().index(parameters[0])
                    prev_p_cont = self.level_0000_data[i-1][p_container_index]
                    act_p_cont = self.level_0000_data[i][p_container_index]
                    self.level_0000_data[i] = self.level_0000_data[i] + [max(abs(float(act_p_cont) - float(prev_p_cont)),0.0)]
            
                except:
                    continue
            new_header = self.level_0000_ascii_file.get_column_headers() + [parameters[1]]
            self.level_0000_ascii_file.set_column_headers(new_header)

    def write_level_0005(self):
        """Write level 0005 dataset.
        """
        output=[]
        for row in self.level_0000_data:
            try:
                if "tfi" in self.filenames.get_station_id():
                    act_time = time_utilities.convert_timezone( \
                        datetime.datetime.strptime(row[0]+row[1],\
                                                   "%Y-%m-%d %H:%M:%S"), \
                        self.level_0005_timezone).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    act_time = time_utilities.convert_timezone( \
                        datetime.datetime.strptime(row[0]+row[1],\
                                                   "%d.%m.%y%H:%M:%S"), \
                        self.level_0005_timezone).strftime("%Y-%m-%d %H:%M:%S")

                act_out=      [act_time, \
                               self.level_0005_timezone, \
                               self.filenames.get_aggregation(), \
                               self.filenames.get_plot_id()[4:], \
                               'xxx', \
                               self.filenames.get_station_id(), \
                               #self.filenames.get_filename_dictionary()['level_0005_calibration_level'], \
                               self.filenames.get_filename_dictionary()['level_0005_processing'], \
                               'q' + '000' * (len(self.level0005_column_headers)-8)]
                for i in range(9, max(self.reorder)+1):
                    try:
                        index =  self.reorder.index(i)
                        act_out = act_out + [float(row[index])]
                    except:
                        act_out = act_out + [float('nan')]
                
                if len(act_out) < len(self.level0005_column_headers):
                    act_out = act_out + [float('nan')]*(len(self.level0005_column_headers)-len(act_out))
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

            
    def calibration_level_0050(self):
        """Compute level 1.0 station data sets
        """
        self.get_level0050_standards()
        print "Level 0005 headers:          ", self.level0005_column_headers
        print "Level 0050 headers:          ", self.level0050_column_headers
        self.reorder_station_coloumn_entries(\
            self.level0005_column_headers, \
            self.level0050_column_headers)
        print "Reorder of input columns:    ", self.reorder

        
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

        calibration_level_index = self.level0005_column_headers.index("Processlevel")
        qualtiy_flag_index = self.level0005_column_headers.index("Qualityflag")

        level_10_counter = 0
        out = []
        for level_10_row in level_10_input:
            found = False
            station_counter = 0
            for station_10_row in station_input:
                if level_10_input[level_10_counter][0] == station_input[station_counter][0]:
                    
                    act_out = station_input[station_counter][0:8]
                    #act_out[calibration_level_index] = self.filenames.get_filename_dictionary()['level_0050_calibration_level']
                    act_out[calibration_level_index] = self.filenames.get_filename_dictionary()['level_0050_processing']
                    act_out[qualtiy_flag_index] = "q" + "000" * (len(self.level0050_column_headers)-8)
                    for i in range(9, max(self.reorder)+1):
                        try:
                            index =  self.reorder.index(i)
                            act_out = act_out + [float(station_input[station_counter][index])]
                        except:
                            act_out = act_out + [float('nan')]
                    
                    if len(act_out) < len(self.level0050_column_headers):
                        act_out = act_out + [float('nan')]*(len(self.level0050_column_headers)-len(act_out))    
                    out.append(act_out)
                    #out.append(station_input[station_counter])
                    found = True
                    break
                station_counter = station_counter + 1
            if found != True:
                if len(level_10_input[level_10_counter]) > 1:
                    out.append(level_10_input[level_10_counter])
                else:
                    act_out = [level_10_input[level_10_counter][0], \
                          self.level_0005_timezone, \
                          self.filenames.get_aggregation(), \
                               self.filenames.get_plot_id()[4:], \
                               'xxx', \
                               self.filenames.get_station_id(), \
                               self.filenames.get_filename_dictionary()['level_0050_processing'], \
                               'q' + '000' * (len(self.level0005_column_headers)-8)]
                    if len(act_out) < len(self.level0050_column_headers):
                        act_out = act_out + [float('nan')]*(len(self.level0050_column_headers)-len(act_out))    
                    out.append(act_out)
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

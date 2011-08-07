'''Handle data files from Driesen & Kern sensor/logger combinations.
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
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2010-08-07"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import datetime
import linecache
import os
import string
import time
from julendat.filetools.stations.StationDataFile import StationDataFile


class DKStationDataFile(object):
    """Class for handling Driesen & Kern station data (sensor/logger).

    This instance can be used to handle Driesn & Kern station data which is a
    defined combination of one or more sensors and one logger.
    """

    def __init__(self,path_to_file):
        '''Inits DKStationDataFile.
        
        Based on the initial binary logger data file instance, the associated
        ASCII file data object will be initialized. In addition, the serial
        number of the logger and the time range of the data file will be
        extracted.
        
        Args:
            path_to_file: Full path and name of binary logger file.
        '''       
        
        self.set_binary_file(path_to_file)
        self.set_ascii_file()
        self.set_serial_number()
        self.set_time_range()

    def set_binary_file(self,path_to_file):
        '''Creates data file instance of the binary logger file.
        
        Args:
            path_to_file: Full path and name of binary logger file.
        '''
        self.bin_file = StationDataFile(path_to_file=path_to_file)

    def get_binary_file(self):
        '''Gets data file instance of the binary logger file.
        
        Returns:
            Data file object of the initially downloaded logger binary file.
        '''
        return self.bin_file

    def set_ascii_file(self):
        '''Creates data file instance of the ascii logger file.
        '''
        ascii_file_exsists = False
        ascii_file = self.bin_file.get_file()[:-3] + "asc"
        if os.path.isfile(ascii_file):
            ascii_file_exsists = True
        if ascii_file_exsists != True:
            ascii_file = self.bin_file.get_file()[:-3] + "ASC"
            if os.path.isfile(ascii_file):
                ascii_file_exsists = True
        if ascii_file_exsists == True:
            self.ascii_file = StationDataFile(path_to_file=ascii_file)
        else:
            ascii_file_exsists = False
            self.ascii_file = None
        
        self.ascii_file_exists = ascii_file_exsists

    def get_ascii_file(self):
        '''Gets ascii logger file instance.
        
        Returns:
            Data file object of the ascii logger file.
        '''
        return self.ascii_file

    def get_ascii_file_exists(self):
        '''Gets information if ASCII file object exists (true/false).

        Returns:
            Flag (true/false) if ascii logger file exists.
        '''
        return self.ascii_file_exists

    def set_serial_number(self):
        '''Sets station serial number extracted from ascii logger file.
        '''
        line = linecache.getline(self.ascii_file.get_file(), 2)
        self.serial_number =  string.strip(line.partition(':')[2])
    
    def get_serial_number(self):
        '''Gets station serial number extracted from ascii logger file.

        Returns:
            Serial number of the logger.
        '''
        return self.serial_number
    
    def set_time_range(self):
        '''Sets time range extracted from ascii logger file.
        '''
        if self.ascii_file_exists == True:
            self.start_time = None
            self.end_time = None
            time_interval = False
            logger_data = open(self.ascii_file.get_file(),'r')
            for line in logger_data:
                if line[2] == "." and line[5] == ".":
                    self.end_time = time.strftime("%Y%m%d%H%M",
                                    time.strptime(\
                                    string.strip(line.split('\t')[0]) +\
                                    string.strip(line.split('\t')[1]), \
                                    "%d.%m.%y%H:%M:%S"))
                    if time_interval == True:
                        self.time_step = str(datetime.datetime.strptime(\
                                        self.end_time,"%Y%m%d%H%M") -\
                                        datetime.datetime.strptime(\
                                        self.start_time,"%Y%m%d%H%M"))[2:4]
                        time_interval = False
                    if self.start_time == None:
                        self.start_time = time.strftime("%Y%m%d%H%M",
                                          time.strptime(
                                          string.strip(line.split('\t')[0]) + \
                                          string.strip(line.split('\t')[1]), \
                                          "%d.%m.%y%H:%M:%S"))
                        time_interval = True

    def get_time_range(self):
        '''Gets time range extracted from ascii logger file.

        Returns:
            Time range of the logger file in the following order:
                start time
                end time
                time step in minutes
        '''
        return self.start_time, self.end_time, self.time_step

    def get_start_time(self):
        '''Gets start time extracted from ascii logger file.

        Returns:
            Start time of the logger file.
        '''
        return self.start_time

    def get_end_time(self):
        '''Gets end time  extracted from ascii logger file.

        Returns:
            End time of the logger file.
        '''
        return self.end_time

    def get_time_interval(self):
        '''Gets time interval extracted from ascii logger file.

        Returns:
            Time interval in minutes of the logger file.
        '''
        return self.time_interval

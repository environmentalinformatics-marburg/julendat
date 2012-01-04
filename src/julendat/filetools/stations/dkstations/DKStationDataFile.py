"""Handle data files from Driesen & Kern sensor/logger combinations.
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

import csv
from datetime import datetime
import linecache
import string
import time
from julendat.filetools.stations.StationDataFile import StationDataFile
from julendat.processtools.TimeInterval import TimeInterval

class DKStationDataFile(StationDataFile):
    """Instance for handling Driesen & Kern station data (sensor/logger).

    This instance can be used to handle Driesn & Kern station data which is a
    defined combination of one or more sensors and one logger.
    """

    def __init__(self, filepath, io_access="r"):
        """Inits DKStationDataFile.
        
        Based on the initial binary logger data file instance, the associated
        ASCII file data object will be initialized. In addition, the serial
        number of the logger and the time range of the data file will be
        extracted.
        
        Args (from class DataFile):
            filepath: Full path and name of the data file
            io_asccess: IO access (r-read,w-write,rw-read/write)
        """       
        
        StationDataFile.__init__(self, filepath, io_access="r")
        
        self.check_filetype()

    def check_filetype(self):
        """Sets filetype of the logger file (binary/ascii).
        """
        if self.get_extension() == 'bin' or \
            self.get_extension() == 'BIN':
            filetype = 'bin'
        elif self.get_extension() == 'asc' or \
            self.get_extension() == 'ASC':
            filetype = 'ascii'
        self.set_filetype(filetype)

    def set_serial_number_ascii(self):
        """Sets station serial number extracted from ascii logger file.
        """
        line = linecache.getline(self.get_filepath(), 2)
        self.set_serial_number(string.strip(line.partition(':')[2]))

    def set_time_range_ascii(self):
        """Sets time range extracted from ascii logger file.
        """
        start_datetime = None
        end_datetime = None
        compute_time_interval = False
        logger_data = open(self.get_filepath(),'r')
        line_counter = 0
        
        for line in logger_data:
            line_counter = line_counter + 1
            if line[2] == "." and line[5] == ".":
                end_datetime = datetime.strptime(\
                           string.strip(line.split('\t')[0]) +\
                           string.strip(line.split('\t')[1]), \
                           "%d.%m.%y%H:%M:%S")
                if compute_time_interval == True:
                    #time_step_delta = end_datetime - start_datetime
                    time_step_delta = TimeInterval(start_datetime, \
                                                     end_datetime)
                    compute_time_interval = False
                if start_datetime == None:
                    line_skip = line_counter -1
                    start_datetime = datetime.strptime(
                                 string.strip(line.split('\t')[0]) + \
                                 string.strip(line.split('\t')[1]), \
                                 "%d.%m.%y%H:%M:%S")
                    compute_time_interval = True
        """
                end_time = time.strftime("%Y%m%d%H%M",
                           time.strptime(\
                           string.strip(line.split('\t')[0]) +\
                           string.strip(line.split('\t')[1]), \
                           "%d.%m.%y%H:%M:%S"))
                if time_interval == True:
                    time_step = str(datetime.strptime(\
                                end_time,"%Y%m%d%H%M") -\
                                datetime.strptime(\
                                start_time,"%Y%m%d%H%M"))[2:4]
                    time_interval = False
                if start_time == None:
                    line_skip = line_counter -1
                    start_time = time.strftime("%Y%m%d%H%M",
                                 time.strptime(
                                 string.strip(line.split('\t')[0]) + \
                                 string.strip(line.split('\t')[1]), \
                                 "%d.%m.%y%H:%M:%S"))
                    time_interval = True
                """
        self.set_start_datetime(start_datetime)
        self.set_end_datetime(end_datetime)
        self.set_time_step_delta(time_step_delta)
        self.line_skip = str(line_skip)

    def get_line_skip(self):
        """Gets number of lines to be skiped at the beginning of the logger file
        
        Returns:
            Number of lines to be skiped until data section.
        """
        return self.line_skip

    #TODO(tnauss): Implement csv routine
    def test(self):
        infile = open(self.get_filepath())
        for i in range (0,6):
            infile.next()
        file = csv.reader(infile,delimiter='\t')
        #quoting=csv.QUOTE_NONNUMERIC)
        test =[]
        for row in file:
            test.append(row)
                
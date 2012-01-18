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
__version__ = "2012-01-15"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import csv
from datetime import datetime
import linecache
import string
import time
from julendat.filetools.stations.StationDataFile import StationDataFile
from julendat.processtools.TimeInterval import TimeInterval
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath

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
        if self.get_filetype() == 'ascii':
            self.set_serial_number_ascii()
            stationdatafilepath = StationDataFilePath(filepath)
            if stationdatafilepath.get_standard_name():
                self.set_start_datetime(stationdatafilepath.get_start_datetime())
                self.set_end_datetime(stationdatafilepath.get_end_datetime())         

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
            try:
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
                    header_extension = line_counter -1
                    start_datetime = datetime.strptime(
                                 string.strip(line.split('\t')[0]) + \
                                 string.strip(line.split('\t')[1]), \
                                 "%d.%m.%y%H:%M:%S")
                    compute_time_interval = True
            except:
                continue
        self.set_start_datetime(start_datetime)
        self.set_end_datetime(end_datetime)
        self.set_time_step_delta(time_step_delta)
        self.set_header_extension(header_extension)

    def read_header(self):
        """Reads header of the logger file
        """
        infile = open(self.get_filepath())
        for header_extension in range (0, self.get_header_line()-1):
            infile.next()
        reader = csv.reader(infile,delimiter='\t')
        self.set_column_headers(reader.next())
        infile.close() 

    def read_data(self):
        """Reads content of the logger file
        """
        infile = open(self.get_filepath())
        for header_extension in range (0, self.get_first_data_line()-1):
            infile.next()
        reader = csv.reader(infile,delimiter='\t')
        self.dataset = []
        for row in reader:
            self.dataset.append(row)
        infile.close()
        
    def get_data(self):
        """Gets data of the logger file without the header column
        """
        try: self.dataset
        except:
            self.read_data()
        return self.dataset
    
    def set_column_headers(self,column_headers):
        """Sets column headers of the dataset
        
        Args:
            column_headers: Headers of the columns
        """
        self.column_headers = column_headers
    
    def get_column_headers(self):
        """Gets column headers of the dataset
        """
        try: self.column_headers
        except:
            self.read_header()
        return self.column_headers
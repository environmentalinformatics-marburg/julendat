"""Handle data files from Mayer NT sensor/logger combinations.
Copyright (C) 2011 Thomas Nauss

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
__version__ = "2012-01-17"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import sys
import csv
from datetime import datetime
import linecache
import string
import time
from julendat.filetools.stations.StationDataFile import StationDataFile
from julendat.processtools.TimeInterval import TimeInterval
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath

class MNTStationDataFile(StationDataFile):
    """Instance for handling Mayer NT station data (sensor/logger).

    This instance can be used to handle Driesn & Kern station data which is a
    defined combination of one or more sensors and one logger.
    """

    def __init__(self, filepath, io_access="r"):
        """Inits MNTStationDataFile.
        
        Based on the ASCII file, the data object will be initialized.
        In addition, the serial number of the logger and the time range
        of the data file will be extracted.
        
        Args (from class DataFile):
            filepath: Full path and name of the data file
            io_asccess: IO access (r-read,w-write,rw-read/write)
        """       
        
        StationDataFile.__init__(self, filepath, io_access="r")
        
        self.check_filetype()
        if self.get_filetype() == 'csv' or self.get_filetype() == 'ascii':
            stationdatafilepath = StationDataFilePath(filepath)
            self.set_plot_id_ascii()
            if stationdatafilepath.get_standard_name():
                self.set_start_datetime(stationdatafilepath.get_start_datetime())
                self.set_end_datetime(stationdatafilepath.get_end_datetime())         

    def set_plot_id_ascii(self):
        """Sets station plot id extracted from initial ascii logger file.
        """
        
        if self.get_filetype() == 'csv':
            plot_id = self.get_filename().partition("_")[0]
            if len(plot_id) < 5:
                if plot_id[0:2] == "HG":
                    plot_id = "HEG" + plot_id[2:]  
                elif plot_id[0:2] == "HW":
                    plot_id = "HEW" + plot_id[2:]  
                elif plot_id[0:2] == "SG":
                    plot_id = "SEG" + plot_id[2:]  
                elif plot_id[0:2] == "SW":
                    plot_id = "SEW" + plot_id[2:]  
                elif plot_id[0:2] == "AG":
                    plot_id = "AEW" + plot_id[2:]  
                elif plot_id[0:2] == "AW":
                    plot_id = "AEW" + plot_id[2:]  
                else:
                    raise Exception, "Invalid plot id."
            self.set_plot_id(plot_id)

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
                           string.strip(line.split(';')[0][0:16]), \
                           "%d.%m.%Y %H:%M")
                if compute_time_interval == True:
                    #time_step_delta = end_datetime - start_datetime
                    time_step_delta = TimeInterval(start_datetime, \
                                                     end_datetime)
                    compute_time_interval = False
                if start_datetime == None:
                    header_extension = line_counter -1
                    start_datetime = datetime.strptime(\
                           string.strip(line.split(';')[0][0:16]), \
                           "%d.%m.%Y %H:%M")
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
        reader = csv.reader(infile,delimiter=';')
        self.set_column_headers(reader.next())
        infile.close() 

    def read_data(self):
        """Reads content of the logger file
        """
        infile = open(self.get_filepath())
        for header_extension in range (0, self.get_first_data_line()-1):
            infile.next()
        reader = csv.reader(infile,delimiter=';')
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
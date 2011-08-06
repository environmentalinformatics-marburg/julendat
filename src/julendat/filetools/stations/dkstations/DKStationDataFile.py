'''
Handle data files from Driesen & Kern sensor/logger combinations.
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

@author: Thomas Nauss, Tim Appelhans
@license: GNU General Public License
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2010-08-04    "
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import linecache
import string
import datetime
import time
import os


from julendat.filetools.stations.StationDataFile import StationDataFile

class DKStationDataFile():
    """Class for Driesen & Kern climate stations (sensor/logger combination).
    
    Constructor:
    DKStation(filepath="None", filetype="None", io_access="r")
    
    For Keyword arguments see __init__().
    
    """

    def __init__(self,binFile):
        
        '''Constructor of the Data2Map class.

        The function will initialize the D&K climate station class.
        
        __init__(self)
        '''       

        self.binFile = StationDataFile(binFile)
        self.set_asciiFile()
        self.set_serialNumber()
        self.set_timeRange()


    def get_binaryFile(self):
        '''Get binary file object downloaded from logger.
        
        '''
        return self.binFile

    def set_asciiFile(self):
        '''Set ASCII file object written right after logger data download
        
        '''
        asciiFileExsists = False
        asciiFile = self.binFile.get_file()[:-3] + "asc"
        if os.path.isfile(asciiFile):
            asciiFileExsists = True
        if asciiFileExsists != True:
            asciiFile = self.binFile.get_file()[:-3] + "ASC"
            if os.path.isfile(asciiFile):
                asciiFileExsists = True
        if asciiFileExsists == True:
            self.asciiFile = StationDataFile(asciiFile)
        else:
            asciiFileExsists = False
            self.asciiFile = None
        
        self.asciiFileExists = asciiFileExsists
            

    def get_asciiFile(self):
        '''Get ASCII file object written right after logger data download
        
        '''
        return self.asciiFile


    def get_asciiFileExists(self):
        '''Get information if ASCII file object exists
        
        '''
        return self.asciiFileExists


    def set_serialNumber(self):
        '''Set serial number from level 01 ASCII logger file.

        '''
        line = linecache.getline(self.asciiFile.get_file(), 2)
        self.serialNumber =  string.strip(line.partition(':')[2])
    

    def get_serialNumber(self):
        '''Get serial number from level 01 ASCII logger file.

        '''
        return self.serialNumber
    

    def set_timeRange(self):
        '''Set time range from level 01 ASCII file.
        
        '''
        if self.asciiFileExists == True:
            self.startTime = None
            self.endTime = None
            timeInterval = False
            logger_data = open(self.asciiFile.get_file(),'r')
            for line in logger_data:
                if line[2] == "." and line[5] == ".":
                    self.endTime = time.strftime("%Y%m%d%H%M",
                                       time.strptime(
                                            string.strip(line.split('\t')[0]) + \
                                            string.strip(line.split('\t')[1]), \
                                            "%d.%m.%y%H:%M:%S"))
                    if timeInterval == True:
                        self.timeStep = str(datetime.datetime.strptime(self.endTime,"%Y%m%d%H%M") - \
                        datetime.datetime.strptime(self.startTime,"%Y%m%d%H%M"))[2:4]
                        timeInterval = False
                    if self.startTime == None:
                        self.startTime = time.strftime("%Y%m%d%H%M",
                                        time.strptime(
                                            string.strip(line.split('\t')[0]) + \
                                            string.strip(line.split('\t')[1]), \
                                            "%d.%m.%y%H:%M:%S"))
                        timeInterval = True


    def get_timeRange(self):
        '''Get time range from level 01 ASCII file.
        
        '''
        return self.startTime, self.endTime, self.timeStep


    def get_startTime(self):
        '''Get start time from level 01 ASCII file.

        '''
        return self.startTime


    def get_endTime(self):
        '''Get end time  from level 01 ASCII file.
        
        '''
        return self.endTime


    def get_timeInterval(self):
        '''Get time interval from level 01 ASCII file.
        
        '''
        return self.timeInterval

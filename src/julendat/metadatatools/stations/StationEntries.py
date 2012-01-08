"""Handle station entries information.
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
__version__ = "2012-01-05"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import string
from julendat.filetools.stations.StationInventoryFile import \
    StationInventoryFile


class StationEntries(StationInventoryFile):   
    """Instance for handling station inventory information.
    
    This instance handles station inventory information based on the serial
    number of the station.
    """
    def __init__(self, filepath, io_access="r", station_id=None):
        """Inits StationEntries.
        
        Args (from class DataFile):
            filepath: Full path and name of the data file
            io_asccess: IO access (r-read,w-write,rw-read/write)
        
        Args:
            serial_number: Serial number of the station
        """       
        StationInventoryFile.__init__(self, filepath, io_access="r")
        self.set_station_id(station_id)
        self.set_station_entries_from_station_id()
        
    def set_station_entries_from_station_id(self):
        """Sets station entries information from station id
        """
        #TODO(tnauss): Implement error handling by end of 2011
        foundID = False
        error = False
        entries_data = open(self.get_filepath(),'r')
        for line in entries_data:
            if string.strip(line.rsplit(',')[0])[4:7] == self.get_station_id()[3:6]:
                if foundID == True:
                    print "The same serial number has been found at least twice!"
                    error = True
                else:
                    act_line = line.rstrip()
                    header_extension = int(string.strip(line.rsplit(',')[1]))
                    station_column_entries = calib_coefficents = act_line.rsplit(',')[2:]
                    foundID = True
        entries_data.close()
        self.header_extension = header_extension
        self.station_column_entries = station_column_entries

    def get_header_extension(self):
        """Gets number of lines in the station file before the dataset  starts
        
        Returns:
            Number of lines in the station logger file before the data starts
        """
        return self.header_extension

    def get_station_column_entries(self):
        """Gets column entries of the station looger file
        
        Returns:
            Column entries of the station looger file
        """
        return self.station_column_entries

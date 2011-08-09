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
__version__ = "2010-08-07"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import string
from julendat.filetools.stations.StationInventoryFile import \
    StationInventoryFile


class Level01Standards(StationInventoryFile):   
    """Instance for handling station inventory information.
    
    This instance handles station inventory information based on the serial
    number of the station.
    """
    def __init__(self, filepath, io_access="r"):
        """Inits StationEntries.
        
        Args (from class DataFile):
            filepath: Full path and name of the data file
            io_asccess: IO access (r-read,w-write,rw-read/write)
        
        Args:
            serial_number: Serial number of the station
        """       
        StationInventoryFile.__init__(self, filepath, io_access="r")
        self.set_level01_standards()
        
    def set_level01_standards(self):
        """Sets station entries information from station id
        """
        #TODO(tnauss): Implement error handling by end of 2011
        foundID = False
        error = False
        entries_data = open(self.get_filepath(),'r')
        counter = 0
        for line in entries_data:
            counter = counter + 1
            act_line = line.rstrip()
            if counter == 1:
                level01_column_entries = act_line.rsplit(',')
            else:
                level01_column_entries = level01_column_entries + \
                    act_line.rsplit(',')
                
        self.level01_column_entries = level01_column_entries

    def get_level01_column_entries(self):
        """Gets number of lines in the station file before the dataset  starts
        
        Returns:
            Number of lines in the station logger file before the data starts
        """
        return self.level01_column_entries


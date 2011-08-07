'''
Station  inventory information.
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

@author: Thomas Nauss
@license: GNU General Public License
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>"
__version__ = "2010-08-04    "
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import string
from julendat.filetools.DataFile import DataFile

class StationInventory(DataFile):   
    """Handle station inventory information.
    
    For Keyword arguments see __init__().
    
    """

    
    def get_Inventory_from_serial_number(self,serial_number):
        '''Get plot ID from serial number
        '''
        foundID = False
        error = False
        inventory_data = open(self.get_file(),'r')
        for line in inventory_data:
            if string.strip(line.rsplit(',')[7]) == serial_number:
                if foundID == True:
                    print "The same serial number has been found at least twice!"
                    error = True
                else:
                    plotID = string.strip(line.rsplit(',')[5][1:5])
                    loggerID = string.strip(line.rsplit(',')[6][1:4])
                    foundID = True
        inventory_data.close()
        return plotID, loggerID

        
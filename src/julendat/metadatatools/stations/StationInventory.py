"""Handle station inventory information.
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


class StationInventory(StationInventoryFile):   
    """Instance for handling station inventory information.
    
    This instance handles station inventory information based on the serial
    number of the station.
    """
    def __init__(self, filepath, io_access="r", serial_number=None):
        """Inits StationInventory.
        
        Args (from class DataFile):
            filepath: Full path and name of the data file
            io_asccess: IO access (r-read,w-write,rw-read/write)
        
        Args:
            serial_number: Serial number of the station
        """       
        StationInventoryFile.__init__(self, filepath, io_access="r")
        self.set_serial_number(serial_number)
        self.set_station_inventory_from_serial_number()
        
    def set_station_inventory_from_serial_number(self):
        """Sets station inventory information from serial number
        """
        #TODO(tnauss): Implement error handling by end of 2011
        foundID = False
        error = False
        inventory_data = open(self.get_filepath(),'r')
        plot_id_list = []
        counter = 0
        for line in inventory_data:
            counter = counter + 1
            if counter == 1:
                act_line = line.rstrip()
                calib_coefficents_headers = act_line.rsplit(',')[10:19]
            else:
                plot_id_list.append(string.strip(line.rsplit(',')[5]).strip('"'))
                if string.strip(line.rsplit(',')[7]).strip('"').lstrip('0') == self.get_serial_number():
                    if foundID == True:
                        print "The same serial number has been found at least twice!"
                        error = True
                    else:
                        act_line = line.rstrip()
                        plot_id = string.strip(line.rsplit(',')[5].strip('"'))
                        logger_id = string.strip(line.rsplit(',')[6])
                        header_line = int(string.strip(line.rsplit(',')[8]))
                        first_data_line = int(string.strip(line.rsplit(',')[9]))
                        calib_coefficents = act_line.rsplit(',')[10:19]
                        misc = act_line.rsplit(',')[20:]
                        foundID = True
        inventory_data.close()
        plot_id_list = sorted(set(plot_id_list))
        plot_id_list.append("not sure")
        self.plot_id_list = plot_id_list 
        self.found_station_inventory = foundID
        if self.get_found_station_inventory():
            self.set_plot_id(plot_id)
            self.set_station_id(logger_id)
            self.set_header_line(header_line)
            self.set_first_data_line(first_data_line)
            self.set_calibration_coefficients_headers(calib_coefficents_headers)
            self.set_calibration_coefficients(calib_coefficents)

    def get_found_station_inventory(self):
        """Gets flag if actual station has been found within station inventory.
        
        Returns:
            Flag if station is in station inventory.
        """
        return self.found_station_inventory

    def set_plot_id_from_serial_number(self):
        """Sets plot ID from serial number
        """
        self.set_station_inventory_from_serial_number()
        
    def get_plot_id_list(self):
        """Gets list of all plot ids.
        
        Returns:
            Returns list of plot ids.
        """
        return self.plot_id_list



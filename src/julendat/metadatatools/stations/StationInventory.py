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
__version__ = "2012-01-05"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import string
import os
from julendat.processtools.TimePoint import TimePoint 
from julendat.filetools.stations.StationInventoryFile import \
    StationInventoryFile


class StationInventory(StationInventoryFile):   
    """Instance for handling station inventory information.
    
    This instance handles station inventory information based on the serial
    number of the station.
    """
    def __init__(self, filepath, io_access="r", \
                 logger_start_time=None, logger_end_time=None, plot_id=None, serial_number=None):
        """Inits StationInventory.
        
        Args (from class DataFile):
            filepath: Full path and name of the data file
            io_asccess: IO access (r-read,w-write,rw-read/write)
        
        Args:
            serial_number: Serial number of the station
        """       
        StationInventoryFile.__init__(self, filepath, io_access="r")
        self.logger_start_time = logger_start_time
        self.logger_end_time = logger_end_time
        self.set_plot_id(plot_id)
        self.set_serial_number(serial_number)
        if self.get_plot_id() != None:
            self.set_station_inventory_from_plot_id()
        elif self.get_serial_number() != None:
            self.set_station_inventory_from_serial_number()
        
    def set_station_inventory_from_plot_id(self):
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
                self.set_calibration_coefficients_headers(act_line.rsplit(',')[10:19])
            else:
                plot_id_list.append(string.strip(line.rsplit(',')[5]).strip('"'))
                if string.strip(line.rsplit(',')[5]).strip('"').lstrip('0') == self.get_plot_id():
                    if foundID == True:
                        install_date = TimePoint(string.strip(line.rsplit(',')[8]))
                        uninstall_date = TimePoint(string.strip(line.rsplit(',')[9]))
                        if self.get_logger_install_date() == install_date.get_data_file_time_value() and \
                           self.get_logger_uninstall_date() == uninstall_date.get_data_file_time_value():
                            print "The same plot id has been found at least twice!"
                            error = True
                    else:
                        act_line = line.rstrip()
                        self.set_logger_install_date(string.strip(line.rsplit(',')[8]))
                        self.set_logger_uninstall_date(string.strip(line.rsplit(',')[9]))
                        if self.logger_start_time >= self.get_logger_install_date() and \
                           self.logger_end_time <= self.get_logger_uninstall_date(): 
                            self.set_type(string.strip(line.rsplit(',')[4].strip('"')))
                            self.set_plot_id(string.strip(line.rsplit(',')[5].strip('"')))
                            self.set_station_id(string.strip(line.rsplit(',')[6]))
                            self.set_serial_number(string.strip(line.rsplit(',')[7]))
                            self.set_logger_install_date(string.strip(line.rsplit(',')[8]))
                            self.set_logger_uninstall_date(string.strip(line.rsplit(',')[9]))
                            self.set_header_line(int(string.strip(line.rsplit(',')[10])))
                            self.set_first_data_line(int(string.strip(line.rsplit(',')[11])))
                            self.set_calibration_coefficients(act_line.rsplit(',')[12:21])
                            misc = act_line.rsplit(',')[22:]
                            foundID = True
        inventory_data.close()
        plot_id_list = sorted(set(plot_id_list))
        plot_id_list.append("not sure")
        self.plot_id_list = plot_id_list 
        self.found_station_inventory = foundID

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
                self.set_calibration_coefficients_headers(act_line.rsplit(',')[10:19])
            else:
                plot_id_list.append(string.strip(line.rsplit(',')[5]).strip('"'))
                if string.strip(line.rsplit(',')[7]).strip('"').lstrip('0') == self.get_serial_number():
                    if foundID == True:
                        install_date = TimePoint(string.strip(line.rsplit(',')[8]))
                        uninstall_date = TimePoint(string.strip(line.rsplit(',')[9]))
                        if self.get_logger_install_date() == install_date and \
                           self.get_logger_uninstall_date() == uninstall_date:
                            print "The same serial number has been found at least twice!"
                            error = True
                    else:
                        act_line = line.rstrip()
                        self.set_logger_install_date(string.strip(line.rsplit(',')[8]))
                        self.set_logger_uninstall_date(string.strip(line.rsplit(',')[9]))
                        if self.logger_start_time >= self.get_logger_install_date() and \
                           self.logger_end_time <= self.get_logger_uninstall_date(): 
                            self.set_type(string.strip(line.rsplit(',')[4].strip('"')))
                            self.set_plot_id(string.strip(line.rsplit(',')[5].strip('"')))
                            self.set_station_id(string.strip(line.rsplit(',')[6]))
                            self.set_serial_number(string.strip(line.rsplit(',')[7]))
                            self.set_header_line(int(string.strip(line.rsplit(',')[10])))
                            self.set_first_data_line(int(string.strip(line.rsplit(',')[11])))
                            self.set_calibration_coefficients(act_line.rsplit(',')[12:21])
                            misc = act_line.rsplit(',')[22:]
                            foundID = True
        inventory_data.close()
        plot_id_list = sorted(set(plot_id_list))
        plot_id_list.append("not sure")
        self.plot_id_list = plot_id_list 
        self.found_station_inventory = foundID
        if self.get_found_station_inventory() != True:
            print "Serial number has not been found in station inventory"

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



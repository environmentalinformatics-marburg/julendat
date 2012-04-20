"""Handle data files from sensor/logger combinations.
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

__author__ = "Thomas Nauss <nausst@googlemail.com>"
__version__ = "2012-01-16"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

from julendat.filetools.DataFile import DataFile
from julendat.processtools.TimePoint import TimePoint 


class StationDataFile(DataFile):
    """Instance for handling station data files.

    This instance can be used to handle station data files which is a
    defined combination of one or more sensors and one logger.
    This is also an abstract class for defining station data file functions.
    """
 
    def set_serial_number(self, serial_number=None):
        """Sets station serial number.
        
        Args:
            serial_number: Serial number of the station
        """
        self.serial_number =  serial_number

    def get_serial_number(self):
        """Gets station serial number extracted from ascii logger file.

        Returns:
            Serial number of the logger.
        """
        try:
            return self.serial_number.lstrip('0')
        except:
            return self.serial_number

    def set_project_id(self, project_id=None):
        """Sets project ID of the data file.
        
        Args:
            project_id = Coded project Id
        """
        self.project_id = project_id

    def get_project_id(self):
        """Gets project ID of the data file.
        
        Returns:
            Coded project Id
        """
        return self.project_id
    
    def set_station_id(self, station_id=None):
        """Sets station type of the data file.

        Args:
            station_id: Type of the station (sensor/logger combination)
        """
        self.station_id = station_id

    def get_station_id(self):
        """Gets station type of the data file.

        Returns:
            Type of the station (sensor/logger combination)
        """
        return self.station_id

    def set_logger_install_date(self, logger_install_date):
        """Sets the installation date of the logger/station
        
        Args:
            logger_install_date: Installation date of the logger/station
        """
        self.logger_install_date = TimePoint(logger_install_date)
    
    def get_logger_install_date(self):
        """Gets the installation date of the logger/station
        
        Returns:
            Installation date of the logger/station
        """
        return self.logger_install_date.get_data_file_time_value()
 
    def set_logger_uninstall_date(self, logger_uninstall_date):
        """Sets the uninstall date of the logger/station
        
        Args:
            logger_uninstall_date: Uninstall date of the logger/station
        """
        self.logger_uninstall_date = TimePoint(logger_uninstall_date)
    
    def get_logger_uninstall_date(self):
        """Gets the uninstall date of the logger/station
        
        Returns:
            Uninstall date of the logger/station
        """
        return self.logger_uninstall_date.get_data_file_time_value()
    
    def set_header_extension(self, header_extension):
        """Sets number of header lines at the beginning of the logger file
        
        Args:
            Number of header lines until the start of the data section.
        """
        self.header_extension = header_extension
    
    def get_header_extension(self):
        """Gets number of header lines at the beginning of the logger file
        
        Returns:
            Number of header lines until the start of the data section.
        """
        return self.header_extension


    def set_header_line(self, header_line):
        """Sets header line
        
        Args:
            header_line: Header line
        """
        self.header_line = header_line
    
    def get_header_line(self):
        """Gets header line
        
        Returns:
            Number of header line
        """
        return self.header_line
    
    def set_first_data_line(self, first_data_line):
        """Sets first data line
        
        Args:
            first_data_line: First data line
        """
        self.first_data_line = first_data_line
    
    def get_first_data_line(self):
        """Gets first data line
        
        Returns:
            Number of first data line
        """
        return self.first_data_line
    
    def set_type(self, type=None):
        """Sets type of plot and/or station of the data file.
        
        Args:
            type: Coded ID of the plot and/or station type
        """
        self.type = type

    def get_type(self):
        """Gets tyoe of the plot and/or station of the data file.
        
        Returns:
            Coded ID of the plot and/or station type
        """
        return self.type

    def set_plot_id(self, plot_id=None):
        """Sets plot ID of the data file.
        
        Args:
            plot_id: Coded ID of the station plot
        """
        self.plot_id = plot_id

    def get_plot_id(self):
        """Gets plot ID of the data file.
        
        Returns:
            Coded ID of the station plot
        """
        return self.plot_id

    def get_raw_plot_id(self):
        """Gets raw plot ID of the data file (i. e. without leading zeros).
        
        Returns:
            Coded ID of the station plot without leading zeros
        """
        return self.plot_id.lstrip("0")

    def set_calibration_level(self, calibration_level=None):
        """Sets calibration level of the data file.
        
        Args:
            calibration_level: Coded calibration procedures applied to the data
        """
        self.calibration_level = calibration_level

    def get_calibration_level(self):
        """Gets calibration level of the data file.
        
        Returns:
            Coded calibration procedures applied to the data
        """
        return self.calibration_level

    def set_aggregation(self, aggregation=None):
        """Sets time aggregation of the data file.
        
        Args:
            aggregation: Coded time aggregation of the data set
        """
        self.aggregation = aggregation
        self.set_time_step_delta(aggregation)
    
    def get_aggregation(self):
        """Get time aggregation of the data file.
        
        Returns:
            Coded time aggregation of the data set
        """
        return self.aggregation
    
    def set_postexflag(self, postexflag=None):
        """Sets post extension of the data file.
        
        Args:
            postexflag: Additional information sticked after the extension
        """
        self.postexflag = postexflag

    def get_postexflag(self):
        """Get post extension of the data file.
        
        Returns:
            Additional information sticked after the extension
        """
        return self.postexflag
    
    def set_calibration_coefficients(self, calib_coefficents ):
        """Sets calibration coefficients
        """
        self.calib_coefficents = calib_coefficents  
        
    def get_calibration_coefficients(self):
        """Gets calibration coefficients
        
        Returns:
            Calibration coefficients
        """
        return self.calib_coefficents    

    def set_calibration_coefficients_headers(self, calib_coefficents_headers):
        """Sets calibration coefficients headers
        """
        self.calib_coefficents_headers = calib_coefficents_headers
        
    def get_calibration_coefficients_headers(self):
        """Gets calibration coefficients headers
        
        Returns:
            Calibration coefficient header names
        """
        return self.calib_coefficents_headers    
    
    def check_filetype(self):
        """Sets filetype of the logger file (binary/ascii).
        """
        if self.get_extension() == 'bin' or \
            self.get_extension() == 'BIN':
            filetype = 'bin'
        elif self.get_extension() == 'asc' or \
            self.get_extension() == 'ASC':
            filetype = 'ascii'
        elif self.get_extension() == 'csv' or \
            self.get_extension() == 'CSV':
            filetype = 'csv'
        elif self.get_extension() == 'txt' or \
            self.get_extension() == 'TXT':
            filetype = 'ascii'
        self.set_filetype(filetype)    

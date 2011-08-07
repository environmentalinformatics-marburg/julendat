'''Handle data files from sensor/logger combinations.
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
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>"
__version__ = "2010-08-07"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

from julendat.filetools.DataFile import DataFile


class StationDataFile(DataFile):
    """Instance for handling station data files.

    This instance can be used to handle station data files which is a
    defined combination of one or more sensors and one logger.
    This is also an abstract class for defining station data file functions.
    """
 
    def set_serial_number(self, serial_number=None):
        '''Sets station serial number.
        
        Args:
            serial_number: Serial number of the station
        '''
        self.serial_number =  serial_number

    def get_serial_number(self):
        '''Gets station serial number extracted from ascii logger file.

        Returns:
            Serial number of the logger.
        '''
        return self.serial_number

    def set_project_id(self, project_id=None):
        '''Sets project ID of the data file.
        
        Args:
            project_id = Coded project Id
        '''
        self.project_id = project_id

    def get_project_id(self):
        '''Gets project ID of the data file.
        
        Returns:
            Coded project Id
        '''
        return self.project_id
    
    def set_station_id(self, station_id=None):
        '''Sets station type of the data file.

        Args:
            station_id: Type of the station (sensor/logger combination)
        '''
        self.station_id = station_id

    def get_station_id(self):
        '''Gets station type of the data file.

        Returns:
            Type of the station (sensor/logger combination)
        '''
        return self.station_id

    def set_plot_id(self, plot_id=None):
        '''Sets plot ID of the data file.
        
        Args:
            plot_id: Coded ID of the station plot
        '''
        self.plot_id = plot_id

    def get_plot_id(self):
        '''Gets plot ID of the data file.
        
        Returns:
            Coded ID of the station plot
        '''
        return self.plot_id

    def get_time_range(self):
        '''Gets time range extracted from ascii logger file.

        Returns:
            Time range of the logger file in the following order:
                start time
                end time
                time step in minutes
        '''
        return self.start_time, self.end_time, self.time_step

    def set_start_time(self, start_time=None):
        '''Sets start time extracted from ascii logger file.

        Args:
            Start time of the logger file.
        '''
        self.start_time = start_time

    def get_start_time(self):
        '''Gets start time extracted from ascii logger file.

        Returns:
            Start time of the logger file.
        '''
        return self.start_time

    def set_end_time(self, end_time=None):
        '''Sets end time  extracted from ascii logger file.

        Args:
            End time of the logger file.
        '''
        self.end_time = end_time

    def get_end_time(self):
        '''Gets end time  extracted from ascii logger file.

        Returns:
            End time of the logger file.
        '''
        return self.end_time

    def set_time_step(self, time_step=None):
        '''Sets time step extracted from ascii logger file.

        Args:
            Time interval in minutes of the logger file.
        '''
        self.time_step = time_step

    def get_time_step(self):
        '''Gets time step extracted from ascii logger file.

        Returns:
            Time step in minutes of the logger file.
        '''
        return self.time_step

    def set_calibration_level(self, calibration_level=None):
        '''Sets calibration level of the data file.
        
        Args:
            calibration_level: Coded calibration procedures applied to the data
        '''
        self.calibration_level = calibration_level

    def get_calibration_level(self):
        '''Gets calibration level of the data file.
        
        Returns:
            Coded calibration procedures applied to the data
        '''
        return self.calibration_level

    def set_aggregation(self, aggregation=None):
        '''Sets time aggregation of the data file.
        
        Args:
            aggregation: Coded time aggregation of the data set
        '''
        self.aggregation = aggregation
    
    def get_aggregation(self):
        '''Get time aggregation of the data file.
        
        Returns:
            Coded time aggregation of the data set
        '''
        return self.aggregation
    
    def set_quality(self, quality=None):
        '''Sets quality flag of the data file.
        
        Args:
            quality: Coded quality level of the data file
        '''
        self.quality = quality
    
    def get_quality(self):
        '''Gets quality flag of the data file.
        
        Returns:
            Coded quality level of the data file
        '''
        return self.quality
    
    def set_postexflag(self, postexflag=None):
        '''Sets post extension of the data file.
        
        Args:
            postexflag: Additional information sticked after the extension
        '''
        self.postexflag = postexflag

    def get_postexflag(self):
        '''Get post extension of the data file.
        
        Returns:
            Additional information sticked after the extension
        '''
        return self.postexflag

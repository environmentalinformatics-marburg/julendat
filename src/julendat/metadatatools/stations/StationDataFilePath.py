"""
Automatic filepath, filename and path generation.
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
__version__ = "2012-01-17"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import calendar
import datetime
import time
import os
from julendat.filetools.stations.StationDataFile import StationDataFile
from julendat.processtools import time_utilities

class StationDataFilePath(StationDataFile):   
    """'Instance for generating station data filenames.
    
    The filenames, paths and filepaths (full path and filename) are generated
    according to the filename convention of the Environmental Informatics
    department at Marburg University.
    """
    def __init__(self, filepath=None, io_access="r", serial_number=None, \
                 toplevel_path=None, filename=None, project_id=None, \
                 plot_id=None, station_id=None, start_datetime=None, \
                 end_datetime=None, time_step_delta=None, \
                 logger_time_zone=None, level_0005_time_zone=None, \
                 calibration_level=None, aggregation_level=None, processing=None, \
                 extension=None, postexflag=None):
        """Inits StationDataFilename.
        
        The instiance can be initialized with 
        a) a filename according to the above mentioned naming convention.
        b) the components of the above mentioned naming convention.
        
        If a top level path is provided, a default directory structure
        is generated, too. 
        
        Args (from class DataFile):
            filepath: Full path and name of the data file
            io_asccess: IO access (r-read,w-write,rw-read/write)
        
        Args:
            toplevel_path: Top level path of the default directory structure
            filename: Filename (same as filepath in this instance).
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            station_id: Type of the station (sensor/logger combination)
            start_datetime: Recording time of the first data set in the file
            end_datetime: Recording time of the last data set in the file
            time_step_delta: Recording time interval
            logger_time_zone: Time zone of the logger time values
            level_0005_time_zone: Time zone of the level 0.5+ data files
            calibration_level: Coded calibration procedures applied to the data
            aggregation_level: Coded aggregation_level of the data set
            processing: Coded processing level of the data file
            extension: Filename extension (3 characters)
            postexflag: Additional information sticked after the extension
        """       

        self.logger_time_zone = logger_time_zone
        self.level_0005_time_zone = level_0005_time_zone
        
        if filepath == None:
            filepath = filename
        if filepath != None:
            StationDataFile.__init__(self, filepath=filepath, io_access="r")
            self.check_standard()
            if self.get_standard_name():
                self.disassemble_filename()
        else:
            self.build_initial_filename(project_id=project_id, \
                plot_id=plot_id, station_id=station_id, \
                start_datetime=start_datetime, end_datetime=end_datetime, \
                time_step_delta=time_step_delta, \
                time_zone=self.logger_time_zone, \
                calibration_level=calibration_level,  \
                aggregation_level=aggregation_level, processing=processing, \
                extension=extension, postexflag=postexflag)
            self.check_standard()
        
        self.set_toplevel_path(toplevel_path)

        #if self.standard_name:
        #    self.build_filename_dictionary()

    def build_filename_dictionary(self, aggregation_level=None):
        """Sets dictionary for data filenames of different levels.
        """
        self.filename_dictionary = {}
        #Level 0 (binary)
        calibration_level="rb01"
        processing = "0000"
        extension="bin"
        self.filename_dictionary['level_000_bin-filename'] = \
            self.build_filename(\
                time_zone = self.logger_time_zone, \
                calibration_level=calibration_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_000_bin-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                processing=processing)
        self.filename_dictionary['level_000_bin-filepath'] = \
            self.filename_dictionary['level_000_bin-path'] + \
            self.filename_dictionary['level_000_bin-filename']

        #Level 0 (ascii)
        calibration_level="ra01"
        processing = "0000"
        extension="asc"
        self.filename_dictionary['level_0000_ascii-filename'] = \
            self.build_filename(\
                time_zone = self.logger_time_zone , \
                calibration_level=calibration_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0000_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                processing=processing)
        self.filename_dictionary['level_0000_ascii-filepath'] = \
            self.filename_dictionary['level_0000_ascii-path'] + \
            self.filename_dictionary['level_0000_ascii-filename']
        self.filename_dictionary['temp_filepath'] = \
            self.filename_dictionary['level_0000_ascii-path'] + "temp.txt"
        
        #Level 0005 (calibrated data values, standard format)
        start_datetime = self.get_start_datetime()
        end_datetime = self.get_end_datetime()
        start_datetime = time_utilities.convert_timezone(start_datetime, \
                            self.level_0005_time_zone)
        end_datetime = time_utilities.convert_timezone(end_datetime, \
                            self.level_0005_time_zone)
        start_datetime = start_datetime.strftime("%Y%m%d%H%M")
        end_datetime = end_datetime.strftime("%Y%m%d%H%M")

        calibration_level="ca01"
        processing = "0005"
        extension="dat"
        self.filename_dictionary['level_0005_calibration_level'] = calibration_level
        self.filename_dictionary['level_0005_processing'] = processing
        self.filename_dictionary['level_0005_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0005_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                processing=processing)
        self.filename_dictionary['level_0005_ascii-filepath'] = \
            self.filename_dictionary['level_0005_ascii-path'] + \
            self.filename_dictionary['level_0005_ascii-filename']

        #Level 0050 (monthly time-filled files, standard format)
        calibration_level="ca05"
        processing = "0050"
        extension="dat"
        self.filename_dictionary['level_0050_calibration_level'] = calibration_level
        self.filename_dictionary['level_0050_processing'] = processing
        self.get_month_range()
        self.filename_dictionary['level_0050_ascii-filename'], \
        self.filename_dictionary['level_0050_ascii-path'], \
        self.filename_dictionary['level_0050_ascii-filepath'], \
        self.filename_dictionary['level_0050_start_time_isostr'], \
        self.filename_dictionary['level_0050_end_time_isostr'] = \
            self.get_monthly_filepath(start_datetime=start_datetime, \
                end_datetime=end_datetime, time_zone=self.level_0005_time_zone, \
                calibration_level=calibration_level, processing=processing, \
                extension=extension)
            
        #Level 0100 (monthly processing controled  files, standard format)
        calibration_level="qc01"
        processing = "0100"
        extension="dat"
        self.filename_dictionary['level_0100_calibration_level'] = calibration_level
        self.filename_dictionary['level_0100_processing'] = processing
        self.filename_dictionary['level_0100_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0100_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                processing=processing)
        self.filename_dictionary['level_0100_ascii-filepath'] = \
            self.filename_dictionary['level_0100_ascii-path'] + \
            self.filename_dictionary['level_0100_ascii-filename']           

        #Level 0190 (monthly processing aggregated files, standard format)
        calibration_level="fc01"
        processing = "0190"
        extension="dat"
        start_datetime = start_datetime[0:8]+"0000"
        end_datetime = end_datetime[0:8]+"0000"
        self.filename_dictionary['level_0190_calibration_level'] = calibration_level
        self.filename_dictionary['level_0190_processing'] = processing
        self.filename_dictionary['level_0190_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0190_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing)
        self.filename_dictionary['level_0190_ascii-filepath'] = \
            self.filename_dictionary['level_0190_ascii-path'] + \
            self.filename_dictionary['level_0190_ascii-filename']           

        #Level 0200 (monthly processing aggregated files, standard format)
        calibration_level="fa01"
        processing = "0200"
        extension="dat"
        start_datetime = start_datetime[0:8]+"0000"
        end_datetime = end_datetime[0:8]+"0000"
        self.filename_dictionary['level_0200_calibration_level'] = calibration_level
        self.filename_dictionary['level_0200_processing'] = processing
        self.filename_dictionary['level_0200_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0200_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing)
        self.filename_dictionary['level_0200_ascii-filepath'] = \
            self.filename_dictionary['level_0200_ascii-path'] + \
            self.filename_dictionary['level_0200_ascii-filename']           

        #Level 0250 (monthly processing controled files, standard format)
        calibration_level="qc25"
        processing = "0250"
        extension="dat"
        self.filename_dictionary['level_0250_calibration_level'] = calibration_level
        self.filename_dictionary['level_0250_processing'] = processing
        self.filename_dictionary['level_0250_wildcard'] =  "*" + \
            self.get_station_id() + "*" + start_datetime + "*" + \
            calibration_level + "_" + self.get_aggregation() + "_" + \
            processing + "." + extension
        self.filename_dictionary['level_0250_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0250_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                processing=processing)
        self.filename_dictionary['level_0250_ascii-filepath'] = \
            self.filename_dictionary['level_0250_ascii-path'] + \
            self.filename_dictionary['level_0250_ascii-filename']           

        #Level 0290 (monthly processing controled files, standard format)
        calibration_level="qc25"
        processing = "0290"
        extension="dat"
        level_0290_startdatetime = start_datetime[0:4] + '01010000'
        level_0290_enddatetime = end_datetime[0:4] + '12310000'
        self.filename_dictionary['level_0290_calibration_level'] = calibration_level
        self.filename_dictionary['level_0290_processing'] = processing
        self.filename_dictionary['level_0290_startdatetime'] =  \
            level_0290_startdatetime[0:4] + "-01-01 00:00:00"
        self.filename_dictionary['level_0290_enddatetime'] =  \
            level_0290_enddatetime[0:4] + "-12-31 23:00:00"
        self.filename_dictionary['level_0290_wildcard'] =  "*" + \
            self.get_station_id() + "*" + level_0290_startdatetime + "*" + \
            calibration_level + "_" + self.get_aggregation() + "_" + \
            processing + "." + extension
        self.filename_dictionary['level_0290_wildcard_rug'] =  "*" + \
            "rug" + "*" + level_0290_startdatetime + "*" + \
            calibration_level + "_" + self.get_aggregation() + "_" + \
            processing + "." + extension
        self.filename_dictionary['level_0290_ascii-filename'] = \
            self.build_filename(\
                start_datetime = level_0290_startdatetime, \
                end_datetime = level_0290_enddatetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0290_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                processing=processing)
        self.filename_dictionary['level_0290_ascii-filepath'] = \
            self.filename_dictionary['level_0290_ascii-path'] + \
            self.filename_dictionary['level_0290_ascii-filename']  

        #Level 0300 (monthly gap-filled files, standard format)
        calibration_level="gc01"
        processing = "0300"
        extension="dat"
        start_datetime = start_datetime[0:8]+"0000"
        end_datetime = end_datetime[0:8]+"0000"
        self.filename_dictionary['level_0300_calibration_level'] = calibration_level
        self.filename_dictionary['level_0300_processing'] = processing
        self.filename_dictionary['level_0300_wildcard'] =  "*" + \
            self.get_station_id() + "*" + start_datetime + "*" + \
            calibration_level + "_" + self.get_aggregation() + "_" + \
            processing + "." + extension
        self.filename_dictionary['level_0300_wildcard_rug'] =  "*" + \
            "rug" + "*" + start_datetime + "*" + \
            calibration_level + "_" + self.get_aggregation() + "_" + \
            processing + "." + extension
        self.filename_dictionary['level_0300_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0300_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing)
        self.filename_dictionary['level_0300_ascii-filepath'] = \
            self.filename_dictionary['level_0300_ascii-path'] + \
            self.filename_dictionary['level_0300_ascii-filename']           

        #Level 0310 (monthly gap-filled files, standard format)
        calibration_level="gc02"
        processing = "0310"
        extension="dat"
        start_datetime = start_datetime[0:8]+"0000"
        end_datetime = end_datetime[0:8]+"0000"
        self.filename_dictionary['level_0310_calibration_level'] = calibration_level
        self.filename_dictionary['level_0310_processing'] = processing
        self.filename_dictionary['level_0310_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0310_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing)
        self.filename_dictionary['level_0310_ascii-filepath'] = \
            self.filename_dictionary['level_0310_ascii-path'] + \
            self.filename_dictionary['level_0310_ascii-filename']           

        #Level 0400 (monthly aggregated, gap-filled files, standard format)
        calibration_level="gc02"
        processing = "0400"
        extension="dat"
        start_datetime = start_datetime
        end_datetime = end_datetime
        self.filename_dictionary['level_0400_calibration_level'] = calibration_level
        self.filename_dictionary['level_0400_processing'] = processing
        self.filename_dictionary['level_0400_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0400_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing)
        self.filename_dictionary['level_0400_ascii-filepath'] = \
            self.filename_dictionary['level_0400_ascii-path'] + \
            self.filename_dictionary['level_0400_ascii-filename']    
    
        #Level 0405 (daily aggregated, gap-filled files, standard format)
        calibration_level="gc02"
        processing = "0405"
        extension="dat"
        start_datetime = start_datetime
        end_datetime = end_datetime
        self.filename_dictionary['level_0405_calibration_level'] = calibration_level
        self.filename_dictionary['level_0405_processing'] = processing
        self.filename_dictionary['level_0405_ascii-filename'] = \
            self.build_filename(\
                start_datetime = start_datetime, \
                end_datetime = end_datetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0405_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing)
        self.filename_dictionary['level_0405_ascii-filepath'] = \
            self.filename_dictionary['level_0405_ascii-path'] + \
            self.filename_dictionary['level_0405_ascii-filename']    

        #Level 0415 (monthly aggregated, gap-filled files, standard format)
        calibration_level="gc02"
        processing = "0415"
        extension="dat"
        level_0415_startdatetime = start_datetime[0:4] + '01010000'
        level_0415_enddatetime = end_datetime[0:4] + '12310000'
        self.filename_dictionary['level_0415_calibration_level'] = calibration_level
        self.filename_dictionary['level_0415_processing'] = processing
        self.filename_dictionary['level_0415_startdatetime'] =  \
            level_0290_startdatetime[0:4] + "-01-01 00:00:00"
        self.filename_dictionary['level_0415_enddatetime'] =  \
            level_0290_enddatetime[0:4] + "-12-31 23:00:00"
        self.filename_dictionary['level_0415_ascii-filename'] = \
            self.build_filename(\
                plot_id = "00000000", \
                start_datetime = level_0415_startdatetime, \
                end_datetime = level_0415_enddatetime, \
                time_zone = self.level_0005_time_zone, \
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing, \
                extension=extension)
        self.filename_dictionary['level_0415_ascii-path'] = \
            self.build_path(\
                plot_id = "00000000", \
                calibration_level=calibration_level, \
                aggregation_level=aggregation_level, \
                processing=processing)
        self.filename_dictionary['level_0415_ascii-filepath'] = \
            self.filename_dictionary['level_0415_ascii-path'] + \
            self.filename_dictionary['level_0415_ascii-filename']    

    def get_filename_dictionary(self):
        """Gets dictionary for data filenames of different levels.
        
        Returns:
        Dictionary mapping file depiction keys to the corresponding filenames.
        To get the filepath, filename or path, complement the depiction with
        ...-filepath for the filepath
        ...-filename for the filename
        ...-path for the path
        """
        return self.filename_dictionary

    def set_first_time_of_month(self, start_datetime):
        """Sets start time (hour, minute)
        This must be different from 00:00 for files which do not have a interval
        of 5, 10, 12, 15, etc. and therefore have different minutes.
        
        Args:
            start_datetime: Start time
        """
        start_month = start_datetime.month
        act_month = start_datetime.month
        time_step = self.get_time_step_delta()
        while start_month == act_month:
            start_datetime = start_datetime - datetime.timedelta(seconds=time_step)
            start_month = start_datetime.month
        start_datetime = start_datetime + datetime.timedelta(seconds=time_step)

        '''
        start_time = str(start_datetime.hour).zfill(2) + \
                     str(start_datetime.minute).zfill(2) + \
                     str(start_datetime.second).zfill(2)
        print start_time
        print self.get_aggregation()
        print self.get_time_step_delta()
        '''
        return start_datetime

    def set_last_time_of_month(self, start_datetime):
        """Sets start time (hour, minute)
        This must be different from 00:00 for files which do not have a interval
        of 5, 10, 12, 15, etc. and therefore have different minutes.
        
        Args:
            start_datetime: Start time
        """
        start_month = start_datetime.month
        act_month = start_datetime.month
        time_step = self.get_time_step_delta()
        while start_month == act_month:
            start_datetime = start_datetime + datetime.timedelta(seconds=time_step)
            start_month = start_datetime.month
        start_datetime = start_datetime - datetime.timedelta(seconds=time_step)

        #last_time_of_month = str(start_datetime.hour).zfill(2) + \
        #                     str(start_datetime.minute).zfill(2)

        return start_datetime
    
    def get_month_range(self):
        """Gets month range of the file.
        """
        start_datetime = self.get_start_datetime()
        start_datetime = time_utilities.convert_timezone(start_datetime, \
                            self.level_0005_time_zone)
        end_datetime = self.get_end_datetime()
        end_datetime = time_utilities.convert_timezone(end_datetime, \
                            self.level_0005_time_zone)

        print end_datetime.year, start_datetime.year
        print start_datetime.month, end_datetime.month
        if end_datetime.year - start_datetime.year > 0:
            month_number = (end_datetime.year - start_datetime.year) * 13 - \
                           start_datetime.month + end_datetime.month
            print month_number
        else:
            month_number = end_datetime.month-start_datetime.month+1
        self.month_number = month_number
        start_datetime = self.set_first_time_of_month(start_datetime)
        self.set_start_datetime(start_datetime)
        self.last_time_of_month = self.set_last_time_of_month(start_datetime)

    def get_monthly_filepath(self, project_id=None, plot_id=None, \
                 station_id=None, start_datetime=None, end_datetime=None, \
                 time_zone=None, calibration_level=None, aggregation_level=None, \
                 processing=None, extension=None, postexflag=None):
        """Builds monthly filepathes, filenames and path.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            station_id: Type of the station (sensor/logger combination)
            start_datetime: Recording time of the first data set in the file
            end_datetime: Recording time of the last data set in the file
            time_zone: Time zone of the time values
            calibration_level: Coded calibration procedures applied to the data
            aggregation_level: Coded time aggregation_level of the data set
            processing: Coded processing level of the data file
            extension: Filename extension (3 characters)
            postexflag: Additional information sticked after the extension
        
        Returns:
            filename: Array encomassing all filenames
            path: Array encomassing all paths
            filepath: Array encomassing all filepaths
        """
        filename = []
        path = []
        filepath = []
        start_time_isostr = []
        end_time_isostr = []
        #TODO(tnauss): Read time aggregation from configuration file,
        #and adjust output filenames.
        #if self.get_aggregation()[2:] != "i05":
        #    aggregation_level = "cti05"
  
        aggregation_level = "ct" + self.get_aggregation()[2:]
        
        for i in range(0,self.month_number):
            act_start_time = self.get_start_datetime()
            act_end_time = self.last_time_of_month
            '''
            act_month = act_start_time.month+i
            print act_start_time, act_month
            if act_month > 12:
                act_month = act_month-12
            act_month = str(act_month).zfill(2)
            act_month = str(act_month)
            act_year = str(act_start_time.year+(act_start_time.month+i)/13)

            start_datetime = time.strftime("%Y%m%d%H%M",
                                 time.strptime(act_year + act_month + "010000",\
                                 "%Y%m%d%H%M"))
            start_time_isostr.append(time.strftime("%Y-%m-%d %H:%M:%S",
                                 time.strptime(act_year + act_month + "010000",\
                                 "%Y%m%d%H%M")))
            end_datetime = time.strftime("%Y%m%d%H%M",
                           time.strptime(act_year + act_month + \
                           str(calendar.monthrange(int(act_year), \
                                                   int(act_month))[1]) + \
                            self.last_time_of_month,"%Y%m%d%H%M"))
            end_time_isostr.append(time.strftime("%Y-%m-%d %H:%M:%S",
                           time.strptime(act_year + act_month + \
                           str(calendar.monthrange(int(act_year), \
                                                   int(act_month))[1]) + \
                            self.last_time_of_month,"%Y%m%d%H%M")))                                     
            '''
            start_datetime = time.strftime("%Y%m%d%H%M",
                                 act_start_time.timetuple())
            
            start_time_isostr.append(time.strftime("%Y-%m-%d %H:%M:%S",
                                 act_start_time.timetuple()))
            end_datetime = time.strftime("%Y%m%d%H%M",
                           act_end_time.timetuple())
            end_time_isostr.append(time.strftime("%Y-%m-%d %H:%M:%S",
                           act_end_time.timetuple()))                                     

            filename.append( \
                self.build_filename(\
                    start_datetime=start_datetime, \
                    end_datetime=end_datetime, \
                    time_zone=time_zone, \
                    calibration_level=calibration_level, \
                    aggregation_level=aggregation_level, \
                    processing=processing, \
                    extension=extension))
            path.append( \
                self.build_path(\
                    calibration_level=calibration_level, \
                    aggregation_level = aggregation_level, \
                    processing=processing))
            filepath.append( \
                path[i] + \
                filename[i])
            
            new_start_time = act_end_time + datetime.timedelta(seconds=self.get_time_step_delta())
            new_start_time = self.set_first_time_of_month(new_start_time)
            self.set_start_datetime(new_start_time)
            self.last_time_of_month = self.set_last_time_of_month(new_start_time)

        return filename, path, filepath, start_time_isostr, end_time_isostr
        
    def build_filename(self, project_id=None, plot_id=None, \
                 station_id=None, start_datetime=None, end_datetime=None, \
                 time_step_delta=None, time_zone=None, calibration_level=None, \
                 aggregation_level=None, processing=None, extension=None, \
                 postexflag=None):
        """Builds filename.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            station_id: Type of the station (sensor/logger combination)
            start_datetime: Recording time of the first data set in the file
            end_datetime: Recording time of the last data set in the file
            time_step_delta: Recording time interval
            time_zone: Time zone of the time values
            calibration_level: Coded calibration procedures applied to the data
            aggregation_level: Coded time aggregation_level of the data set
            processing: Coded processing level of the data file
            extension: Filename extension (3 characters)
            postexflag: Additional information sticked after the extension
        
        Returns:
            filename: Filename according to provided arguments.
        """
        if project_id == None:
            project_id = self.get_project_id()
        if plot_id == None:
            plot_id = self.get_plot_id()
        if station_id == None:
            station_id = self.get_station_id()
        if start_datetime == None:
            start_datetime = self.get_start_datetime_eifc()
        if end_datetime == None:
            end_datetime = self.get_end_datetime_eifc()
        if time_zone == None:
            time_zone = self.get_time_zone()
        if calibration_level == None:
            calibration_level = self.get_calibration_level()
        if aggregation_level == None:
            aggregation_level = self.get_aggregation()
        if processing == None:
            processing = self.get_processing()
        if extension == None:
            extension = self.get_extension()
        if postexflag == None:
            postexflag = self.get_postexflag()

        filename = project_id + "_" + \
            plot_id + "_" + \
            station_id + "_" + \
            start_datetime + "_" + \
            end_datetime + "_" + \
            time_zone + "_" + \
            calibration_level + "_" + \
            aggregation_level + "_" + \
            processing + "." + \
            extension
        if postexflag != None:
            filename = filename + "." + postexflag 
        return filename

    def build_path(self, project_id=None, plot_id=None, \
                            calibration_level=None, aggregation_level=None, \
                            processing=None):
        """Builds path to file.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            calibration_level: Coded calibration procedures applied to the data
            aggregation_level: Coded time aggregation_level of the data set
            processing: Coded processing level of the data file
        
        Returns:
            path: Path to file according to provided arguments.
        """
        if project_id == None:
            project_id = self.get_project_id()
        if plot_id == None:
            plot_id = self.get_plot_id()
        if plot_id[0:2] == "xx":
            plot_id = "conflict" + os.sep + plot_id
        if calibration_level == None:
            calibration_level = self.get_calibration_level()
        if aggregation_level == None:
            aggregation_level = self.get_aggregation() 
        if processing == None:
            processing = self.get_processing()
        
        path = self.get_toplevel_path() + \
               project_id  + os.sep + \
               plot_id  + os.sep + \
               calibration_level + "_" + \
               aggregation_level + "_" + \
               processing + os.sep
        
        return path

    def check_standard(self):
        """Checks if file is named according to the naming convention.
        """
        filename = self.get_filename()
        if filename[2] == "_" and filename[11] == "_" \
            and filename[18] == "_" and filename[31]  == "_" \
            and filename[44] == "_" and filename[48] == "_" \
            and filename[53] == "_" and filename[59] == "_":
            self.standard_name  = True
            
        else:
            self.standard_name = False
    
    def get_standard_name(self):
        """Gets info if files has a standard name (True)
        
        Returns
            True if file has a standard name according to the eifc
        """
        return self.standard_name
    
    def build_initial_filename(self,project_id, plot_id, station_id, \
                               start_datetime, end_datetime, time_step_delta, \
                               time_zone, calibration_level, \
                               aggregation_level, processing, extension, \
                               postexflag):
        """Sets filename of the data file.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            station_id: Type of the station (sensor/logger combination)
            start_datetime: Recording time of the first data set in the file
            end_datetime: Recording time of the last data set in the file
            time_step_delta: Recording time interval
            time_zone: Time zone of the time values
            calibration_level: Coded calibration procedures applied to the data
            aggregation_level: Coded time aggregation_level of the data set
            processing: Coded processing level of the data file
            extension: Filename extension (3 characters)
            postexflag: Additional information sticked after the extension
        """

        self.build_project_id(project_id)
        self.build_plot_id(plot_id)
        self.build_station_id(station_id)
        self.build_start_datetime(start_datetime)
        self.build_end_datetime(end_datetime)
        self.build_time_zone(time_zone)
        self.build_calibration_level(calibration_level)
        self.build_aggregation(aggregation_level, time_step_delta)
        self.build_processing(processing)
        self.set_extension(extension)
        self.build_postexflag(postexflag)
        
        filename = self.build_filename(project_id=self.get_project_id(), \
                            plot_id=self.get_plot_id(), \
                            station_id=self.get_station_id(), \
                            start_datetime=self.get_start_datetime_eifc(), \
                            end_datetime=self.get_end_datetime_eifc(), \
                            time_zone=self.get_time_zone(), \
                            calibration_level=self.get_calibration_level(), \
                            aggregation_level=self.get_aggregation(), \
                            processing=self.get_processing(), \
                            extension=self.get_extension(), \
                            postexflag=self.get_postexflag())
        self.set_filepath(filename)
        self.set_filename()
        self.set_extension() 


    def build_project_id(self, project_id):
        """Sets project ID of the data file.

        Args:
            project_id: Coded ID of the project
        """
        if project_id == None:
            project_id = "00"
        self.set_project_id(project_id)

    def build_plot_id(self, plot_id):
        """Sets plot ID of the data file.
        
        Args:
            plot_id: Coded ID of the station plot
        """
        if plot_id == None:
            plot_id = "00000000"
        elif plot_id[0:2] == "xx":
            plot_id = "xx" + plot_id[2:].zfill(6)  
        else:
            plot_id = plot_id.zfill(8)
        
        self.set_plot_id(plot_id)

    def build_station_id(self, station_id):
        """Sets station type of the data file.

        Args:
            station_id: Type of the station (sensor/logger combination)
        """
        if station_id == None:
            station_id = "000000"
        self.set_station_id(station_id)

    def build_start_datetime(self, start_datetime):
        """Sets start time of the data file.

        Args:
            start_datetime: Recording time of the first data set in the file
        """
        if start_datetime == None:
            start_datetime = "000000000000"
        self.set_start_datetime(start_datetime)

    def build_end_datetime(self, end_datetime):
        """Sets end time of the data file.

        Args:
            end_datetime: Recording time of the last data set in the file
        """
        if end_datetime == None:
            end_datetime = "000000000000"
        self.set_end_datetime(end_datetime)

    def build_time_zone(self, time_zone):
        """Sets time zone of the data file.

        Args:
            time_zone: Recording time zone of the data set
        """
        if time_zone == None:
            time_zone = "000"
        self.set_time_zone(time_zone)

    def build_calibration_level(self, calibration_level):
        """Set calibration level of the data file.

        Args:
            calibration_level: Coded calibration procedures applied to the data
        """
        if calibration_level == None:
            calibration_level = "0000"
        self.set_calibration_level(calibration_level)

    def build_aggregation(self, aggregation_level, time_step_delta):
        """Set aggregation_level of the data file.

        Args:
            aggregation_level: Coded time aggregation_level of the data set
        """
        if aggregation_level == None:
            aggregation_level = "00"
        self.set_time_step_delta(time_step_delta)
        self.set_aggregation(aggregation_level + \
                             self.time_step_delta.get_time_step_level_str() + \
                             self.time_step_delta.get_data_file_time_value_eifc())

    def build_processing(self, processing):
        """Set processing level of the data file.
        
        Args:
            processing: Coded processing level of the data file
        """
        if processing == None:
            processing = "00000"
        self.set_processing(processing)

    def build_postexflag(self, postexflag):
        """Set post extension of the data file.
        
        Args:
            postexflag: Additional information sticked after the extension        
        """
        self.set_postexflag(postexflag)

    def set_toplevel_path(self, toplevel_path):
        """Set toplevel path of the data file neseccary for dictionary.

        Args:
            toplevel_path: Top level path of the default directory structure
        """
        if toplevel_path == None:
            toplevel_path = os.getcwd()
        self.toplevel_path = toplevel_path

    def get_toplevel_path(self):
        """Get toplevel path of the data file neseccary for dictionary.
        
        Returns:
            Top level path of the default directory structure
        """
        return self.toplevel_path
    
    def disassemble_filename(self):
        """Disassembles filename.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            station_id: Type of the station (sensor/logger combination)
            start_datetime: Recording time of the first data set in the file
            end_datetime: Recording time of the last data set in the file
            time_zone: Time zone of the time values
            calibration_level: Coded calibration procedures applied to the data
            aggregation_level: Coded time aggregation_level of the data set
            processing: Coded processing level of the data file
            extension: Filename extension (3 characters)
            postexflag: Additional information sticked after the extension
        
        Returns:
            filename: Filename according to provided arguments.
        """
        filename = self.get_filename()
        self.set_project_id(filename[0:2])
        self.set_plot_id(filename[3:11])
        self.set_station_id(filename[12:18])
        self.set_start_datetime(filename[19:31])
        self.set_end_datetime(filename[32:44])
        self.set_time_zone(filename[45:48])
        self.set_calibration_level(filename[49:53])
        self.set_aggregation(filename[54:59])
        self.set_processing(filename[60:64])
        self.set_extension(filename[66:69])
        self.set_postexflag(filename[70:])
        if len(self.get_postexflag()) == 0:
            self.set_postexflag(postexflag=None)
        
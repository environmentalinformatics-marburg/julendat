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
__version__ = "2010-08-07"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import calendar
import datetime
import time
import os
from julendat.filetools.stations.StationDataFile import StationDataFile


class StationDataFilePath(StationDataFile):   
    """'Instance for generating station data filenames.
    
    The filenames, paths and filepaths (full path and filename) are generated
    according to the filename convention of the Environmental Informatics
    department at Marburg University.
    """
    def __init__(self, filepath=None, io_access="r", serial_number=None, \
                 toplevel_path=None, filename=None, project_id=None, \
                 plot_id=None, station_id=None, start_time=None, \
                 end_time=None, calibration_level=None, aggregation=None, \
                 quality=None, extension=None, postexflag=None):
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
            start_time: Recording time of the first data set in the file
            end_time: Recording time of the last data set in the file
            calibration_level: Coded calibration procedures applied to the data
            aggregation: Coded time aggregation of the data set
            quality: Coded quality level of the data file
            extension: Filename extension (3 characters)
            postexflag: Additional information sticked after the extension
        """       
        if filepath == None:
            filepath = filename
        
        if filepath != None:
            StationDataFile.__init__(self, filepath=filepath, io_access="r")
            self.check_standard()
            if self.standard_name:
                self.disassemble_filename()
        else:
            self.build_initial_filename(project_id, plot_id, station_id, \
                                    start_time, end_time, calibration_level, \
                                    aggregation, quality, extension, postexflag)
            self.check_standard()
        
        self.set_toplevel_path(toplevel_path)
        
        if self.standard_name:
            self.build_filename_dictionary()

    def build_filename_dictionary(self):
        """Sets dictionary for data filenames of different levels.
        """
               
        self.filename_dictionary = {}

        #Level 0 (binary)
        calibration_level="rb01"
        quality = "0000"
        extension="bin"
        self.filename_dictionary['level_000_bin-filename'] = \
            self.build_filename(\
                calibration_level=calibration_level, \
                quality=quality, \
                extension=extension)
        self.filename_dictionary['level_000_bin-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                quality=quality)
        self.filename_dictionary['level_000_bin-filepath'] = \
            self.filename_dictionary['level_000_bin-path'] + \
            self.filename_dictionary['level_000_bin-filename']

        #Level 0 (ascii)
        calibration_level="ra01"
        quality = "0000"
        extension="asc"
        self.filename_dictionary['level_00_ascii-filename'] = \
            self.build_filename(\
                calibration_level=calibration_level, \
                quality=quality, \
                extension=extension)
        self.filename_dictionary['level_00_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                quality=quality)
        self.filename_dictionary['level_00_ascii-filepath'] = \
            self.filename_dictionary['level_00_ascii-path'] + \
            self.filename_dictionary['level_00_ascii-filename']

        #Level 0.5 (ascii)
        calibration_level="ca01"
        quality = "0000"
        extension="dat"
        self.filename_dictionary['level_05_ascii-filename'] = \
            self.build_filename(\
                calibration_level=calibration_level, \
                quality=quality, \
                extension=extension)
        self.filename_dictionary['level_05_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                quality=quality)
        self.filename_dictionary['level_05_ascii-filepath'] = \
            self.filename_dictionary['level_05_ascii-path'] + \
            self.filename_dictionary['level_05_ascii-filename']

        #Level 0.6 (ascii)
        calibration_level="ca01"
        quality = "0000"
        extension="dat"
        self.get_month_range()
        
        self.filename_dictionary['level_06_ascii-filename'], \
        self.filename_dictionary['level_06_ascii-path'], \
        self.filename_dictionary['level_06_ascii-filepath'] = \
            self.get_monthly_filepath(calibration_level=calibration_level, \
                quality=quality, extension=extension)

        #Level 1.0 (filled)
        calibration_level="ca01"
        quality = "0010"
        extension="dat"
        self.filename_dictionary['level_10_ascii-filename'] = \
            self.build_filename(\
                calibration_level=calibration_level, \
                quality=quality, \
                extension=extension)
        self.filename_dictionary['level_10_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                quality=quality)
        self.filename_dictionary['level_10_ascii-filepath'] = \
            self.filename_dictionary['level_10_ascii-path'] + \
            self.filename_dictionary['level_10_ascii-filename']
    
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

    def get_month_range(self):
        """Gets month range of t file.
        """
        start_time = datetime.datetime.strptime(\
                            self.get_start_time(),"%Y%m%d%H%M")
        end_time = datetime.datetime.strptime(\
                            self.get_end_time(),"%Y%m%d%H%M")
        month_number = end_time.month-start_time.month
        start_year = str(start_time.year)
        start_month = str(start_time.month)
        start_month = start_month.zfill(2)
        start_time = time.strftime("%Y%m%d%H%M",
                             time.strptime(start_year+start_month+"010000",\
                             "%Y%m%d%H%M"))
        last_time_of_month = "23" + str(60 - int(self.get_aggregation()[3:5]))
        self.set_start_time(start_time)
        self.month_number = month_number
        self.last_time_of_month = last_time_of_month

    def get_monthly_filepath(self, project_id=None, plot_id=None, \
                 station_id=None, start_time=None, end_time=None, \
                 calibration_level=None, aggregation=None, \
                 quality=None, extension=None, postexflag=None):
        """Builds monthly filepathes, filenames and path.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            station_id: Type of the station (sensor/logger combination)
            start_time: Recording time of the first data set in the file
            end_time: Recording time of the last data set in the file
            calibration_level: Coded calibration procedures applied to the data
            aggregation: Coded time aggregation of the data set
            quality: Coded quality level of the data file
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
        for i in range(0,self.month_number+1):
            act_time = datetime.datetime.strptime(\
                                self.get_start_time(),"%Y%m%d%H%M")
            act_month = str((act_time.month+i)%12)
            act_year = str(act_time.year+(act_time.month+i)/12)
            start_time = time.strftime("%Y%m%d%H%M",
                                 time.strptime(act_year + act_month + "010000",\
                                 "%Y%m%d%H%M"))
            end_time = time.strftime("%Y%m%d%H%M",
                           time.strptime(act_year + act_month + \
                           str(calendar.monthrange(int(act_year), \
                                                   int(act_month))[1]) + \
                            self.last_time_of_month,"%Y%m%d%H%M"))
            filename.append( \
                self.build_filename(\
                    start_time=start_time, \
                    end_time=end_time, \
                    calibration_level=calibration_level, \
                    quality=quality, \
                    extension=extension))
            path.append( \
                self.build_path(\
                    calibration_level=calibration_level, \
                    quality=quality))
            filepath.append( \
                path[i] + \
                filename[i])

        return filename, path, filepath
        
    def build_filename(self, project_id=None, plot_id=None, \
                 station_id=None, start_time=None, end_time=None, \
                 calibration_level=None, aggregation=None, \
                 quality=None, extension=None, postexflag=None):
        """Builds filename.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            station_id: Type of the station (sensor/logger combination)
            start_time: Recording time of the first data set in the file
            end_time: Recording time of the last data set in the file
            calibration_level: Coded calibration procedures applied to the data
            aggregation: Coded time aggregation of the data set
            quality: Coded quality level of the data file
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
        if start_time == None:
            start_time = self.get_start_time()
        if end_time == None:
            end_time = self.get_end_time()
        if calibration_level == None:
            calibration_level = self.get_calibration_level()
        if aggregation == None:
            aggregation = self.get_aggregation()
        if quality == None:
            quality = self.get_quality()
        if extension == None:
            extension = self.get_extension()
        if postexflag == None:
            postexflag = self.get_postexflag()

        filename = project_id + "_" + \
                   plot_id + "_" + \
                   station_id + "_" + \
                   start_time + "_" + \
                   end_time + "_" + \
                   calibration_level + "_" + \
                   aggregation + "_" + \
                   quality + "." + \
                   extension
        if postexflag != None:
            filename = filename + "." + postexflag 
        
        return filename

    def build_path(self, project_id=None, plot_id=None, \
                            calibration_level=None, aggregation=None, \
                            quality=None):
        """Builds path to file.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            calibration_level: Coded calibration procedures applied to the data
            aggregation: Coded time aggregation of the data set
            quality: Coded quality level of the data file
        
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
        if aggregation == None:
            aggregation = self.get_aggregation()
        if quality == None:
            quality = self.get_quality()
        
        path = self.get_toplevel_path() + os.sep + \
               project_id  + os.sep + \
               plot_id  + os.sep + \
               calibration_level + "_" + \
               aggregation + "_" + \
               quality + os.sep
        
        return path

    def check_standard(self):
        """Checks if file is named according to the naming convention.
        """
        filename = self.get_filename()
        if filename[2] == "_" and filename[11] == "_" \
            and filename[15] == "_" and filename[28]  == "_" \
            and filename[41] == "_" and filename[46] == "_" \
            and filename[52] == "_":
            self.standard_name  = True
            
        else:
            self.standard_name = False
    
    def build_initial_filename(self,project_id, plot_id, station_id, \
                               start_time, end_time, calibration_level, \
                               aggregation, quality, extension, postexflag):
        """Sets filename of the data file.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            station_id: Type of the station (sensor/logger combination)
            start_time: Recording time of the first data set in the file
            end_time: Recording time of the last data set in the file
            calibration_level: Coded calibration procedures applied to the data
            aggregation: Coded time aggregation of the data set
            quality: Coded quality level of the data file
            extension: Filename extension (3 characters)
            postexflag: Additional information sticked after the extension
        """
        self.build_project_id(project_id)
        self.build_plot_id(plot_id)
        self.build_station_id(station_id)
        self.build_start_time(start_time)
        self.build_end_time(end_time)
        self.build_calibration_level(calibration_level)
        self.build_aggregation(aggregation)
        self.build_quality(quality)
        self.set_extension(extension)
        self.build_postexflag(postexflag)

        filename = self.get_project_id() + "_" + \
                        self.get_plot_id() + "_" + \
                        self.get_station_id() + "_" + \
                        self.get_start_time() + "_" + \
                        self.get_end_time() + "_" + \
                        self.get_calibration_level() + "_" + \
                        self.get_aggregation() + "_" + \
                        self.get_quality() + "." + \
                        self.get_extension()
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
            station_id = "000"
        self.set_station_id(station_id)

    def build_start_time(self, start_time):
        """Sets start time of the data file.

        Args:
            start_time: Recording time of the first data set in the file
        """
        if start_time == None:
            start_time = "000000000000"
        self.set_start_time(start_time)

    def build_end_time(self, end_time):
        """Sets end time of the data file.

        Args:
            end_time: Recording time of the last data set in the file
        """
        if end_time == None:
            end_time = "000000000000"
        self.set_end_time(end_time)

    def build_calibration_level(self, calibration_level):
        """Set calibration level of the data file.

        Args:
            calibration_level: Coded calibration procedures applied to the data
        """
        if calibration_level == None:
            calibration_level = "0000"
        self.set_calibration_level(calibration_level)

    def build_aggregation(self, aggregation):
        """Set aggregation of the data file.

        Args:
            aggregation: Coded time aggregation of the data set
        """
        if aggregation == None:
            aggregation = "00000"
        self.set_aggregation(aggregation)

    def build_quality(self, quality):
        """Set quality flag of the data file.
        
        Args:
            quality: Coded quality level of the data file
        """
        if quality == None:
            quality = "00000"
        self.set_quality(quality)

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
            start_time: Recording time of the first data set in the file
            end_time: Recording time of the last data set in the file
            calibration_level: Coded calibration procedures applied to the data
            aggregation: Coded time aggregation of the data set
            quality: Coded quality level of the data file
            extension: Filename extension (3 characters)
            postexflag: Additional information sticked after the extension
        
        Returns:
            filename: Filename according to provided arguments.
        """
        filename = self.get_filename()
        self.set_project_id(filename[0:2])
        self.set_plot_id(filename[3:11])
        self.set_station_id(filename[12:15])
        self.set_start_time(filename[16:28])
        self.set_end_time(filename[29:41])
        self.set_calibration_level(filename[42:46])
        self.set_aggregation(filename[47:52])
        self.set_quality(filename[53:57])
        self.set_extension(filename[58:61])
        self.set_postexflag(filename[62:])
        if len(self.get_postexflag()) == 0:
            self.set_postexflag(postexflag=None)
        
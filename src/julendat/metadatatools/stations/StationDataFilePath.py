'''
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
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2010-08-07"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import os
from julendat.filetools.stations.StationDataFile import StationDataFile


class StationDataFilePath(StationDataFile):   
    """Instance for generating station data filenames.
    
    The filenames, paths and filepaths (full path and filename) are generated
    according to the filename convention of the Environmental Informatics
    department at Marburg University.
    """
    def __init__(self, filepath=None, io_access="r", serial_number=None, \
                 toplevel_path=None, filename=None, project_id=None, \
                 plot_id=None, station_id=None, start_time=None, \
                 end_time=None, calibration_level=None, aggregation=None, \
                 quality=None, extension=None, postexflag=None):
        '''Inits StationDataFilename.
        
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
        '''       
        if filepath == None:
            filepath = filename
        else:
            filename = filepath
        StationDataFile.__init__(self, filepath=None, io_access="r")
        self.set_toplevel_path(toplevel_path)
            
        if filepath == None:
            self.build_project_id(project_id)
            self.build_plot_id(plot_id)
            self.build_station_id(station_id)
            self.build_start_time(start_time)
            self.build_end_time(end_time)
            self.build_calibration_level(calibration_level)
            self.build_aggregation(aggregation)
            self.build_quality(quality)
            self.set_file_extension(extension)
            self.build_postexflag(postexflag)
            self.build_initial_filename()
        
        self.check_standard()
        if self.standard_name:
            self.build_filename_dictionary()

    def build_filename_dictionary(self):
        '''Sets dictionary for data filenames of different levels.
        '''
               
        self.filename_dictionary = {}

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

        calibration_level="ra01"
        quality = "0000"
        extension="asc"
        self.filename_dictionary['level_001_ascii-filename'] = \
            self.build_filename(\
                calibration_level=calibration_level, \
                quality=quality, \
                extension=extension)
        self.filename_dictionary['level_001_ascii-path'] = \
            self.build_path(\
                calibration_level=calibration_level, \
                quality=quality)
        self.filename_dictionary['level_001_ascii-filepath'] = \
            self.filename_dictionary['level_001_ascii-path'] + \
            self.filename_dictionary['level_001_ascii-filename']

    def get_filename_dictionary(self):
        '''Gets dictionary for data filenames of different levels.
        
        Returns:
        Dictionary mapping file depiction keys to the corresponding filenames.
        To get the filepath, filename or path, complement the depiction with
        ...-filepath for the filepath
        ...-filename for the filename
        ...-path for the path
        '''
        return self.filename_dictionary

    def build_filename(self, project_id=None, plot_id=None, \
                 station_id=None, start_time=None, end_time=None, \
                 calibration_level=None, aggregation=None, \
                 quality=None, extension=None, postexflag=None):
        '''buils filename.

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
        '''
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
            extension = self.get_file_extension()
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
        '''buils path to file.

        Args:
            project_id: Coded ID of the project
            plot_id: Coded ID of the station plot
            calibration_level: Coded calibration procedures applied to the data
            aggregation: Coded time aggregation of the data set
            quality: Coded quality level of the data file
        
        Returns:
            path: Path to file according to provided arguments.
        '''
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
        '''Checks if file is named according to the naming convention.
        '''
        print "HALI", self.filename
        filename = self.get_filename()
        if filename[2] == "_" and filename[11] == "_" \
            and filename[15] == "_" and filename[28]  == "_" \
            and filename[41] == "_" and filename[46] == "_" \
            and filename[52] == "_":
            self.standard_name  = True
            
        else:
            self.standard_name = False
    
    def build_initial_filename(self):
        '''Sets filename of the data file.

        Args:
            filename: Filename
        '''
        filename = self.get_project_id() + "_" + \
                        self.get_plot_id() + "_" + \
                        self.get_station_id() + "_" + \
                        self.get_start_time() + "_" + \
                        self.get_end_time() + "_" + \
                        self.get_calibration_level() + "_" + \
                        self.get_aggregation() + "_" + \
                        self.get_quality() + "." + \
                        self.get_file_extension()
        self.set_filepath(filename)
        self.set_filename()
        self.set_file_extension()                

    def build_project_id(self, project_id):
        '''Sets project ID of the data file.

        Args:
            project_id: Coded ID of the project
        '''
        if project_id == None:
            project_id = "00"
        self.set_project_id(project_id)

    def build_plot_id(self, plot_id):
        '''Sets plot ID of the data file.
        
        Args:
            plot_id: Coded ID of the station plot
        '''
        if plot_id == None:
            plot_id = "00000000"
        elif plot_id[0:2] == "xx":
            plot_id = "xx" + plot_id[2:].zfill(6)  
        else:
            plot_id = plot_id.zfill(8)
        
        self.set_plot_id(plot_id)

    def build_station_id(self, station_id):
        '''Sets station type of the data file.

        Args:
            station_id: Type of the station (sensor/logger combination)
        '''
        if station_id == None:
            station_id = "000"
        self.set_station_id(station_id)

    def build_start_time(self, start_time):
        '''Sets start time of the data file.

        Args:
            start_time: Recording time of the first data set in the file
        '''
        if start_time == None:
            start_time = "000000000000"
        self.set_start_time(start_time)

    def build_end_time(self, end_time):
        '''Sets end time of the data file.

        Args:
            end_time: Recording time of the last data set in the file
        '''
        if end_time == None:
            end_time = "000000000000"
        self.set_end_time(end_time)

    def build_calibration_level(self, calibration_level):
        '''Set calibration level of the data file.

        Args:
            calibration_level: Coded calibration procedures applied to the data
        '''
        if calibration_level == None:
            calibration_level = "0000"
        self.set_calibration_level(calibration_level)

    def build_aggregation(self, aggregation):
        '''Set aggregation of the data file.

        Args:
            aggregation: Coded time aggregation of the data set
        '''
        if aggregation == None:
            aggregation = "00000"
        self.set_aggregation(aggregation)

    def build_quality(self, quality):
        '''Set quality flag of the data file.
        
        Args:
            quality: Coded quality level of the data file
        '''
        if quality == None:
            quality = "00000"
        self.set_quality(quality)

    def build_postexflag(self, postexflag):
        '''Set post extension of the data file.
        
        Args:
            postexflag: Additional information sticked after the extension        
        '''
        self.set_postexflag(postexflag)

    def set_toplevel_path(self, toplevel_path):
        '''Set toplevel path of the data file neseccary for dictionary.

        Args:
            toplevel_path: Top level path of the default directory structure
        '''
        if toplevel_path == None:
            toplevel_path = os.getcwd()
        self.toplevel_path = toplevel_path

    def get_toplevel_path(self):
        '''Get toplevel path of the data file neseccary for dictionary.
        
        Returns:
            Top level path of the default directory structure
        '''
        return self.toplevel_path

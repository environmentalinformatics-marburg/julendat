"""Handle data files.
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
__version__ = "2010-08-07"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import os


class DataFile:   
    """Instance for handling data files.

    This instance can be used to handle station data files .
    This is also an abstract class for defining data file functions.
    """

    def __init__(self, filepath, io_access="r"):
        """Inits DataFile.
        
        Args:
            filepath: Full path and name of the data file.
            io_asccess: IO access (r-read,w-write,rw-read/write)
        """       
        self.set_io_access(io_access)
        self.set_filepath(filepath)
        if self.get_filepath() != None:
            self.set_filename()
            self.set_extension()
            self.set_path()
            self.check_file_exists()
        
    def set_io_access(self, io_access):
        """Sets read/write access of the file.
        
        Args:
            io_access: IO access (r-read,w-write,rw-read/write)
        """
        self.io_access = io_access

    def get_io_access(self):
        """Gets read/write access of the file.
        
        Returns:
            IO access of the data file.
        """
        return self.io_access

    def set_filepath(self, filepath):
        """Sets full path and name of the data file.

        Args:
             filepath: Full path and name of the data file.
        """
        self.file = filepath

    def get_filepath(self):
        """Gets full path and name of the data file.
        
        Returns:
            Full path and name of the data file.
        """
        return self.file

    def set_filename(self, filename=None):
        """Sets name of the data file.
        
        Args:
            filename: Name of the data file
        """
        if filename != None:
            self.filename = filename
        self.filename = os.path.split(self.get_filepath())[1] 

    def get_filename(self):
        """Gets name of the data file.
        
        Returns:
            Name of the data file.
        """
        return self.filename
    
    def set_extension(self, extension=None):
        """Sets extension (last 3 characters) of the data file.

        Args:
            extension: Filename extension (3 characters)
        """
        if extension == None:
            try:
                extension = self.get_filename()[-3:]
            except:
                extension = "dat"
        self.extension = extension

    def get_extension(self):
        """Gets extension (last 3 characters) of the data file.
        
        Returns:
            Extension (last 3 characters) of the data file.
        """
        return self.extension

    def set_path(self):
        """Sets path of the data file.
        """
        self.data_path = os.path.split(self.get_filepath())[0]

    def get_path(self):
        """Gets path of the data file.
        
        Returns:
            Full path of the data file.        
        """
        return self.data_path

    def check_file_exists(self):
        """Checks if file exists.
        """
        if os.path.isfile(self.get_filepath()):
            self.file_exists = True
        else:
            self.file_exists = False

    def get_file_exists(self):
        """Gets flag if file exists (true/false).
        
        Returns:
            Flag if file exists (true/false)
        """
        return self.file_exists
    
    def set_filetype(self, filetype=None):
        """Sets filetype of the station file (binary/ascii).
        
        Args
            Filetype of the file.
        """
        self.filetype = filetype

    def get_filetype(self):
        """Gets filetype of the station file (binary/ascii).
        
        Returns
            Filetype (binary/ascii of the data file.
        """
        return self.filetype

    def get_time_range(self):
        """Gets time range extracted from data file.

        Returns:
            Time range of the data file in the following order:
                start time
                end time
                time step in minutes
        """
        return self.start_time, self.end_time, self.time_step

    def set_start_time(self, start_time=None):
        """Sets start time extracted from data file.

        Args:
            Start time of the data file.
        """
        self.start_time = start_time

    def get_start_time(self):
        """Gets start time extracted from data file.

        Returns:
            Start time of the data file.
        """
        return self.start_time

    def set_end_time(self, end_time=None):
        """Sets end time  extracted from data file.

        Args:
            End time of the data file.
        """
        self.end_time = end_time

    def get_end_time(self):
        """Gets end time  extracted from data file.

        Returns:
            End time of the data file.
        """
        return self.end_time

    def set_time_zone(self, time_zone=None):
        """Sets time zone extracted from data file.

        Args:
            Time zone of the data file.
        """
        self.time_zone = time_zone

    def get_time_zone(self):
        """Gets time zone extracted from data file.

        Returns:
            Time zone of the data file.
        """
        return self.time_zone

    def set_time_step(self, time_step=None):
        """Sets time step extracted from data file.

        Args:
            Time interval in minutes of the data file.
        """
        self.time_step = time_step

    def get_time_step(self):
        """Gets time step extracted from data file.

        Returns:
            Time step in minutes of the data file.
        """
        return self.time_step    

    def set_quality(self, quality=None):
        """Sets quality flag of the data file.
        
        Args:
            quality: Coded quality level of the data file
        """
        self.quality = quality
    
    def get_quality(self):
        """Gets quality flag of the data file.
        
        Returns:
            Coded quality level of the data file
        """
        return self.quality

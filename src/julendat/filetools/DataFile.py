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
import datetime
import time

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
        """Gets time range extracted from data file as time object.

        Returns:
            Time range of the data file as time object in the following order:
                start time
                end time
                time step in minutes
        """
        return self.start_datetime, self.end_datetime, self.time_step_delta

    def get_time_range_str(self):
        """Gets time range extracted from data file as string.

        Returns:
            Time range of the data file as string in the following order:
                start time
                end time
                time step in minutes
        """
        return self.start_datetime_str, self.end_datetime_str, \
            self.time_step_delta_str

    def set_start_datetime(self, start_datetime=None):
        """Sets start time of the data file as datetime object.

        Args:
            Start time of the data file.
        """
        if  isinstance(start_datetime, str):
            start_datetime = datetime.datetime.strptime(start_datetime, "%Y%m%d%H%M")
        self.start_datetime = start_datetime
        self.set_start_datetime_str(self.start_datetime)

    def get_start_datetime(self):
        """Gets start time of the data file as datetime object.

        Returns:
            Start time of the data file as datetime object.
        """
        return self.start_datetime

    def set_start_datetime_str(self, start_datetime=None):
        """Sets start time extracted from data file.

        Args:
            Start time of the data file.
        """
        self.start_datetime_str = time.strftime("%Y%m%d%H%M", \
                                                    start_datetime.timetuple())

    def get_start_datetime_str(self):
        """Gets start time of the data file as string.

        Returns:
            Start time of the data file as string.
        """
        return self.start_datetime_str

    def set_end_datetime(self, end_datetime=None):
        """Sets end time of the data file as datetime object.

        Args:
            end time of the data file.
        """
        if isinstance(end_datetime, str):
            end_datetime = datetime.datetime.strptime(end_datetime, "%Y%m%d%H%M")
        self.end_datetime = end_datetime
        self.set_end_datetime_str(self.end_datetime)

    def get_end_datetime(self):
        """Gets end time of the data file as datetime object.

        Returns:
            end time of the data file as datetime object.
        """
        return self.end_datetime

    def set_end_datetime_str(self, end_datetime=None):
        """Sets end time extracted from data file.

        Args:
            end time of the data file.
        """
        self.end_datetime_str = time.strftime("%Y%m%d%H%M", \
                                                    end_datetime.timetuple())

    def get_end_datetime_str(self):
        """Gets end time of the data file as string.

        Returns:
            end time of the data file as string.
        """
        return self.end_datetime_str

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

    def set_time_step_delta(self, time_step_delta=None):
        """Sets time step of the data file as datetime.timedelta object.

        Args:
            time step of the data file as datetime.timedelta object.
        """
        if  isinstance(time_step_delta, str):
            a = datetime.datetime.strptime("2001010101" + time_step_delta, "%Y%m%d%H%M")
            b = datetime.datetime.strptime("200101010100", "%Y%m%d%H%M")
            time_step_delta = a - b
        print time_step_delta
        self.time_step_delta = time_step_delta
        self.set_time_step_delta_str(time_step_delta)

    def get_time_step_delta(self):
        """Gets time step of the data file as datetime.timedelta object.

        Returns:
            Time time step of the data file as datetime.timedelta object.
        """
        return self.time_step_delta

    def set_time_step_delta_str(self, time_step_delta=None):
        """Sets time step of the data file as string.

        Args:
            time step of the data file as datetime.timedelta object.
        """
        y = "0000"
        m = "00"
        d = "00"
        h = "00"
        i = "00"
        s = "00"

        seconds = time_step_delta.total_seconds()
        if seconds < 60.0:
            s = time.strftime("%S",time.strptime(str(int(seconds)),"%S"))
            time_step_delta_str = s
            time_step_level = "seconds"
        elif seconds >= 60.0:
            i = seconds // 60.0
            remainder = seconds - (i*60.0)
            s = time.strftime("%S",time.strptime(str(int(remainder)),"%S"))
            if i < 60.0:
                i = time.strftime("%M",time.strptime(str(int(i)),"%M"))
                time_step_delta_str = i
                time_step_level = "minutes"
            elif i >= 60.0:
                h = i // 60.0
                remainder = i - (h*60)
                i = time.strftime("%M",time.strptime(str(int(remainder)),"%M"))
                if h < 24.0:
                    h = time.strftime("%H",time.strptime(str(int(h)),"%H"))
                    time_step_delta_str = h
                    time_step_level = "hours"
                if h >= 24.0:
                    d = h // 24.0
                    remainder = h - (d*24)
                    h = time.strftime("%H",time.strptime(str(int(remainder)),"%H"))
                    d = time.strftime("%d",time.strptime(str(int(d)),"%d"))
                    time_step_delta_str = d
                    time_step_level = "days"

        self.time_step_delta_str = time_step_delta_str
        self.time_step_level = time_step_level
    
    def get_time_step_delta_str(self):
        """Gets time step of the data file as string.

        Returns:
            Time time step of the data file as string.
        """
        return self.time_step_delta_str

    def get_time_step_level_str(self):
        """Gets coded time step level of the data file.

        Returns:
            Coded time step level of the data file
        """
        if self.time_step_level == "seconds":
           self.time_step_level_str = "s"
        elif self.time_step_level == "minutes":
            self.time_step_level_str = "i"
        elif self.time_step_level == "hours":
            self.time_step_level_str = "h"
        elif self.time_step_level == "days":
            self.time_step_level_str = "d"
        return self.time_step_level_str

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

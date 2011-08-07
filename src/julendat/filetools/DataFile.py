'''Handle data files.
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

import os


class DataFile:   
    """Instance for handling data files.

    This instance can be used to handle station data files .
    This is also an abstract class for defining data file functions.
    """

    def __init__(self, filepath, io_access="r"):
        '''Inits DataFile.
        
        Args:
            filepath: Full path and name of the data file.
            io_asccess: IO access (r-read,w-write,rw-read/write)
        '''       
        self.set_io_access(io_access)
        self.set_filepath(filepath)
        if self.get_filepath() != None:
            self.set_filename()
            self.set_file_extension()
            self.set_path()
            self.check_file_exists()
        
    def set_io_access(self, io_access):
        '''Sets read/write access of the file.
        
        Args:
            io_access: IO access (r-read,w-write,rw-read/write)
        '''
        self.io_access = io_access

    def get_io_access(self):
        '''Gets read/write access of the file.
        
        Returns:
            IO access of the data file.
        '''
        return self.io_access

    def set_filepath(self, filepath):
        '''Sets full path and name of the data file.

        Args:
             filepath: Full path and name of the data file.
        '''
        self.file = filepath

    def get_filepath(self):
        '''Gets full path and name of the data file.
        
        Returns:
            Full path and name of the data file.
        '''
        return self.file

    def set_filename(self, filename=None):
        '''Sets name of the data file.
        
        Args:
            filename: Name of the data file
        '''
        if filename != None:
            self.filename = filename
        self.filename = os.path.split(self.get_filepath())[1] 

    def get_filename(self):
        '''Gets name of the data file.
        
        Returns:
            Name of the data file.
        '''
        return self.filename
    
    def set_file_extension(self, extension=None):
        '''Sets extension (last 3 characters) of the data file.

        Args:
            extension: Filename extension (3 characters)
        '''
        if extension == None:
            try:
                extension = self.get_filename()[-3:]
            except:
                extension = "dat"
        self.file_extension = extension

    def get_file_extension(self):
        '''Gets extension (last 3 characters) of the data file.
        
        Returns:
            Extension (last 3 characters) of the data file.
        '''
        return self.file_extension

    def set_path(self):
        '''Sets path of the data file.
        '''
        self.data_path = os.path.split(self.get_filepath())[0]

    def get_path(self):
        '''Gets path of the data file.
        
        Returns:
            Full path of the data file.        
        '''
        return self.data_path

    def check_file_exists(self):
        '''Checks if file exists.
        '''
        if os.path.isfile(self.get_filepath()):
            self.file_exists = True
        else:
            self.file_exists = False

    def get_file_exists(self):
        '''Gets flag if file exists (true/false).
        
        Returns:
            Flag if file exists (true/false)
        '''
        return self.file_exists
    
    def set_filetype(self, filetype=None):
        '''Sets filetype of the station file (binary/ascii).
        
        Args
            Filetype of the file.
        '''
        self.filetype = filetype

    def get_filetype(self):
        '''Gets filetype of the station file (binary/ascii).
        
        Returns
            Filetype (binary/ascii of the logger file.
        '''
        return self.filetype

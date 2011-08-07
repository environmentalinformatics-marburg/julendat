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
    """Class for handling data files.

    This instance can be used to handle station data files .
    This is also an abstract class for defining data file functions.
    """

    def __init__(self, path_to_file, io_access="r"):
        '''Inits DataFile.
        
        Args:
            path_to_file: Full path and name of the data file.
            io_asccess: IO access (r-read,w-write,rw-read/write)
        '''       
        self.set_io_access(io_access)
        self.set_file(path_to_file)
        self.set_filename()
        self.set_path()

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

    def set_file(self, path_to_file):
        '''Sets full path and name of the data file.

        Args:
             path_to_file: Full path and name of the data file.
        '''
        self.data_file = path_to_file

    def get_file(self):
        '''Gets full path and name of the data file.
        
        Returns:
            Full path and name of the data file.
        '''
        return self.data_file

    def set_filename(self):
        '''Sets name of the data file.
        '''
        self.data_filename = os.path.split(self.get_file())[1] 

    def get_filename(self):
        '''Gets name of the data file.
        
        Returns:
            Name of the data file.
        '''
        return self.data_filename.get_filename()

    def get_filename_extension(self):
        '''Gets name of the data file.
        
        Returns:
            Extension (last 3 characters) of the data file.
        '''
        return self.data_filename.get_extension()

    def set_path(self):
        '''Sets path of the data file.
        '''
        self.data_path = os.path.split(self.get_file())[0]

    def get_path(self):
        '''Get path of the data file.
        
        Returns:
            Full path of the data file.        
        '''
        return self.data_path

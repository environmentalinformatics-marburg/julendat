'''
Basic class for data file handling.
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

@author: Thomas Nauss
@license: GNU General Public License
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>"
__version__ = "2010-08-04    "
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import os

class DataFile:   
    """Abstract class for data files.
    
    Constructor:
    DataFile(filepath="None", filetype="None", io_access="r")
    
    For Keyword arguments see __init__().
    
    """

    def __init__(self, file, io_access="r"):
        '''Constructor of the class.         

        __init__(self, file, filetype,io_access="r")
        
        @param file: Full path and name of the data file.
        @param filetype: Type of the data file.
        @param io_access: Read/write access to data file ('r' or 'w').

        '''

        self.set_io_access(io_access)
        self.set_file(file)
        self.set_filename()
        self.set_path()


    def set_io_access(self, io_access):
        '''Set read/write access of the file.
        
        @param io_access: Read ('r') or write ('w') access to data file
        
        '''

        self.io_access = io_access


    def get_io_access(self):
        '''Get read/write access of the file.
        
        '''

        return self.io_access


    def set_file(self, file):
        '''Set full path and name of the data file.
        
        '''

        self.data_file = file


    def get_file(self):
        '''Get full path and name of the data file.
        
        '''

        return self.data_file


    def set_filename(self):
        '''Set name of the data file.
        
        '''

        self.data_filename = os.path.split(self.get_file())[1] 
        


    def get_filename(self):
        '''Get name of the data file.
        
        '''

        return self.data_filename.get_filename()


    def get_filename_extension(self):
        '''Get name of the data file.
        
        '''

        return self.data_filename.get_extension()


    def set_path(self):
        '''Set path of the data file.
        
        '''

        self.data_path = os.path.split(self.get_file())[0]


    def get_path(self):
        '''Get path of the data file.
        
        '''

        return self.data_path
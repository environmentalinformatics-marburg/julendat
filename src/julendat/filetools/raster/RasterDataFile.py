"""Handle raster data files.
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
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import os
import datetime
from julendat.filetools.DataFile import DataFile

class RasterDataFile(DataFile):
    """Instance for handling raster data files.

    This instance can be used to handle raster data files.
    This is also an abstract class for defining station data file functions.
    """
    def __init__(self, filepath, filetype, io_access="r"):
        """Inits RasterDataFile.
 
        Args (from DataFile):
            filepath: Full path and name of the data file.
            io_access: Read/write access to data file ('r' or 'w').
        
        Args:
            filetype: Type of the data file.
        """
        DataFile.__init__(self, filepath, io_access="r")
        self.set_filetype(filetype)


    def set_filetype(self, filetype):
        """Sets type of the data file.

        Args:
            filetype: Type of the data file
        """
        self.filetype = filetype

    def get_filetype(self):
        """Get type of the data file.
        
        Returns:
            Type of the data file
        """
        return self.filetype

    def get_metadata_file(self):
        """Gets filename of the metadata file.
        
        Returns:
            Filename of the metadata file.
        """
        return self.metadata_file

    def set_metadata_filename(self):
        """Sets name of the metadata file.
        """
        self.metadata_filename = os.path.split(self.get_metadata_file())[1]

    def get_metadata_filename(self):
        """Gets name of the metadata file.
        
        Returns:
            Name of the metadata file.
        """
        return self.metadata_filename

    def set_metadata_path(self):
        """Sets path of the metadata file.
        """
        self.metadata_path = os.path.split(self.get_metadata_file())[0]

    def get_metadata_path(self):
        """Gets path of the metadata file.
        
        Returns:
            Path of the metadata file.
        """
        return self.metadata_path

    def get_metadata(self):
        """Gets metadata as dicitionary.

        Returns:
            Metadata dictionary.
        """
        return self.variable_metadata

    def get_variable_name(self):
        """Gets variable name.
        
        Returns:
            Variable name.
        """
        return self.variable_name

    def set_layer(self, layer=0):
        """Sets layer.
        
        Args:
            Layer of the data file (e. g. within HDF EOS file)
        """
        self.layer = layer

    def get_layer(self):
        """Gets layer.
        
        Returns:
            Layer of the data file.
        """
        return self.layer

    def set_flag_store_time_values(self, flag_store_time_values=False):
        """Sets flag for storing time values in read data function.
        
        Args:
          flag_store_time_values: Flag for storing time values in read function.  
        """
        self.flag_store_time_values = flag_store_time_values

    def get_flag_store_time_values(self):
        """Gets flag for storing time values in read data function.

        Returns:
          flag_store_time_values: Flag for storing time values in read function.  
        """
        return self.flag_store_time_values

    def get_variable_names(self):
        """Gets variable names from data file.
        
        Returns:
            Dictionary containing the variable names.
        """
        return self.variable_names

    def get_variable_metadata(self):
        """Gets metadata of the variable.
        
        Returns:
            Dictionary containing the metadata of variables.
        """
        return self.variable_metadata

    def get_variable_dimensions(self):
        """Gets dimensions of the variable.
        
        Returns:
            Dictionary containing the variable dimensions.
        """
        return self.variable_dimensions

    def get_variable_shape(self):
        """Gets shape of the variable.
        
        Returns:
            Dictionary containing the variable shape.
        """
        return self.variable_shape

    def get_data(self):
        """Gets data values of the variable.
        
        Returns:
            Numpy array containing the data values of the actual variable.
        """
        return self.data

# The following functions might have to be implemented in the actual classes.
    def set_start_timestep(self, start_time=False):
        """Sets start time step of the data set variable.
        
        Args:
            start_timestep: Start time of the dataset (for e. g. netCDF)
        """
        try:
            start_time = \
                datetime.datetime.strptime(start_time,"%Y%m%d%H%M%S")
        except TypeError:
            start_time = start_time
        self.set_start_time(start_time)

    def set_end_timestep(self, end_time=False):
        """Sets end time step of the data set variable.
        
        Args:
            start_timestep: End time of the dataset (for e. g. netCDF)
        """
        try:
            end_time = datetime.datetime.strptime(end_time,"%Y%m%d%H%M%S")
        except TypeError:
            end_time = end_time
        self.set_end_time(end_time)

    def set_variable_names(self, variable_names):
        """Sets variable names of the data file.
        
        Args:
            variable_names: Variable names of interest.
        """
        self.variable_names = variable_names

    def set_variable_metadata(self, variable_metadata):
        """Sets metadata of the variable.
        
        Args:
            variable_metadata: Dictionary containing the metadata.
        """
        self.variable_metadata = variable_metadata

    def set_variable_dimensions(self, variable_dimensions):
        """Sets dimensions of the variable.
        
        Args:
            variable_dimensions: Dictionary containing variable dimensions.
        """
        self.variable_dimensions = variable_dimensions

    def set_variable_shape(self, variable_shape):
        """Set shape of the variable.
        
        Args:
            variable_shape: Dictionary containing the variable shape.
        """
        self.variable_shape = variable_shape

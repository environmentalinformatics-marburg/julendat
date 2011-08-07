'''Handle raster data files from.
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

#from julendat.filetools.DataFile import DataFile
#TODO(tnauss): Adjust to julendat.
import os
import datetime


class RasterDataFile():
    """Instance for handling station data files.

    This instance can be used to handle station data files which is a
    defined combination of one or more sensors and one logger.
    This is also an abstract class for defining station data file functions.
    """
    def __init__(self, filepath, filetype, io_access="r"):
        '''Constructor of the class.         

        Args:
        filepath: Full path and name of the data file.
        filetype: Type of the data file.
        io_access: Read/write access to data file ('r' or 'w').
        '''

        self.set_filetype(filetype)
        self.set_io_access(io_access)
        self.set_data_file(filepath)
        self.set_data_filename()
        self.set_data_path()
        self.initialize()


    def set_filetype(self, filetype):
        '''Set type of the data file.
        
        @param filetype: Type of the data file
        
        '''

        self.filetype = filetype


    def get_filetype(self):
        '''Get type of the data file.
        
        '''

        return self.filetype


    def set_io_access(self, io_access):
        '''Set read/write access of the file.
        
        @param io_access: Read ('r') or write ('w') access to data file
        
        '''

        self.io_access = io_access


    def get_io_access(self):
        '''Get read/write access of the file.
        
        '''

        return self.io_access


    def set_data_file(self, filepath):
        '''Set full path and name of the data file.
        
        '''

        self.data_file = filepath


    def get_data_file(self):
        '''Get full path and name of the data file.
        
        '''

        return self.data_file


    def set_data_filename(self):
        '''Set name of the data file.
        
        '''

        self.data_filename = os.path.split(self.get_data_file())[1]


    def get_data_filename(self):
        '''Get name of the data file.
        
        '''

        return self.data_filename


    def set_data_path(self):
        '''Set path of the data file.
        
        '''

        self.data_path = os.path.split(self.get_data_file())[0]


    def get_data_path(self):
        '''Get path of the data file.
        
        '''

        return self.data_path


    def get_metadata_file(self):
        '''Get filename of the metadata file.
        
        '''

        return self.metadata_file


    def set_metadata_filename(self):
        '''Set name of the metadata file.
        
        '''

        self.metadata_filename = os.path.split(self.get_metadata_file())[1]


    def get_metadata_filename(self):
        '''Get name of the metadata file.
        
        '''

        return self.metadata_filename


    def set_metadata_path(self):
        '''Set path of the metadata file.
        
        '''

        self.metadata_path = os.path.split(self.get_metadata_file())[0]


    def get_metadata_path(self):
        '''Get path of the metadata file.
        
        '''

        return self.metadata_path

    def get_metadata(self):
        '''Get metadata as dicitionary.
        
        '''

        return self.variable_metadata


    def get_variable_name(self):
        '''Get variable name.
        
        '''

        return self.variable_name


    def set_layer(self, layer=0):
        '''Set layer.
        
        '''

        self.layer = layer


    def get_layer(self):
        '''Get layer.
        
        '''

        return self.layer


    def get_timestep(self):
        '''Get timestep.
        
        '''

        return self.timestep


    def get_start_timestep(self):
        '''Get start timestep.
        
        '''

        return self.start_timestep


    def get_end_timestep(self):
        '''Get end timestep.
        
        '''

        return self.end_timestep


    def set_flag_store_time_values(self, flag_store_time_values=False):
        '''Set flag for storing time values in read data function.
        
        '''

        self.flag_store_time_values = flag_store_time_values


    def get_flag_store_time_values(self):
        '''Get flag for storing time values in read data function.
        
        '''

        return self.flag_store_time_values


    def set_quality_flag(self, quality_flag=" ?"):
        '''Set quality flag.
        
        '''

        self.quality_flag = quality_flag


    def get_quality_flag(self):
        '''Get quality flag.
        
        '''

        return self.quality_flag


    def get_variable_names(self):
        '''Get variable names from data file.
        
        Returns
        Dictionary containing the variable names.

        '''

        return self.variable_names


    def get_variable_metadata(self):
        '''Get metadata of the variable.
        
        Returns
        Dictionary containing the metadata.

        '''

        return self.variable_metadata


    def get_variable_dimensions(self):
        '''Get dimensions of the variable.
        
        Returns
        Dictionary containing the variable dimensions.

        '''

        return self.variable_dimensions


    def get_variable_shape(self):
        '''Get shape of the variable.
        
        Returns
        Dictionary containing the variable shape.

        '''

        return self.variable_shape


    def get_data(self):
        '''Get data values of the variable.
        
        Returns
        Numpy array containing the data values of the actual variable.

        '''

        return self.data


# The following functions have to be implemented in the actual classes.
    def initialize(self):
        '''Initialize everything you can.         

        '''


    def set_metadata_file(self):
        '''Set full path and name of the metadata file.
        
        '''


    def set_metadata(self):
        '''Set metadata.

        This function has to be implemented by the actual data file class.
        

        '''


    def set_variable_name(self):
        '''Set variable name.

        This function has to be implemented by the actual data file class.

        '''


    def set_timestep(self):
        '''Set variable name.

        This function has to be implemented by the actual data file class.

        '''


    def write_data(self, datavalues=None):
        '''Write data values of the variable to the data file.

        This function has to be implemented by the actual data file class.

        '''

 
# The following functions might have to be implemented in the actual classes.
    def set_start_timestep(self, start_timestep=False):
        '''Set start time step of the data set variable.
        
        @param start_timestep: Start time of the dataset (for e. g. netCDF)
                 
        '''

        try:
            self.start_timestep = \
                datetime.datetime.strptime(start_timestep,"%Y%m%d%H%M%S")
        except TypeError:
            self.start_timestep = start_timestep

    def set_end_timestep(self, end_timestep=False):
        '''Set end time step of the data set variable.
        
        @param start_timestep: End time of the dataset (for e. g. netCDF)
        
        '''

        try:
            self.end_timestep = datetime.datetime.strptime(end_timestep,"%Y%m%d%H%M%S")
        except TypeError:
            self.end_timestep = end_timestep


    def set_variable_names(self, variable_names):
        '''Set variable names of the data file.
        
        @param variable_names: Variable names of interest.

        '''

        self.variable_names = variable_names


    def set_variable_metadata(self, variable_metadata):
        '''Set metadata of the variable.
        
        @param variable_metadata: Dictionary containing the metadata.

        '''

        self.variable_metadata = variable_metadata


    def set_variable_dimensions(self, variable_dimensions):
        '''Set dimensions of the variable.
        
        @param variable_dimensions: Dictionary containing variable dimensions.

        '''

        self.variable_dimensions = variable_dimensions


    def set_variable_shape(self, variable_shape):
        '''Set shape of the variable.
        
        @param variable_shape: Dictionary containing the variable shape.

        '''

        self.variable_shape = variable_shape


"""Handle data file conversions.
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

#TODO(tnauss): Adjust to julendat

import os
import julendat.metadatatools.raster.RasterDataFilePath as RasterDataFilePath


class DataConverter(object):
    """Instance for handling data files.

    This instance can be used to handle station data files .
    This is also an abstract class for defining data file functions.
    """

    def __init__(self, filepath, output_filetype, output_path):
        """Inits DataFile.
        
        Args:
            filepath : Full path and name of the data file.
            output_filetype : Type of the output data file.
            output_path : Full path to the output directory.
        """       
        self.set_filepath(filepath)
        self.set_filepathname()
        self.set_input_data_path()
        self.set_input_filetype()
        self.set_input_data_product()
        self.set_output_filetype(output_filetype)
        self.set_output_path(output_path)
        self.set_satellite_system()
        self.set_timestep()
        self.initialize()

    def set_filepath(self, filepath):
        """Sets full path and name of the input data file.
        
        Args:
            filepath : Full name and path of the input data file.
        """
        self.filepath = filepath

    def get_filepath(self):
        """Gets full path and name of the input data file.
        
        Returns:
            Full name and path of the input data file.
        """
        return self.filepath

    def set_filepathname(self, filepathname='none'):
        """Sets name of the input data file.
        
        Args:
            filepathname : Name of input data file ( default: none)
        """
        if filepathname == 'none':
            filepathname = os.path.split(
                                          self.get_filepath())[1]
        self.filepathname = filepathname 

    def get_filepathname(self):
        """Gets name of the input data file.
        
        Returns:
            Name of input data file.
        """
        return self.filepathname

    def set_input_data_path(self, input_data_path='none'):
        """Sets path of the input data file.
        
        Args:
            input_data_path : Path of the input data file (default: none)
        """
        if input_data_path == 'none':
            input_data_path = os.path.split(self.get_filepath())[0]
        self.input_data_path = input_data_path

    def get_input_data_path(self):
        """Gets path of the input data file.
        
        Returns:
            Path of the input data file.
        """
        return self.input_data_path

    def set_input_filetype(self, input_filetype='none'):
        """Sets type of the input data file.
        
        Args:
            filetype : Type of the input data file.
        """
        if input_filetype == 'none':
            input_filetype = \
            RasterDataFilePath.get_extension_from_filename(self.get_filepathname())
        self.input_filetype = input_filetype

    def get_input_filetype(self):
        """Gets type of the input data file.
        
        Returns:
            Type of the input data file
        """
        return self.input_filetype

    def set_input_data_product(self, input_data_product='none'):
        """Sets overall data set product of the input data file
        from its filename (default) or from parameter.

        Args:
            input_data_product : Product of the input data file. 
        """
        if input_data_product == 'none':
            self.input_data_product = \
            RasterDataFilePath.get_product_from_filename(
                                     self.get_filepathname())
        else:
            self.input_data_product = input_data_product

    def get_input_data_product(self):
        """Gets overall data set product of the input data file.
        
        Returns:
            Product of the input data file.
        """
        return self.input_data_product

    def set_satellite_system(self, satellite_system='none'):
        """Sets satellite system of the data set from its filename
        (default) or from parameter.
        
        Args:
            satellite_system : Satellite system of the input data set.
        """
        if satellite_system == 'none':
            self.satellite_system = \
            RasterDataFilePath.get_convention_satellite_system(
            self.get_filepathname())
        else:
            self.satellite_system = satellite_system

    def get_satellite_system(self):
        """Gets satellite system.
        
        Returns:
            Satellite system of the input data set.
        """
        return self.satellite_system

    def set_timestep(self, timestep='none'):
        """Sets time step of variable from filename (default) or from parameter.
        
        Args:
            timestep : Time step of the data set variable.
        """
        if timestep == 'none':
            self.timestep = \
            RasterDataFilePath.get_convention_time(self.get_filepathname())
        else:
            self.timestep = timestep

    def get_timestep(self):
        """Gets time step of variable.
        
        Returns:
            Time step of the data set variable.
        """
        return self.timestep

    def set_output_data_file(self, output_data_file):
        """Sets full path and name of the output data file.
        
        Args:
            output_data_file : Full name and path of the output data file.
        """
        self.output_data_file = output_data_file


    def get_output_data_file(self):
        """Gets full path and name of the output data file.
        
        Returns:
            Full name and path of the output data file.
        """
        return self.output_data_file


    def set_output_path(self, output_path='none'):
        """Sets path of the output data file.
        
        Args:
            output_path : Path of the output data file (default: none)
        """
        if output_path == 'none':
            output_path = self.get_input_data_path()
        self.output_path = output_path

    def get_output_path(self):
        """Gets path of the output data file.
        
        Returns:
            Path of the output data file.
        """
        return self.output_path
    
    def set_output_filetype(self, output_filetype):
        """Sets type of the output data file.
        
        Args:
            output_filetype : Type of the output data file.
        """
        self.output_filetype = output_filetype

    def get_output_filetype(self):
        """Gets type of the output data file.
        
        Returns:
            Type of the output data file.
        """

        return self.output_filetype

    def get_output_data_filename(self):
        """Gets name of the output data file.
        
        Returns:
            Name of the output data file.
        """
        return self.output_data_filename
    

    def initialize(self):
        """Initialize everything you can.         

        """

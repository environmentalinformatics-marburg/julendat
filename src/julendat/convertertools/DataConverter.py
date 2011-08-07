'''Handle data files from sensor/logger combinations.
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

#TODO(tnauss): Adjust to julendat

import os
import julendat.metadatatools.raster.RasterDataFilePath as RasterDataFilePath


class DataConverter(object):
    """Abstract class as basis for more specified classes for converting
    geo data files.
    
    Constructor:
    GeoFileConverter(input_data_file, output_filetype, data_outpath)
    
    For Keyword arguments see __init__().
    
    """


    def __init__(self, input_data_file, output_filetype, output_data_path):
        '''Constructor of the class.         
        
        @param input_data_file : Full path and name of the data file.
        @param output_filetype : Type of the output data file.
        @param output_data_path : Full path to the output directory.

        '''

        self.set_input_data_file(input_data_file)
        self.set_input_data_filename()
        self.set_input_data_path()
        self.set_input_filetype()
        self.set_input_data_product()
        self.set_output_filetype(output_filetype)
        self.set_output_data_path(output_data_path)
        self.set_satellite_system()
        self.set_timestep()
        self.initialize()


    def set_input_data_file(self, input_data_file):
        '''Set full path and name of the input data file.
        
        @param input_data_file : Full name and path of the input data file.
        
        '''

        self.input_data_file = input_data_file


    def get_input_data_file(self):
        '''Get full path and name of the input data file.
        
        '''

        return self.input_data_file


    def set_input_data_filename(self, input_data_filename='none'):
        '''Set name of the input data file.
        
        @param input_data_filename : Name of input data file ( default: none)
                
        '''
        
        if input_data_filename == 'none':
            input_data_filename = os.path.split(
                                          self.get_input_data_file())[1]
        self.input_data_filename = input_data_filename 


    def get_input_data_filename(self):
        '''Get name of the input data file.
        
        '''

        return self.input_data_filename


    def set_input_data_path(self, input_data_path='none'):
        '''Set path of the input data file.
        
        @param input_data_path : Path of the input data file (default: none)
        
        '''

        if input_data_path == 'none':
            input_data_path = os.path.split(self.get_input_data_file())[0]
        self.input_data_path = input_data_path
 

    def get_input_data_path(self):
        '''Get path of the input data file.
        
        '''

        return self.input_data_path


    def set_input_filetype(self, input_filetype='none'):
        '''Set type of the input data file.

        @param filetype : Type of the input data file.
                        
        '''

        if input_filetype == 'none':
            input_filetype = \
            RasterDataFilePath.get_extension_from_filename(self.get_input_data_filename())
        self.input_filetype = input_filetype


    def get_input_filetype(self):
        '''Get type of the input data file.
         
        '''

        return self.input_filetype


    def set_input_data_product(self, input_data_product='none'):
        '''Set overall data set product of the input data file
        from its filename (default) or from parameter.

        @param input_data_product : Product of the input data file. 
                
        '''

        if input_data_product == 'none':
            self.input_data_product = \
            RasterDataFilePath.get_product_from_filename(
                                     self.get_input_data_filename())
        else:
            self.input_data_product = input_data_product


    def get_input_data_product(self):
        '''Get overall data set product of the input data file.
         
        '''

        return self.input_data_product


    def set_satellite_system(self, satellite_system='none'):
        '''Set satellite system of the data set from its filename
        (default) or from parameter.
        
        @param satellite_system : Satellite system of the input data set.
                
        '''

        if satellite_system == 'none':
            self.satellite_system = \
            RasterDataFilePath.get_convention_satellite_system(
            self.get_input_data_filename())
        else:
            self.satellite_system = satellite_system


    def get_satellite_system(self):
        '''Get satellite system.
        
        '''

        return self.satellite_system


    def set_timestep(self, timestep='none'):
        '''Set time step of variable from filename (default) or from parameter.
        
        @param timestep : Time step of the data set variable.
        
        '''

        if timestep == 'none':
            self.timestep = \
            RasterDataFilePath.get_convention_time(self.get_input_data_filename())
        else:
            self.timestep = timestep


    def get_timestep(self):
        '''Get time step of variable.
        
        '''
        
        return self.timestep


    def set_output_data_file(self, output_data_file):
        '''Set full path and name of the output data file.
        
        @param output_data_file : Full name and path of the output data file.
        
        '''

        self.output_data_file = output_data_file


    def get_output_data_file(self):
        '''Get full path and name of the output data file.
        
        '''

        return self.output_data_file


    def set_output_data_path(self, output_data_path='none'):
        '''Set path of the output data file.
        
        @param output_data_path : Path of the output data file (default: none)
        
        '''

        if output_data_path == 'none':
            output_data_path = self.get_input_data_path()
        self.output_data_path = output_data_path
 

    def get_output_data_path(self):
        '''Get path of the output data file.
        
        '''

        return self.output_data_path

    
    def set_output_filetype(self, output_filetype):
        '''Set type of the output data file.
        
        @param output_filetype : Type of the output data file.
        
        '''

        self.output_filetype = output_filetype


    def get_output_filetype(self):
        '''Get type of the output data file.
        
        '''

        return self.output_filetype


# Get-routines for variables defined in the derived classes for the output file.
    def get_output_data_filename(self):
        '''Get name of the output data file.
        
        '''

        return self.output_data_filename
    

# The following functions have to be implemented in the actual classes.
    def initialize(self):
        '''Initialize everything you can.         

        '''

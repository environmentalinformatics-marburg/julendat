"""Handle conversion of CMORPH files to Idrisi raster files.
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
__version__ = "2012-04-29"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

#TODO(tnauss): Adjust to julendat

import array
import numpy
import sys
import datetime
import os
import julendat.metadatatools.raster.RasterDataFilePath as RasterDataFilePath
from julendat.convertertools.DataConverter import DataConverter
from julendat.metadatatools.geolocations.GeoLocations import GeoLocations
from julendat.filetools.raster.idrisi.IdrisiDataFile import IdrisiDataFile


class CMORPH2RSTConverter(DataConverter):
    """Convert NOAA CMORPH file to Idrisi raster data files.
    
    Constructor:
    CMORPH2RSTConverter(input_filepath, output_filetype, data_outpath)
    
    For Keyword arguments see DataConverter.DataConverter.__init__().
    
    """

    def initialize(self):
        """Initialize several class variables.

        The function will initialize the metadata variables of the
        class instance.
        
        """

    def convert(self, projection='Standard_CMORPH'):
        """Initialize several class variables.

        The function will initialize the metadata variables of the
        class instance.
        
        """
    
        self.set_output_projection(projection)
        self.set_output_filenames()            
        if self.get_output_projection() != 'Standard_CMORPH':
            self.reproject()


    def reproject(self):
        """Reproject hdf file using gdalwarp.
        
        """

        '''
        for counter in range(0, len(self.get_sds_index())):
            command = 'gdalwarp -t_srs EPSG:' + \
                      str(self.get_output_projection().get_projection()[18]) + \
                      ' -te ' + \
                      str(self.get_output_projection().get_projection()[12]) + \
                      ' ' + \
                      str(self.get_output_projection().get_projection()[14]) + \
                      ' ' + \
                      str(self.get_output_projection().get_projection()[13]) + \
                      ' ' + \
                      str(self.get_output_projection().get_projection()[15]) + \
                      ' -tr ' +\
                      str(self.get_output_projection().get_projection()[19]) + \
                      ' ' + \
                      str(self.get_output_projection().get_projection()[20]) + \
                      " -of RST 'HDF4_EOS:EOS_GRID:" + \
                      '"' + \
                      self.get_filepathname() + \
                      '":' + \
                      self.get_sds_name() + \
                      "' " + \
                      self.get_output_filenames()[counter]
            os.system(command)
            print command
#                      self.get_input_data_filename() + \
            '''

    def set_output_data_units(self,output_data_units):
        """Set data units for the output file.
        
        @param output_data_units : Units of the output data set
        
        """

        self.set_output_convention_units(output_data_units)
        

    def get_output_data_units(self):
        """Get data units for the output file.
        
        """

        return self.output_data_units


    def set_output_projection(self,standard_projection):
        """Set projection of the output data set.
        
        @param standard_projection: Standard projection of the output file
        
        """

        self.output_projection = GeoLocations(standard_projection)
        
        
    def get_output_projection(self):
        """Get projection of the output data set.
        
        """

        return self.output_projection
        
        
    def set_output_bands(self):
        """Set bands of the output data set.
        
        """

        self.output_bands = RasterDataFilePath.get_bands_from_hdf_eos(
                                                        self.get_sds_name())

        if self.get_sds_index()[0] == None:
            sds_index = []
            for counter in range(0,len(self.output_bands)):
                sds_index.append(counter+1)

            self.set_sds_index(sds_index)


    def get_output_bands(self):
        """Get bands of the output data set.
        
        """

        return self.output_bands


    def set_output_convention_units(self, output_data_units):
        """Set convention untis of the output data set.
        
        @param output_data_units: Units of the output data set
        
        """

        self.output_data_units = RasterDataFilePath.get_convention_units(
                                                            output_data_units)

    def set_output_data_conversion_keyword(self):
        """Set data conversion algorithm for the output data set.
        
        """

        if self.get_output_data_units() == 'rd':
            self.output_data_conversion_keyword = 'Radiance'
        if self.get_output_data_units() == 'p0':
            self.output_data_conversion_keyword = 'Reflectance'
        if self.get_output_data_units() == 'dk':
            self.output_data_conversion_keyword = 'BTT'
        if self.get_output_data_units() == 'um':
            self.output_data_conversion_keyword = 'y=a(x-b)'
        if self.get_output_data_units() == 'dl':
            if self.get_sds_name() == '250m 16 days NDVI' or \
               self.get_sds_name() == '250m 16 days EVI' :
                self.output_data_conversion_keyword = 'None'
            else:
                self.output_data_conversion_keyword = 'y=a(x-b)'
        
        if self.output_data_conversion_keyword == 'None':
            self.set_output_data_type('integer')
        else:
            self.set_output_data_type('real')


    def get_output_data_conversion_keyword(self):
        """Get data conversion algorithm for the output data set.
        
        """

        return self.output_data_conversion_keyword


    def set_output_data_type(self,output_data_type):
        """Set data types for the output file.
        
        """

        self.output_data_type = output_data_type


    def get_output_data_type(self):
        """Get data types for the output file.
        
        """

        return self.output_data_type


    def set_output_product(self):
        """Set output data set product.
        
        """

        self.output_product = RasterDataFilePath.get_product_from_hdf_eos(
                                    self.get_sds_name(),
                                    self.get_output_data_units())

    def get_output_product(self):
        """Get output data set product.
        
        """

        return self.output_product


    def set_output_filenames(self):
        """Set output filename.
        
        """
                
        filetype = 'rst'
#        timestep = RasterDataFilePath.get_convention_time(
#                                                self.get_input_data_filename())
        timestep = RasterDataFilePath.get_convention_time(
                                                self.get_filepathname())
        
#        satellite_system = RasterDataFilePath.get_convention_satellite_system(
#                                                self.get_input_data_filename())
        satellite_system = RasterDataFilePath.get_convention_satellite_system(
                                                self.get_filepathname())

        product = self.get_output_product()
        units = self.get_output_data_units()
        resolution = self.get_output_projection().get_projection()[1]
        projection = self.get_output_projection().get_projection()[16]
        
        output_filenames = []
        for counter in range(0, len(self.get_output_bands())):
            band = self.get_output_bands()[counter]
            output_filenames.append(RasterDataFilePath.get_convention_filename(
                    filetype, timestep, satellite_system, product, units,
                    band, resolution, projection))
        self.output_filenames = output_filenames


    def get_output_filenames(self):
        """Get output filename.
        
        """
        
        return self.output_filenames

    
    def write_metadata(self, filename):
        """Write metadata for output file format (Idrisi).
        
        @param filename: Filename of the output data file (Idrisi format)

        """
        title = 'none'
        datatype = self.get_output_data_type()
        filetype="IDRISI Raster A.1"
        ncols = self.get_output_projection().get_projection()[5]
        nrows = self.get_output_projection().get_projection()[6]
        ref_system = self.get_output_projection().get_projection()[17]
        ref_units = self.get_output_data_units()
        unit_distance = 1
        min_x = self.get_output_projection().get_projection()[12]
        max_x = self.get_output_projection().get_projection()[13]
        min_y = self.get_output_projection().get_projection()[14]
        max_y = self.get_output_projection().get_projection()[15]
        min_val = 0
        max_val = 100
        min_disp_val = min_val
        max_disp_val = max_val
        data = None

        idrisi_file = IdrisiDataFile(self.get_output_data_path() + '/' + filename,'rst','w')
        idrisi_file.set_metadata(title,
                     datatype, filetype,
                     ncols, nrows,
                     ref_system, ref_units, unit_distance,
                     min_x, max_x, min_y, max_y,
                     min_val, max_val,
                     min_disp_val, max_disp_val,
                     data)

        idrisi_file.write_meta()
        
        

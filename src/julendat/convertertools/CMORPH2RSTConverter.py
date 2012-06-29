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
        self.set_output_projection("Standard_CMORPH")
        self.set_output_product("pp70")
        self.set_output_data_units("mm")
        self.set_output_bands()
        self.set_output_filenames()
        self.set_output_data_type('real')            
        if self.get_output_projection() != 'Standard_CMORPH':
            self.reproject()
        self.extract()


    def extract(self):
        """Extract CMORPH data and store datasets in individual Idrisi files.
        
        """
        atype = '>f'
        ntype = numpy.float32
        cmorph_file = open(self.get_filepath(), mode='rb')
        daily_sum = numpy.zeros((480,1440), dtype='f')
        for name in self.get_output_filenames():
            print name
            # Read merged microwave precipitation only for actual timestep
            temp = numpy.fromfile(cmorph_file,dtype='<f',count=691200).byteswap()
            # Read CMORPH precipitation estimates for actual timestep
            data = numpy.fromfile(cmorph_file,dtype='<f',count=691200).byteswap()
            data = numpy.reshape(data,(480,1440))
            daily_sum = daily_sum + data
            print data[250,500]
            print daily_sum[250,500]
            print type(data)
            self.write_data(name, data)
        cmorph_file.close()
        self.write_data(self.get_daily_output_filenames(), daily_sum)
            
        

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

        self.output_bands = ["00","03","06","09","12","15","18","21"]

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


    def set_output_data_type(self,output_data_type):
        """Set data types for the output file.
        
        """

        self.output_data_type = output_data_type


    def get_output_data_type(self):
        """Get data types for the output file.
        
        """

        return self.output_data_type


    def set_output_product(self, output_product="None"):
        """Set output data set product.
        
        """

        self.output_product = output_product

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
        
#        satellite_system = RasterDataFilePath.get_convention_satellite_system(
#                                                self.get_input_data_filename())
        satellite_system = RasterDataFilePath.get_convention_satellite_system(
                                                self.get_filepathname())

        product = self.get_output_product()
        units = self.get_output_data_units()
        aggregation = "m1h03"
        resolution = self.get_output_projection().get_projection()[1]
        projection = self.get_output_projection().get_projection()[16]
        
        output_filenames = []
        for hour in self.get_output_bands():
            band = "nb1"
            timestep = RasterDataFilePath.get_convention_time(
                                                self.get_filepathname()) + \
                       hour + "00"
                       
            
            output_filenames.append(RasterDataFilePath.get_convention_filename(
                    filetype, timestep, satellite_system, product, units,
                    band, resolution, projection, aggregation=aggregation))
        self.output_filenames = output_filenames
        
        aggregation = "m1d01"
        timestep = RasterDataFilePath.get_convention_time(
                                                self.get_filepathname())+"0000"
        self.daily_outputfilename = RasterDataFilePath.get_convention_filename(
                    filetype, timestep, satellite_system, product, units,
                    band, resolution, projection, aggregation=aggregation)


    def get_output_filenames(self):
        """Get output filename.
        
        """
        
        return self.output_filenames


    def get_daily_output_filenames(self):
        """Get output filename of daily summed file.
        
        """
        
        return self.daily_outputfilename
    
    def write_data(self, filename, data):
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
        max_val = 30
        min_disp_val = min_val
        max_disp_val = max_val
        idrisi_file = IdrisiDataFile(self.get_output_path() + '/' + filename,'rst','w')
        idrisi_file.set_metadata(title,
                     datatype, filetype,
                     ncols, nrows,
                     ref_system, ref_units, unit_distance,
                     min_x, max_x, min_y, max_y,
                     min_val, max_val,
                     min_disp_val, max_disp_val,
                     data)
        #idrisi_file.write_meta()

        #output = IdrisiDataFile(name,'rst','w')
        #output.set_variable_metadata(scene[0].get_metadata())
        #output.set_array_datatype()
        idrisi_file.write_data(data)

        
        

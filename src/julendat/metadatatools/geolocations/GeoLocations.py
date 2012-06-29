"""Handle standard projections and map areas.
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
__version__ = "2011-11-02"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

#TODO(tnauss): Adjust to julendat

import julendat.metadatatools.raster.RasterDataFilePath as RasterDataFilePath

class GeoLocations(object):
    """Provides access to standart projection information.
    
    Constructor:
    GeoFileProjections(standard_projection)
    
    For Keyword arguments see __init__().
    
    """


    def __init__(self, standard_projection):
        """Constructor of the class.         
        
        @param standard_projection : Standard projection.

        """

        self.set_standard_projection(standard_projection)

    
    
    def set_standard_projection(self, standard_projection):
        """Set standard projection.
        
        @param standard_projection : Standard projection
        
        """
        self.standard_projection = standard_projection
        if self.standard_projection == 'Standard_Germany_00250':
            self.projection_resolution = 250
            self.projection = 'UTM'
            self.zone = 32
            self.hemisphere = 'n'
            self.width = 2672
            self.height = 5612
            self.latitude_min = 42.5312448
            self.latitude_max = 55.2714587
            self.longitude_min = 5.2428681
            self.longitude_max = 15.7260805
            self.projection_datum = 8
            self.coord_xmin = 191425.4100402
            self.coord_xmax = 1053135.0292120
            self.coord_ymin = 4708250.2122994
            self.coord_ymax = 6145637.5305687
            self.convention_projection = \
                    RasterDataFilePath.get_convention_projection(
                                                self.standard_projection)
            self.convention_idrisi_meta_projection = \
                    RasterDataFilePath.get_convention_idrisi_meta_projection_for_utm(
                                                self.zone, self.hemisphere)
            self.epsg = 32632
            self.xresolution = 250
            self.yresolution = 250


        elif self.standard_projection == 'Standard_Germany_00500':
            self.projection_resolution = 500
            self.projection = 'UTM'
            self.zone = 32
            self.hemisphere = 'n'
            self.width= 1336
            self.height = 2806
            self.latitude_min = 42.5312448
            self.latitude_max = 55.2714587
            self.longitude_min = 5.2428681
            self.longitude_max = 15.7260805
            self.projection_datum = 8
            self.coord_xmin = 191425.4100402
            self.coord_xmax = 1053135.0292120
            self.coord_ymin = 4708250.2122994
            self.coord_ymax = 6145637.5305687
            self.convention_projection = \
                    RasterDataFilePath.get_convention_projection(
                                                self.standard_projection)
            self.convention_idrisi_meta_projection = \
                    RasterDataFilePath.get_convention_idrisi_meta_projection_for_utm(
                                                self.zone, self.hemisphere)
            self.epsg = 32632
            self.xresolution = 500
            self.yresolution = 500


        elif self.standard_projection == 'Standard_Germany_01000':
            self.projection_resolution = 1000
            self.projection = 'UTM'
            self.zone = 32
            self.hemisphere = 'n'
            self.width= 668
            self.height = 1403
            self.latitude_min = 42.5312448
            self.latitude_max = 55.2714587
            self.longitude_min = 5.2428681
            self.longitude_max = 15.7260805
            self.projection_datum = 8
            self.coord_xmin = 191425.4100402
            self.coord_xmax = 1053135.0292120
            self.coord_ymin = 4708250.2122994
            self.coord_ymax = 6145637.5305687
            self.convention_projection = \
                    RasterDataFilePath.get_convention_projection(
                                                self.standard_projection)
            self.convention_idrisi_meta_projection = \
                    RasterDataFilePath.get_convention_idrisi_meta_projection_for_utm(
                                                self.zone, self.hemisphere)
            self.epsg = 32632
            self.xresolution = 1000
            self.yresolution = 1000


        elif self.standard_projection == 'Standard_French_Guyana_01000':
            self.projection_resolution = 1000
            self.projection = 'UTM'
            self.zone = 22
            self.hemisphere = 'n'
            self.width= 445
            self.height = 445
            self.latitude_min = 2.0
            self.latitude_max = 6.0
            self.longitude_min = -55.0
            self.longitude_max = -51.0
            self.projection_datum = 8
            self.coord_xmin = 54806.1410180
            self.coord_xmax = 501002.6888716
            self.coord_ymin = 220061.5294647
            self.coord_ymax = 664823.0623228
            self.convention_projection = \
                    RasterDataFilePath.get_convention_projection(
                                                self.standard_projection)
            self.convention_idrisi_meta_projection = \
                    RasterDataFilePath.get_convention_idrisi_meta_projection_for_utm(
                                                self.zone, self.hemisphere)

            self.epsg = 32703
            self.xresolution = 1000
            self.yresolution = 1000

            
        elif self.standard_projection == 'Standard_CMORPH':
            self.projection_resolution = 25000
            self.projection = 'latlong'
            self.zone = ''
            self.hemisphere = ''
            self.width= 1440
            self.height = 480
            self.latitude_min = -60.0
            self.latitude_max = 60.0
            self.longitude_min = -180.0
            self.longitude_max = 180.0
            self.projection_datum = 8
            self.coord_xmin = -180.00
            self.coord_xmax = 180.0
            self.coord_ymin = -60.0
            self.coord_ymax = 60.0
            self.convention_projection = \
                    RasterDataFilePath.get_convention_projection(
                                                self.standard_projection)
            self.convention_idrisi_meta_projection = "latlong"

            self.epsg = 4326
            self.xresolution = 25000
            self.yresolution = 25000            


    def get_projection(self):
        """Set units of data set.
                
        """
        return self.standard_projection, \
               self.projection_resolution, \
               self.projection, \
               self.zone, \
               self.hemisphere, \
               self.width, \
               self.height, \
               self.latitude_min, \
               self.latitude_max, \
               self.longitude_min, \
               self.longitude_max, \
               self.projection_datum, \
               self.coord_xmin, \
               self.coord_xmax, \
               self.coord_ymin, \
               self.coord_ymax, \
               self.convention_projection, \
               self.convention_idrisi_meta_projection, \
               self.epsg, \
               self.xresolution, \
               self.yresolution

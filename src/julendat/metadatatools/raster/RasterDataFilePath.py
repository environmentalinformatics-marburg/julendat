"""Automatic filepath, filename and path generation for raster files.
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

import time
import os
import sys



def get_extension_from_filename(filename):
    """Get extension from filename.
        
    @param filename : Full name of data file 

    """
    extension = os.path.splitext(filename)[1]
    return extension


def get_product_from_filename(filename):
    """Get product information from filename.
        
    @param filename : Full name of data file 

    """
    
    if get_extension_from_filename(filename) == '.hdf':
        product = filename.partition('.')[0]
    return product


def get_convention_time(filename):
    """Convert arbitrary time code to code of convention.
        
    @param filename : Full name of data file 

    """

    if get_extension_from_filename(filename) == '.hdf':
        satellite = get_convention_satellite_system(filename)
        """
        # Info: do not bother abouth satellite - just try/error.
        if satellite == 'ta01m':
            timestep = time.strftime("%Y%m%d%H%M",
                       time.strptime(filename[-34:-22],"%Y%j.%H%M"))
        if satellite == 'aq01m':
            timestep = time.strftime("%Y%m%d%H%M",
                       time.strptime(filename[-36:-22],"%Y%j.h%Hv%M"))
        """
        try:
            timestep = time.strftime("%Y%m%d%H%M",
                       time.strptime(filename[-34:-22],"%Y%j.%H%M"))
        except:
            timestep = time.strftime("%Y%m%d%H%M",
                       time.strptime(filename[-36:-22],"%Y%j.h%Hv%M"))

    return timestep


def get_convention_satellite_system(filename):
    """Convert arbitrary satellite code to code of convention.
        
    @param filename : Full name of data file 

    """
    if get_extension_from_filename(filename) == '.hdf':
        if filename.partition('.')[0][0:3] == 'MOD':
            satellite = 'ta01m'
        elif filename.partition('.')[0][0:3] == 'MYD':
            satellite = 'aq01m'
    return satellite


def get_convention_units(units):
    """Get convention units.
        
    @param units: Units at question. 

    """
    
    if units == 'radiance' or units == 'Radiance':
        units = 'rd'
    if units == 'reflectance' or units == 'Reflectance':
        units = 'p0'
    if units == 'kelvin' or units == 'Kelvin':
        units = 'dk'
    if units == 'micrometer' or units == 'Micrometer':
        units = 'um'
    if units == 'dimensionless' or units == 'Dimensionless':
        units = 'dl'
    
    return units


def get_convention_idrisi_meta_projection_for_utm(zone, hemisphere):
    """Get projection information for Idrisi meta files.
        
    @param zone: Zone of UTM projection. 
    @param hemisphere: Hemisphere of projection. 

    """
    
    if hemisphere == 'n':
        hemisphere = 'n'
    if zone == 32:
        convention_projection = 'utm-32'+'n'
    elif zone == 22:
        convention_projection = 'utm-22'+'n'
    return convention_projection


def get_convention_projection(standard_projection):
    """Get projection information for filename.
        
    @param standard_projection: Name of standard prorjection to be used. 

    """
    
    if standard_projection == 'Standard_Germany_00250':
        convention_projection = 'p32nde'
    elif standard_projection == 'Standard_Germany_00500':
        convention_projection = 'p32nde'
    elif standard_projection == 'Standard_Germany_01000':
        convention_projection = 'p32nde'
    elif standard_projection == 'Standard_French_Guyana_01000':
        convention_projection = 'p22nfg'

    return convention_projection


def get_convention_filename(
        filetype, timestep, satellite_system, product, units, band, resolution, 
        projection, projection_resolution='none', quality='na001'):
    """Get convention filename
        
    @param filetype : File type of the data file 
    @param timestep : Timestep of the data file
    @param satellite_system : Satellite system
    @param product : Product of the data variable
    @param units : Units of the data variable
    @param band : Band (i. e. satellite channel) of the dataset
    @param resolution : Resolution of the data variable
    @param projection : Geographic projection
    @param projection_resolution : Resolution of the geographic projection
    @param quality : Quality of the data variable

    """
    if isinstance(band,str)!=True:
        band = '%03i' % band
    if resolution != 'none':
        if isinstance(resolution,str)!=True:
            projection_resolution = '%06i' % resolution
        else:
            projection_resolution = '00' + resolution
    if projection_resolution == 'none':
        if isinstance(resolution,str)!=True:
            projection_resolution = '%06i' % resolution
        else:
            projection_resolution = '00' + resolution
    if isinstance(resolution,str)!=True:
        resolution = '%04i' % resolution

    filename = timestep + '_' + satellite_system + '_' + product + units + \
               band + '_' + quality + '_' + resolution + '_' + \
               projection + '_' + projection_resolution + '.' + filetype
    return filename


def get_bands_from_hdf_eos(sds_name):
    """Get convention filenames for hdf eos datasets.
  
    @param sds_name : SDS name 
    @param projection : GeoFileProjections object 
    """
    if sds_name == 'EV_250_Aggr1km_RefSB':
        bands = []
        for band_id in range(0,2):
            bands.append(band_id+1)
    elif sds_name == 'EV_500_Aggr1km_RefSB':
        bands = []
        for band_id in range(0,5):
            bands.append(band_id+3)
    elif sds_name == 'EV_1KM_RefSB':
        bands = []
        for band_id in range(0,15):
            bands.append(band_id+8)
        # Correct for band 13h, 13l, 14h, 14l and 26
        bands[5] = '13l'
        bands[6] = '13h'
        bands[7] = '14l'
        bands[8] = '14h'
        bands[14] = 26
    elif sds_name == 'EV_1KM_Emissive':
        bands = []
        for band_id in range(0,6):
            bands.append(band_id+20)
        for band_id in range(6,16):
            bands.append(band_id+21)
    elif sds_name == 'EV_250_Aggr500_RefSB':
        bands = []
        for band_id in range(0,2):
            bands.append(band_id+1)
    elif sds_name == 'EV_500_RefSB':
        bands = []
        for band_id in range(0,5):
            bands.append(band_id+1)
    elif sds_name == 'MOD06':
        bands = []
        for band_id in range(0,1):
            bands.append('nb01')
    elif sds_name == 'Cloud_Effective_Radius':
        bands = []
        for band_id in range(0,1):
            bands.append(band_id+1)
    elif sds_name == 'Cloud_Effective_Radius_1621':
        bands = []
        for band_id in range(0,1):
            bands.append(band_id+1)
    elif sds_name == 'Cloud_Optical_Thickness':
        bands = []
        for band_id in range(0,1):
            bands.append(band_id+1)
    elif sds_name == '250m 16 days NDVI':
        bands = []
        for band_id in range(0,1):
            bands.append(band_id+1)
    elif sds_name == '250m 16 days EVI':
        bands = []
        for band_id in range(0,1):
            bands.append(band_id+1)
    else:
        bands = []
        for band_id in range(0,1):
            bands.append(band_id+1)

    return bands

def get_product_from_hdf_eos(sds_name, data_units=None):
    """Get convention filenames for hdf eos datasets.
  
    @param sds_name : SDS name 
    @param projection : GeoFileProjections object 
    """

    if data_units == 'rd':
        product = 'cr01'
    elif data_units == 'po':
        product = 'ca01'
    elif data_units == 'dk':
        product = 'ct01'
    elif sds_name == 'Cloud_Effective_Radius':
        product = 'py71'
    elif sds_name == 'Cloud_Effective_Radius_1621':
        product = 'py75'
    elif sds_name == 'Cloud_Optical_Thickness':
        product = 'py72'
    elif sds_name == '250m 16 days NDVI':
        product = 'pv71'
    elif sds_name == '250m 16 days EVI':
        product = 'pv72'
    elif sds_name == 'MODIS_Grid_16DAY_250m_500m_VI:250m 16 days EVI':
        product = 'pv72'
    
    return product

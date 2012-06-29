"""Handle Idrisi data files.
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

import array
import numpy
import sys
import datetime
from julendat.filetools.raster.RasterDataFile import RasterDataFile


class IdrisiDataFile(RasterDataFile):
    """'Instance for handling Idrisi data files.

    This instance can be used to handle Idrisi files and their data/metadata.
    """

    def __init__(self, filepath, filetype, io_access="r"):
        """Inits StationInventory.
        
        Args (from class RasterDataFile):
            filepath: Full path and name of the data file.
            filetype: Type of the data file.
            io_access: Read/write access to data file ('r' or 'w').
        """       
        RasterDataFile.__init__(self, filepath, filetype, io_access)
        self.set_metadata_file()
        if self.get_io_access() == 'r':
            self.set_metadata()
            self.set_variable_name()
            self.set_data()

    def set_metadata_file(self, metafilepath=None):
        """Sets full path and name of the metadata file
        
        Args:
            metafilepath: Full path and name to the metadata file (otherwise
                              filename is generated from data filename) 
        """
        if metafilepath is None:
            self.metadata_file = self.get_filepath()[:-4] + '.rdc'
        else:
            self.metadata_file = metafilepath
        self.set_metadata_filename()
        self.set_metadata_path()

    def set_metadata(self, title=None,
                     datatype=None, filetype="IDRISI Raster A.1",
                     ncols=None, nrows=None,
                     ref_system=None, ref_units=None, unit_distance=None,
                     min_x=None, max_x=None, min_y=None, max_y=None,
                     min_val=None, max_val=None,
                     min_disp_val=None, max_disp_val=None,
                     data=None):
        """Sets metadata of an Idrisi raster file.

        Set metadata info in a dictionary. If file access is read, the metadata
        will be read from the Idrisi metadata file.
        
        Args:
            title: Title of the file
            datatype: Datatype of the file
            filetype: Filetype
            ncols: Number of self.ncols
            nrows: Number of self.nrows
            ref_system: Reference system
            ref_units: Reference units
            unit_distance: Unit distance
            min_x: Minimum X coordinate
            max_x: Maximum X coordinate
            min_y: Minimum Y coordinate
            max_y: Maximum Y coordinate
            min_disp_val: Minimum display value
            max_disp_val: Maximum display value
        """
        if self.get_io_access() == 'r':
            self.metadata = self.read_metadata()
        else:
            self.metadata = {}
            self.metadata['title'] = title
            self.metadata['datatype'] = datatype
            self.metadata['filetype'] = filetype
            self.metadata['cols'] = ncols
            self.metadata['rows'] = nrows
            self.metadata['ref_system'] = ref_system
            self.metadata['ref_units'] = ref_units
            self.metadata['unit_distance'] = unit_distance
            self.metadata['min_x'] = min_x
            self.metadata['max_x'] = max_x
            self.metadata['min_y'] = min_y
            self.metadata['max_y'] = max_y
            self.metadata['min_val'] = min_disp_val
            self.metadata['max_val'] = max_disp_val
            self.metadata['min_disp_val'] = min_disp_val
            self.metadata['max_disp_val'] = max_disp_val
        self.set_variable_metadata(self.metadata)
        variable_dimension = {"dim_01" : self.get_variable_metadata()['cols'],\
                              "dim_02": self.get_variable_metadata()['rows']}
        self.set_variable_dimensions(variable_dimension)
        variable_shape = {"rows": self.get_variable_metadata()['rows'], \
                          "cols": self.get_variable_metadata()['cols']}
        self.set_variable_shape(variable_shape)
        self.set_array_datatype()

    def set_variable_name(self, variable_name=None):
        """Sets variable name.
        
        Args:
            variable_name: Name of the data variable (otherwise variable name
                is generated from filename convention)
        """
        if self.get_io_access() == 'r' and variable_name is None:
            self.variable_name = self.get_filepath()[-38:-29]
        else:
            self.variable_name = variable_name
        self.set_variable_names(variable_name)

    def set_timestep(self, timestep=False):
        """Sets variable name.
        
        Args:
            timestep: Time code of the data file (otherwise timecode is 
                generated from file name convention)
        """
        if self.get_io_access() == 'r' and timestep is None:
            self.timestep = datetime.datetime.strptime(
                                self.get_filename()[0:11] + "00","%Y%m%d%H%M%S")
        else:
            self.timestep = datetime.datetime.strptime(timestep,"%Y%m%d%H%M%S")
        self.set_start_timestep(self.get_timestep())
        self.set_end_timestep(self.get_timestep())

    def open_data_file(self):
        """Opens the data file for read/write.
        """
        try:
            if self.get_io_access() == 'r':
                file = open(self.get_filepath(), mode='rb')
            else:
                file = open(self.get_filepath(), mode='wb')
            return file
        except IOError:
            print 'File not found: ' + self.filename
            sys.exit()

    def open_metadata_file(self):
        """Opens the metadata file for read/write.
        """

        try:
            file = open(self.get_metadata_file(),self.get_io_access())
            return file
        except IOError:
            print 'File not found: ' + self.filename
            sys.exit()

    def set_array_datatype(self):
        """Sets array settings with respect to datatype
        """
        if self.get_metadata()['datatype'] == 'byte':
            self.atype = 'B'
            self.ntype = numpy.int8    
        elif self.get_metadata()['datatype'] == 'integer':
            self.atype = 'h'
            self.ntype = numpy.int16
        elif self.get_metadata()['datatype'] == 'real':
            self.atype = 'f'
            self.ntype = numpy.float32

    def get_array_datatype(self):
        """Gets array settings with respect to datatype
        
        Returns:
            Array type.
        """
        return self.atype, self.ntype

    def set_data(self, datavalues=None):
        """Sets numpy array containing the data values
        
        If file access is read and datavlaues is None, the dataset is read
        from the Idrisi file.
        
        Args:
            datavalues: 2D numpy array containing the data values.
        """
        
        if self.get_io_access() == 'r' and datavalues is None:
            self.data = self.read_rasterdata()
        else:
            self.data = datavalues


    def read_metadata(self):
        """Reads metadata from an Idrisi file and return a dictionary.
        
        Args:
            title: Title of the file
            datatype: Datatype of the file
            filetype: Filetype
            ncols: Number of self.ncols
            nrows: Number of self.nrows
            ref_system: Reference system
            ref_units: Reference units
            unit_distance: Unit distance
            min_x: Minimum X coordinate
            max_x: Maximum X coordinate
            min_y: Minimum Y coordinate
            max_y: Maximum Y coordinate
            min_disp_val: Minimum display value
            max_disp_val: Maximum display value

        Thanks to Jan Cermak (http://www.iac.ethz.ch/people/cermakj)
        who counted all the lines.
        """
        metadata = {}
        metadata['name'] = self.set_filename()
        file = self.open_metadata_file()
        for line in file:
            if line.find('file title') != -1:
                metadata['title'] = line[13:].strip()
            elif line.find('data type') != -1:
                metadata['datatype'] = line[13:].strip()
                """
                self.datatype = line[13:].strip()
                if self.datatype == 'real':
                    metadata['datatype'] = 4
                elif self.datatype == 'integer':
                    metadata['datatype'] = 2
                elif self.datatype == 'byte':
                    metadata['datatype'] = 1
                """
            elif line.find('file type') != -1:
                metadata['filetype'] = line[13:].strip()
            elif line.find('columns') != -1:
                metadata['cols'] = int(line[13:].strip())
            elif line.find('rows') != -1:
                metadata['rows'] = int(line[13:].strip())
            elif line.find('ref. system') != -1:
                metadata['ref_system'] = line[13:].strip()
            elif line.find('ref. units') != -1:
                metadata['ref_units'] = line[13:].strip()
            elif line.find('unit dist.') != -1:
                metadata['unit_distance'] = float(line[13:].strip())
            elif line.find('min. X') != -1:
                metadata['min_x'] = float(line[13:].strip())
            elif line.find('max. X') != -1:
                metadata['max_x'] = float(line[13:].strip())
            elif line.find('min. Y') != -1:
                metadata['min_y'] = float(line[13:].strip())
            elif line.find('max. Y') != -1:
                metadata['max_y'] = float(line[13:].strip())
            elif line.find('min. value') != -1:
                metadata['min_disp_val'] = float(line[13:].strip())
            elif line.find('max. value') != -1:
                metadata['max_disp_val'] = float(line[13:].strip())
        file.close()
        return metadata

    def read_rasterdata(self):    
        """Reads data from Idrisi raster file and return a 2D array.
        
        Returns:
            Data of Idrisi file.
        """
        
        atype, ntype = self.get_array_datatype()
        file = self.open_data_file()
        temp = array.array(atype)
        temp.fromfile(file,self.get_metadata()['cols']*self.get_metadata()['rows'])
        file.close()
        data = numpy.array(temp, dtype=ntype)
        data = numpy.reshape(data,(self.get_metadata()['rows'],self.get_metadata()['cols']))
        return data


    def write_meta(self):
        """Writes metadata for an Idrisi raster file.
        """
        linebreak = '\r\n'

        atype, ntype = self.get_array_datatype()
        file = self.open_metadata_file()
        file.write('file format : IDRISI Raster A.1' + linebreak)
        file.write('file title  : ' + self.get_metadata()['title'] + linebreak)
        file.write('data type   : ' + str(self.get_metadata()['datatype']) + linebreak)
        file.write('file type   : binary' + linebreak)
        file.write('columns     : ' + str(self.get_metadata()['cols']) + linebreak)
        file.write('rows        : ' + str(self.get_metadata()['rows']) + linebreak)
        file.write('ref. system : ' + self.get_metadata()['ref_system'] + linebreak)
        file.write('ref. units  : ' + self.get_metadata()['ref_units'] + linebreak)
        file.write('unit dist.  : 1.0000000' + linebreak)
        file.write('min. X      : ' + str(self.get_metadata()['min_x']) + linebreak)
        file.write('max. X      : ' + str(self.get_metadata()['max_x']) + linebreak)
        file.write('min. Y      : ' + str(self.get_metadata()['min_y']) + linebreak)
        file.write('max. Y      : ' + str(self.get_metadata()['max_y']) + linebreak)
        file.write('pos`n error : unknown' + linebreak)
        file.write('resolution  : unknown' + linebreak)
        file.write('min. value  : ' + str(self.get_metadata()['min_val']) + linebreak)
        file.write('max. value  : ' + str(self.get_metadata()['max_val']) + linebreak)
        file.write('display min : ' + str(self.get_metadata()['min_disp_val']) + linebreak)
        file.write('display max : ' + str(self.get_metadata()['max_disp_val']) + linebreak)
        file.write('value units : unspecified' + linebreak)
        file.write('value error : unknown' + linebreak)
        file.write('flag value  : none' + linebreak)
        file.write('flag def`n  : none' + linebreak)
        file.write('legend cats : 0 ' + linebreak)
        file.close()
            
    def write_data(self, datavalues=None):
        """Write data to an Idrisi raster file (including meta data).
        
        Args:
            datavalues: 2D numpy array (if None, self.datavalues is used)
        """
        if datavalues is None:
            datavalues = self.get_data()
        else:
            self.set_data(datavalues)
            
        linebreak = '\r\n'
    
        # Write datavalues from 2D array to Idrisi *.rst file.
        atype, ntype = self.get_array_datatype()
        datavalues = datavalues.astype(ntype)
        file = self.open_data_file()
        temp = self.data.flatten()
        temp.tofile(file)
        file.close()

        # Set metadata
        self.metadata = self.get_variable_metadata()
        self.metadata['min_val'] = min(temp)
        self.metadata['max_val'] = max(temp)
        if self.metadata['min_disp_val'] == self.metadata['max_disp_val']:
            self.metadata['min_disp_val'] = self.metadata['min_val']
            self.metadata['max_disp_val'] = self.metadata['max_val']

        # Write metadata to Idrisi *.rdc file.
        self.write_meta()
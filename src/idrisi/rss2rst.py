"""Convert data from Remote Sensing Systems to Idrisi raster files.
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
__version__ = "2010-08-06"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import numpy
import array
import optparse
import idrisigeofile

#TODO(tnauss): Adjust to julendat.

print
print 'Module: rss2rst'
print 'Version: ' + __version__
print 'Author: ' + __author__
print 'License: ' + __license__
print


def read_rasterdata(scene):    
    '''Read data from Idrisi raster file and return a 2D array.

    read_rasterdata(self)

    '''
    atype = 'B'
    ntype = numpy.int8
    file = open(scene, mode='rb')
    temp = {}
    data = {}
    # wind (m/s), vapor (mm), lwp (mm), rain (mm/h)
    factor = [0.2,0.3,0.01,0.1]
    for i in range(0,4):
        temp[i] = array.array(atype)
        temp[i].fromfile(file,1440*720)
        data[i] = numpy.array(temp[i], dtype=numpy.float32)* factor[i]
        data[i] = numpy.reshape(data[i],(720,1440))
        data[i] = data[i][ ::-1,:]
    file.close()
    return data


# Set framework for command line arguments and define runtime configuration.
parser = optparse.OptionParser("usage: %prog [options] data_file")
parser.add_option("-o", "--out", dest="output_file",
                  help="Full path/name of the output file(s) (can be tuple).",
                  metavar="string")
parser.add_option("-p", "--prd", nargs=1, dest="product",
                  help="Product to be converted.",
                  metavar="string")

parser.set_description('Options for module rss2rst.')
(options, args) = parser.parse_args()

if len(args) != 1:
    parser.print_help()
    parser.error("No input file given.")

# Set filenames and variables
scene = args[0]
print scene
if options.output_file != None: 
    output_file = options.output_file
else:
    output_file = scene
if options.product != None: 
    product = options.product
else:
    product = None

# Read SSMI dataset
print 'Reading rss data..'
data = read_rasterdata(scene)

print 'Writing rss data..'
info = ['wind','vapor','lwp','rain']
maximum_value = [255.0*0.2,255.0*0.3,255.0*0.01,255.0*0.1]
for i in range(0,4):
    output = idrisigeofile.IdrisiGeoFile(
                                    output_file+'_'+info[i]+'.rst','rst','w')
    output.set_data(data[3])
    output.set_metadata(title=info[i],
                datatype='real', filetype='IDRISI Raster A.1',
                ncols=1440, nrows=720,
                ref_system='Latlong', ref_units='Degrees', unit_distance='1',
                min_x=-180.0, max_x=180.0, min_y=-90.0, max_y=90.0,
                min_val=0.0, max_val=maximum_value[i],
                min_disp_val=0.0, max_disp_val=maximum_value[i],data=None)
    output.set_array_datatype()
    output.write_data()


print '...finished.'

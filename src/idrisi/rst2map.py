'''Create publication quality maps from Idrisi raster files.
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
__version__ = "2010-08-06"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import optparse
import numpy
import os
from julendat.plottingtools.Data2Map import Data2Map
from julendat.filetools.raster.idrisi.IdrisiDataFile import IdrisiDataFile


def main():
    '''Main program function
    Create publication quality maps from Idrisi raster files.
    '''
    print
    print 'Module: rst2map'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print


    # Set framework for command line arguments and runtime configuration.
    parser = optparse.OptionParser("usage: %prog [options] data_file " + \
                                   "lat_file lon_file ")
    parser.add_option("-o", dest="output_mapfile",
                      help="Full path/name of the output map(s) (can be tuple).",
                      metavar="string")
    parser.add_option("-y","--lat", nargs=2, dest="lat_range",
                      help="Latitude range for target map",
                      metavar="float", type=float)
    parser.add_option("-x","--lon", nargs=2, dest="lon_range",
                      help="Longitude range for target map",
                      metavar="float", type=float)
    parser.add_option("-v", "--val", nargs=2, dest="value_range",
                      help="Value range to be considered (default: all).",
                      metavar="float", type=float)
    parser.add_option("-l","--label", nargs=1, dest="label",
                      help="Label for map legend",
                      metavar="string")
    parser.add_option("-r","--res", dest="map_resolution",
                      help="Resolution of the map grid [m].",
                      metavar="float", type=float)
    parser.set_description('Options for module rst2map.')
    (options, args) = parser.parse_args()

    if len(args) < 3:
        parser.print_help()
        parser.error("No input and/or lat and/or lon file(s) given.")

    # Set filenames and variables
    act_file = args[0]
    lat_file = args[1]
    lon_file = args[2]
    
    if options.output_mapfile != None: 
        output_mapfile = options.output_mapfile
    else:
        output_mapfile = os.getcwd() + os.sep + "map.png"
    if options.lat_range != None:
        lat_range = (options.lat_range[0],options.lat_range[1])
    else:
        lat_range = None
    if options.lon_range != None:
        lon_range = (options.lon_range[0],options.lon_range[1])
    else:
        lon_range = None
    if options.value_range != None: 
        value_range = (options.value_range)
    else:
        value_range = None
    if options.label != None: 
        label = options.label
    else:
        label = None
    if options.map_resolution != None: 
        map_resolution = options.map_resolution
    else:
        map_resolution = None
    
    # Read datasets and compute map
    print 'Reading latitude/longitude and variable data..'
    lat_data = IdrisiDataFile(lat_file,'r').get_data()
    lon_data = IdrisiDataFile(lon_file,'r').get_data()
    
    act_data = IdrisiDataFile(act_file,'r').get_data()
    
    if value_range is not None:
        act_data = numpy.clip(act_data,value_range[0],value_range[1])

    print 'Initializing map class...'
    map = Data2Map(act_data, lat_data, lon_data, output_mapfile,
                            map_resolution, label, lat_range, lon_range)
    map.compress_data()
    map.plot_map()
    
    print '...finished.'

if __name__ == '__main__':
    main()

"""Convert HDF EOS to Idrisi raster files.
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

import optparse

from hdfeos2rstconverter import HDFEOS2RSTConverter

#TODO(tnauss): Adjust to julendat.

print
print 'Module: mod2rst'
print 'Version: ' + __version__
print 'Author: ' + __author__
print 'License: ' + __license__
print

# Set framework for command line arguments and runtime configuration.
parser = optparse.OptionParser("usage: %prog [options] data_file")
parser.add_option("-o", dest="output_mapfile",
                  help="Full path/name of the output map(s) (can be tuple).",
                  metavar="string")
parser.add_option("-s","--sds", nargs=1, dest="sds_name",
                  help="Name of SDS",
                  metavar="string")
parser.add_option("-d","--du", nargs=1, dest="data_units",
                  help="Output data units",
                  metavar="string")
parser.add_option("-p","--projection", nargs=1, dest="projection",
                  help="Output standard projection",
                  metavar="string")
parser.set_description('Options for module rst2map.')
(options, args) = parser.parse_args()

if len(args) < 1:
    parser.print_help()
    parser.error("No input file given.")

# Set filenames and variables
act_file = args[0]

if options.sds_name != None: 
    sds_name = options.sds_name
else:
    sds_name = None
if options.data_units != None: 
    data_units = options.data_units
else:
    data_units = None
if options.projection != None: 
    projection = options.projection
else:
    projection = None

sds_index = None

#act_file ='/home/modiskette/Desktop/modis/modis/500349202/MYD021KM.A2007272.0500.005.2008190110135.hdf'
#sds_name = 'EV_1KM_RefSB'
#sds_name = 'EV_250_Aggr1km_RefSB'
#sds_name = 'EV_500_Aggr1km_RefSB'
#sds_name = 'EV_1KM_Emissive'
#data_units = 'Radiance'
#projection = 'Standard_French_Guyana_01000'

print projection

hdffile = HDFEOS2RSTConverter(act_file ,'rst','none')
hdffile.convert(sds_name, sds_index, data_units, projection)

print '...finished.'

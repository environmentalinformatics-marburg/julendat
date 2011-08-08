"""Compute statistics with Idrisi raster files.
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
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import numpy
import optparse
import sys
import os
import data2plot
import idrisigeofile
import eumeltools

#TODO(tnauss): Adjust to julendat.

print
print 'Module: rst2plot'
print 'Version: ' + __version__
print 'Author: ' + __author__
print 'License: ' + __license__
print


# Set framework for command line arguments and define runtime configuration.
parser = optparse.OptionParser("usage: %prog [options] data_file")
parser.add_option("-o", "--out", dest="output_file",
                  help="Full path/name of the output file(s) (can be tuple).",
                  metavar="string")
parser.add_option("-a", "--arm", nargs=1, dest="arithmetic",
                  help="Arithmetic to be computed.",
                  metavar="string")
parser.add_option("-v", "--val", nargs=2, dest="value_range",
                  help="Value range to be considered (default: all).",
                  metavar="float", type=float)
"""
parser.add_option("-c", "--col", nargs=2, dest="col_range",
                  help="Col range of dataset included in plot (default: all).",
                  metavar="int", type=int)
parser.add_option("-r", "--row", nargs=2, dest="row_range",
                  help=" range of dataset included in plot (default: all).",
                  metavar="int", type=int)
parser.add_option("-x", "--xlb", dest="xlabel",
                  help="Label for first input file (default: file id).",
                  metavar="string")
parser.add_option("-y", "--ylb", dest="ylabel",
                  help="Label for second input file (default: file id).",
                  metavar="string")
parser.add_option("-t", "--til", nargs=2, dest="title",
                  help="Title for plots (default: file id).",
                  metavar="string")
"""
parser.set_description('Options for module rststatistics.')
(options, args) = parser.parse_args()

if len(args) != 1:
    parser.print_help()
    parser.error("No input file(s) given.")

# Set filenames and variables
scenes ={}
for i in range(len(args)):
    scenes[i] = args[i]
if options.output_file != None: 
    output_file = options.output_file
else:
    output_file = os.getcwd() + os.sep + "output.txt"
if options.value_range != None: 
    value_range = (options.value_range)
else:
    value_range = None
"""
if options.col_range != None: 
    col_range = (options.col_range[0],options.col_range[1]+1)
else:
    col_range = None
if options.row_range != None: 
    row_range = (options.row_range[0],options.row_range[1]+1)
else:
    row_range = None
if options.xlabel != None: 
    xlabel = options.xlabel
else:
    xlabel = None
if options.ylabel != None: 
    ylabel = options.ylabel
else:
    ylabel = None
if options.title != None: 
    title = options.title
else:
    title = None
"""

# Read Idrisi datasets
print 'Reading Idrisi data..'
scene = {}
for i in range(len(scenes)):
    scene[i] = idrisigeofile.IdrisiGeoFile(scenes[i],'rst')

# Set array map with respect to value range
dummy, mask_values, dummy = \
    eumeltools.mask_values((scene[0].get_data()),value_range)

# Set final mask and compress dataset arrays
data = {}
data = numpy.ravel(scene[0].get_data())
data = numpy.compress(mask_values==1,scene[0].get_data())

print "File:               ", scene[0].get_data_filename()
print "Minimum:            ", data.min()
print "Maximum:            ", data.max()
print "Mean:               ", data.mean()
print "Median:             ", numpy.median(data)
print "Standard deviation: ", data.std()

output = open(output_file, "a")
output.write("File:               " + scene[0].get_data_filename() + "\n")
output.write("Minimum:            " + str(data.min()) + "\n")
output.write("Maximum:            " + str(data.max()) + "\n")
output.write("Mean:               " + str(data.mean()) + "\n")
output.write("Median:             " + str(numpy.median(data)) + "\n")
output.write("Standard deviation: " + str(data.std()) + "\n")
output.write("\n")

print '...finished.'

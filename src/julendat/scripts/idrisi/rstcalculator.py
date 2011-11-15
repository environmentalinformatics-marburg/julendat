"""Compute calculations with Idrisi raster files.
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
print 'Module: rstcalculator'
print 'Version: ' + __version__
print 'Author: ' + __author__
print 'License: ' + __license__
print


# Set framework for command line arguments and define runtime configuration.
parser = optparse.OptionParser("usage: %prog [options] data_files")
parser.add_option("-o", "--out", dest="output_file",
                  help="Full path/name of the output file(s) (can be tuple).",
                  metavar="string")
parser.add_option("-a", "--arm", nargs=1, dest="arithmetic",
                  help="Arithmetic to be computed.",
                  metavar="string")
parser.set_description('Options for module rstcalculator.')
(options, args) = parser.parse_args()

if len(args) != 2:
    parser.print_help()
    parser.error("No input file(s) given.")

# Set filenames and variables
scenes ={}
for i in range(len(args)):
    scenes[i] = args[i]
if options.output_file != None: 
    output_file = options.output_file
else:
    output_file = os.getcwd() + os.sep + "output.rst"
if options.arithmetic != None: 
    arithmetic = options.arithmetic
else:
    parser.print_help()
    parser.error("No arithmetic given.")


# Read Idrisi datasets
print 'Reading Idrisi data..'
scene = {}
for i in range(len(scenes)):
    scene[i] = idrisigeofile.IdrisiGeoFile(scenes[i],'rst')

output = idrisigeofile.IdrisiGeoFile(output_file,'rst','w')

if arithmetic == '*':
    print 'Computing multiplication...'
    output.set_data(scene[0].get_data()*scene[1].get_data())
elif arithmetic == '/':
    print 'Computing division...'
    result = scene[0].get_data()/scene[1].get_data()
    result[numpy.isnan(result)]=1
    output.set_data(result)
elif arithmetic == '+':
    print 'Computing addition...'
    output.set_data(scene[0].get_data()+scene[1].get_data())
elif arithmetic == '-':
    print 'Computing substraction...'
    output.set_data(scene[0].get_data()-scene[1].get_data())

output.set_variable_metadata(scene[0].get_metadata())
output.set_array_datatype()
output.write_data()


print '...finished.'

"""Aggregate Idrisi raster files.
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
__version__ = "2012-06-30"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import optparse
import fnmatch
import os

from julendat.filetools.raster.idrisi.IdrisiDataFile import IdrisiDataFile

#TODO(tnauss): Adjust to julendat.

print
print 'Module: rstaggregator'
print 'Version: ' + __version__
print 'Author: ' + __author__
print 'License: ' + __license__
print

def locate(pattern, patternpath, root=os.curdir):
    '''Locate files matching filename pattern recursively
    
    This routine is based on the one from Simon Brunning at
    http://code.activestate.com/recipes/499305/ and extended by the patternpath.
     
    Args:
        pattern: Pattern of the filename
        patternpath: Pattern of the filepath
        root: Root directory for the recursive search
    '''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            # Modified by Thomas Nauss
            if fnmatch.fnmatch(filename, patternpath):
                yield os.path.join(path, filename)

# Set framework for command line arguments and runtime configuration.

parser = optparse.OptionParser("usage: %prog [options] input_path")
parser.add_option("-o", dest="output_path",
                  help="Full path for the output datasets.",
                  metavar="string")
parser.add_option("-t", nargs=2, dest="timeframe",
                  help="Start and end year for aggregation.",
                  metavar="int", type=int)

parser.add_option("-p", dest="filepattern",
                  help="Pattern of filenames to be considered.",
                  metavar="string")
parser.set_description('Options for module cmorph2rst.')
(options, args) = parser.parse_args()

if len(args) < 1:
    parser.print_help()
    parser.error("No input filepath given.")

# Set filenames and variables
input_path = args[0]

if options.output_path != None: 
    output_path = options.output_path
else:
    output_path = input_path

if options.timeframe != None: 
    timeframe = options.timeframe
else:
    timeframe = [2010, 2012]
    
if options.filepattern != None: 
    filepattern = options.filepattern
else:
    filepattern = "*"


for year in range (timeframe[0],timeframe[1]):
    for month in range (1,13):
        act_year = '%04i' % year
        act_month = '%02i' % month 
        filepattern = act_year + act_month + "*m1d01*"
        print filepattern
        cmorph_dataset=locate("*.rst", filepattern, input_path)

        first_run = True
        aggregation = []

        for dataset in cmorph_dataset:
            print " "
            print "Processing dataset ", dataset
            act_file = IdrisiDataFile(dataset,'rst')
            if first_run:
                aggregation = act_file.get_data()
                first_run = False
                output_filename = os.path.basename(dataset)
                output_filename = act_year + act_month + "000000" + \
                                  output_filename[12:29] + \
                                  "m1m01" + \
                                  output_filename[34:]
                output_filepath = output_path + os.sep + \
                                  output_filename

            else:
                aggregation = aggregation + act_file.get_data()
        
            out_file = IdrisiDataFile(output_filepath,'rst','w')
            out_file.set_data(aggregation)
            out_file.set_variable_metadata(act_file.get_metadata())
            out_file.set_array_datatype()
            out_file.write_data()
    
print '...finished.'

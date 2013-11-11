"""Prepare reprosessing of CMORPH binary files.
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

print
print 'Module: cmorph2rst_prepare_reprocess'
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
            if fnmatch.fnmatch(path, patternpath):
                yield os.path.join(path, filename)

# Set framework for command line arguments and runtime configuration.

parser = optparse.OptionParser("usage: %prog [options] input_path")
parser.set_description('Options for module cmorph2rst.')
(options, args) = parser.parse_args()

if len(args) < 1:
    parser.print_help()
    parser.error("No input filepath given.")

# Set filenames and variables
input_path = args[0]

cmorph_dataset=locate("*.Z.done", "*", input_path)
os.chdir(input_path)
for dataset in cmorph_dataset:
    print " "
    print "Processing dataset ", dataset
    cmd = "mv " + dataset + " " + dataset[0:-5]
    os.system(cmd)
     

print '...finished.'

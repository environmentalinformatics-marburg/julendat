"""Process inital logger files from DFG-Kilimanjaro.
Copyright (C) 2011 Thomas Nauss, Tim Appelhans

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

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2010-08-06"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import datetime
import fnmatch
import os

## {{{ http://code.activestate.com/recipes/499305/ (r3)
## Creatied by Simon Brunning
## Modified by Thomas Nauss: add patternpath to check for path.     
def locate(pattern, patternpath, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
## Modified by Thomas Nauss
            if fnmatch.fnmatch(path, patternpath):
## End of Thomas Nauss
                yield os.path.join(path, filename)
## end of http://code.activestate.com/recipes/499305/ }}}

   
def main():
    """Main program function
    Process data from level 0 to level 1.
    """
    print
    print 'Module: ki_prepare_depricated'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    
    input_path = "/home/dogbert/kilimanjaro/incoming/"
    station_dataset=locate("*.asc*", "*", input_path)
    for dataset in station_dataset:
        #print(dataset)
        cmd = "cp " + dataset + " /home/dogbert/kilimanjaro/temp/" + os.path.basename(dataset)
        os.system(cmd)
        cmd = "mv " + dataset + " /home/dogbert/kilimanjaro/processing/logger/noname.bin"
        os.system(cmd)
        cmd = "cp /home/dogbert/kilimanjaro/processing/logger/noname.bin /home/dogbert/kilimanjaro/processing/logger/noname.asc"
        os.system(cmd)
        print dataset
        cmd = "python /home/dogbert/kilimanjaro/scripts/julendat-processing-packages/src/ki_stations/ki_dkstation2level0_gui.py"
        os.system(cmd)

if __name__ == '__main__':
    main()


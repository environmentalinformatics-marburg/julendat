"""Process D&K logger data from level 0 to level 1 (DFG-Kilimanjaro).
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
from julendat.processtools.stations.DKStationLevel02Level1 import \
    DKStationLevel02Level1

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


def configure(config_file):
    """Reads configuration settings and configure object.
    
    Args:
        config_file: Full path and name of the configuration file.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    toplevel_repository_path = config.get('repository', \
                                          'toplevel_repository_path')
    project_id = config.get('project','project_id')
    return toplevel_repository_path, project_id
    
def main():
    """Main program function
    Process data from level 0 to level 1.
    """
    print
    print 'Module: ki_dkstationlevel02level1'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    toplevel_repository_path, project_id = configure(config_file='ki_stations.cnf')
    input_path = toplevel_repository_path + os.sep + project_id
    station_dataset=locate("*.asc", "*ra01_*", input_path)
    for dataset in station_dataset:
        print(dataset)
        systemdate = datetime.datetime.now()
        filepath=dataset
        
        DKStationLevel02Level1(filepath=filepath, config_file='ki_stations.cnf')
        '''
        try:
            DKStationLevel02Level1(filepath=filepath, config_file='ki_stations.cnf')
            move_file = "mv " + dataset + " " + \
                dataset + ".processed." + systemdate.strftime("%Y%m%d%H%M")
            os.system(move_file)
        except Exception as inst:
            print "An error occured with the following dataset."
            print "Some details:"
            print "Filename: " + dataset
            print "Exception type: " , type(inst)
            print "Exception args: " , inst.args
            print "Exception content: " , inst        
        '''
if __name__ == '__main__':
    main()


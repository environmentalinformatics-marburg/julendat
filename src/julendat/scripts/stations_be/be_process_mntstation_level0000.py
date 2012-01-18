"""Move MayerNT logger data to level 0 folder structure (DFG-Exploratories).
Copyright (C) 2011 Thomas Nauss, Insa Otte, Falk Haensel

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

__author__ = "Thomas Nauss <nausst@googlemail.com>, Insa Otte, Falk Haensel"
__version__ = "2012-01-18"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import fnmatch
import os
from julendat.processtools.stations.mntstations.MNTStationToLevel0000 import \
    MNTStationToLevel0000

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


def configure(config_file):
    """Reads configuration settings and configure object.

    Args:
        config_file: Full path and name of the configuration file.
        
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config.get('repository', 'toplevel_incoming_path'), \
           config.get('repository', 'toplevel_temp_path'), \
           config.get('repository', 'toplevel_processing_logger_path')



def main():
    """Main program function
    Move data from initial logger import to level 0 folder structure.
    """
    print
    print 'Module: be_process_mntstation_level0000'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    config_file = "be_config.cnf"
    toplevel_incoming_path, toplevel_temp_path , \
        toplevel_processing_logger_path = configure(config_file)
    
    station_dataset=locate("*.csv*", "*", toplevel_incoming_path)
    for dataset in station_dataset:
        print " "
        print "Processing dataset ", dataset
        cmd = "cp " + dataset + " " + \
            toplevel_temp_path + os.path.basename(dataset)
        os.system(cmd)
        cmd = "mv " + dataset + " " + \
            toplevel_processing_logger_path + os.path.basename(dataset)
        os.system(cmd)
        
        MNTStationToLevel0000(input_filepath=toplevel_processing_logger_path + os.path.basename(dataset), config_file=config_file)

        
if __name__ == '__main__':
    main()
    



"""Prepare reprocessing of level 0200 to level x files (DFG-Exploratories).
Copyright (C) 2013 Thomas Nauss, Tim Appelhans

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
__version__ = "2013-11-12"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import fnmatch
import os
import re

def locate_dir(pattern, root=os.curdir):
    '''Locate folders matching pattern recursively
    
    This routine is based on the one from Andrew Hare at
    http://stackoverflow.com/questions/1548704/delete-multiple-files-matching-a-pattern.
     
    Args:
        root: Root directory for the recursive search
        pattern: Pattern of the filename
    '''
    for path in os.walk(os.path.abspath(root)):
        try:
            if int(path[0][-4:]) >= 200:
                yield path[0]
        except:
            continue
    
def configure(config_file):
    """Reads configuration settings and configure object.

    Args:
        config_file: Full path and name of the configuration file.
        
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config.get('repository', 'toplevel_processing_plots_path')


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
    toplevel_processing_plots_path = configure(config_file)
    
    directories = locate_dir("*_0200", toplevel_processing_plots_path)
    for directory in directories:
        print " "
        print "Deleting ", directory
        cmd = "rm -r " + directory
        print cmd
        os.system(cmd)
        
if __name__ == '__main__':
    main()

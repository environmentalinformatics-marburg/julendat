"""Query throughfall information and store data to level 0 folder structure.
Copyright (C) 2012 Thomas Nauss, Tim Appelhans

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Please send any comments, suggestions, criticism, or (for our sake) bug
reports to nausst@googlemail.com
"""

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2012-09-19"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import fnmatch
import os
import shutil
from datetime import datetime
from julendat.processtools.stations.uistations.EITFStationToLevel0000 import \
    EITFStationToLevel0000


def backup_files(toplevel_processing_logger_path, toplevel_temp_path):
    '''Backup files - just in case.

    Args:
        toplevel_processing_logger_path: Path to backup
        toplevel_temp_path: Path where backup will be stored
    '''
    bu_path = toplevel_temp_path + \
                datetime.now().strftime('%Y%m%d-%H%M%S')
    shutil.copytree(toplevel_processing_logger_path,bu_path)


def configure(config_file):
    """Reads configuration settings and configure object.
    
    Args:
        config_file: Full path and name of the configuration file.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    toplevel_processing_plots_path = config.get('repository', \
                                          'toplevel_processing_plots_path')
    return toplevel_processing_plots_path

def main():
    """Main program function
    Change initial file names to lower case filenames and replace spaces.
    Move data from initial logger import to level 0 folder structure.
    """
    print
    print 'Module: ki_process_dkstation_level0000_gui'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    config_file = "ki_config.cnf"
    toplevel_processing_plots_path = \
        configure(config_file=config_file)
    
    print " "
    print "Processing throughfall dataset..."
    try:
        EITFStationToLevel0000(config_file=config_file)
    except Exception as inst:
        print "An error occured."
        print "Some details:"
        print "Exception type: " , type(inst)
        print "Exception args: " , inst.args
        print "Exception content: " , inst        
    
    print "...finished"
        
if __name__ == '__main__':
    main()


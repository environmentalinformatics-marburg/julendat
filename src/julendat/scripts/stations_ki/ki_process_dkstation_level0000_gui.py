"""Move Driesen and Kern logger data to level 0 folder structure (DFG-Kilimanjaro).
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
__version__ = "2012-01-17"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import fnmatch
import os
import shutil
from datetime import datetime
from julendat.processtools.stations.dkstations.DKStationToLevel0000 import \
    DKStationToLevel0000

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

def backup_files(toplevel_processing_logger_path, toplevel_temp_path):
    '''Backup files - just in case.

    Args:
        toplevel_processing_logger_path: Path to backup
        toplevel_temp_path: Path where backup will be stored
    '''
    bu_path = toplevel_temp_path + \
                datetime.now().strftime('%Y%m%d-%H%M%S%f')
    shutil.copytree(toplevel_processing_logger_path,bu_path)

def remedy_filenames(root=os.curdir):
    '''Rename files to lower case letters and replace spaces.
    
    This routine is based on the one from Simon Brunning at
    http://code.activestate.com/recipes/499305/ and extended by the patternpath.
     
    Args:
        root: Root directory for the recursive search
    '''
    act_datetime = datetime.now().strftime('%Y%m%d-%H%M%S%f')
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in files:
            # Modified by Thomas Nauss
            if len(filename) < 100:
                temp_name = "new_" +  act_datetime + \
                            "_" + filename
            else:
                temp_name = "new_" +  act_datetime + \
                            "_" + filename[50:]
            print path
            print temp_name
            os.rename(os.path.join(path, filename),
                      os.path.join(path, temp_name))
            os.rename(os.path.join(path, temp_name), 
                      os.path.join(path, temp_name.replace (" ", "_").lower()))

def configure(config_file):
    """Reads configuration settings and configure object.
    
    Args:
        config_file: Full path and name of the configuration file.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    toplevel_processing_logger_path = config.get('repository', \
                                          'toplevel_processing_logger_path')
    toplevel_temp_path = config.get('repository', \
                                    'toplevel_temp_path')
    initial_logger_file = config.get('logger','initial_logger_file')
    return toplevel_processing_logger_path, toplevel_temp_path, \
           initial_logger_file

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
    toplevel_processing_logger_path, toplevel_temp_path, initial_logger_file = \
        configure(config_file=config_file)
    
    backup_files(toplevel_processing_logger_path, toplevel_temp_path)
    remedy_filenames(toplevel_processing_logger_path)
    station_dataset = locate("*.bin", "*", toplevel_processing_logger_path)
    
    for dataset in station_dataset:
        print " "
        print "Processing dataset ", dataset
        try:
            binary_logger_filepath = dataset
            ascii_logger_filepath = os.path.dirname(dataset) + os.sep + \
                os.path.basename(dataset).split(".bin")[0] + '.asc'
            DKStationToLevel0000( binary_logger_filepath=binary_logger_filepath, \
                                 ascii_logger_filepath=ascii_logger_filepath, \
                                 config_file=config_file)

        except Exception as inst:
            print "An error occured with the following dataset."
            print "Some details:"
            print "Filename: " + dataset
            print "Exception type: " , type(inst)
            print "Exception args: " , inst.args
            print "Exception content: " , inst        
        
if __name__ == '__main__':
    main()


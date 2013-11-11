"""Upload data to server.
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
along with this program. If not, see <http://www.gnu.org/licenses/>.

Please send any comments, suggestions, criticism, or (for our sake) bug
reports to nausst@googlemail.com
"""

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2013-11-13"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import fnmatch
import os
import shutil
from datetime import datetime
from julendat.processtools.stations.uistations.EITFStationToLevel0000 import \
    EITFStationToLevel0000


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
                
def move_files(source_path, target_path):
    '''Move files - just in case.

    Args:
        source_path: Path to move
        target_path: Path where moved files will be stored
    '''
    print source_path
    print target_path
    if not os.path.exists(target_path): os.makedirs(target_path)
    cmd = 'mv ' + source_path + ' ' + target_path
    os.system(cmd)
    return target_path
    

def zip_files(source_path, target_path):
    '''ZIP files.

    Args:
        source_path: Path to zip
        target_path: Path to zip file
    '''
    target_path = target_path + os.sep + \
                datetime.now().strftime('%Y%m%d-%H%M%S') + '.7z' 
    cmd = '7z a ' + target_path + ' ' + source_path + os.sep + '*'
    os.system(cmd)
    return target_path


def upload_files(source_path, target_path):
    '''ZIP files.

    Args:
        source_path: Path to zip
        target_path: Path to server
    '''
    cmd = 'scp ' + source_path + ' ' + target_path
    os.system(cmd)
    return target_path
    
    
def configure(config_file):
    """Reads configuration settings and configure object.
    
    Args:
        config_file: Full path and name of the configuration file.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    toplevel_processing_plots_path = config.get('repository', \
                                          'toplevel_processing_plots_path')
    project_id = config.get('project', 'project_id')
    toplevel_temp_path = config.get('repository', 'toplevel_temp_path')
    
    return toplevel_processing_plots_path, project_id, toplevel_temp_path

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
    toplevel_processing_plots_path, project_id, toplevel_temp_path = \
        configure(config_file=config_file)
    
    path = toplevel_processing_plots_path + project_id
    print " "
    print "Zipping dataset ", path
    act_file = zip_files(path, path)
    print "Uploading dataset ", act_file
    upload_files(act_file, \
        'eikistations@137.248.191.83:/home/eikistations/ei_data_kilimanjaro/incoming/')
    print "Moving files "
    target_path = toplevel_temp_path + datetime.now().strftime('%Y%m%d-%H%M%S')

    target_path = move_files(path + os.sep + "*", target_path)
    target_path = move_files(target_path + os.sep + os.path.basename(act_file), path)
    print "...finished"
        
if __name__ == '__main__':
    main()


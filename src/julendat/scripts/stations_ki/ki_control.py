"""Control processing of logger data from DFG-Kilimanjaro project.
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
__version__ = "2010-09-26"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import datetime
import fnmatch
import os
from julendat.processtools.stations.DKStationToLevel0010 import \
    DKStationToLevel0010

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
    toplevel_incoming_path = config.get('repository', \
                                          'toplevel_incoming_path')
    toplevel_processing_plots_path = config.get('repository', \
                                          'toplevel_processing_plots_path')
    project_id = config.get('project','project_id')
    return toplevel_incoming_path, toplevel_processing_plots_path, project_id
    
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
    
    #Move ASCII logger files
    toplevel_incoming_path, toplevel_processing_plots_path, project_id = \
        configure(config_file='ki_stations.cnf')
    station_dataset=locate("*.asc", "*ra01_*", toplevel_incoming_path)
    for dataset in station_dataset:
        print "...moving " + dataset + " to"
        len_toplevel_incoming_path = len(toplevel_incoming_path.split("/"))
        parts = dataset.split("/")
        target = toplevel_processing_plots_path + os.sep + project_id
        for part in range(len_toplevel_incoming_path + 1, len(parts)):
            target = target + os.sep + parts[part] 
        print target
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        move_file = "mv " + dataset + " " + target 
        os.system(move_file)

    #Move binary logger files
    station_dataset=locate("*.bin", "*rb01_*", toplevel_incoming_path)
    for dataset in station_dataset:
        print "...moving " + dataset + " to"
        len_toplevel_incoming_path = len(toplevel_incoming_path.split("/"))
        parts = dataset.split("/")
        target = toplevel_processing_plots_path + os.sep + project_id
        for part in range(len_toplevel_incoming_path + 1, len(parts)):
            target = target + os.sep + parts[part] 
        print target
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        move_file = "mv " + dataset + " " + target 
        os.system(move_file)

    #Move conflict folder to todo destination
    station_dataset=locate("*.asc.*", "*conflict*", toplevel_incoming_path)
    for dataset in station_dataset:
        len_toplevel_incoming_path = len(toplevel_incoming_path.split("/"))
        len_toplevel_processing_plots_path = len(toplevel_processing_plots_path.split("/"))
        source_parts = dataset.split("/")
        source = ""
        for part in range(len_toplevel_incoming_path + 2):
            source = source + os.sep + source_parts[part]
        print "...moving " + source + " to"
        target_parts = toplevel_processing_plots_path.split("/")
        target = ""
        for part in range(len_toplevel_processing_plots_path - 1):
            target = target + os.sep + target_parts[part] 
        target = target + os.sep + "todo" + \
            os.sep + source_parts[len_toplevel_incoming_path] + os.sep
        print target
        os.mkdir(target)
        move_file = "mv " + source + " " + target 
        os.system(move_file)

if __name__ == '__main__':
    main()


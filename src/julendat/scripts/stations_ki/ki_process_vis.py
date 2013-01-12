"""Visualize level 0050 datasets
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
import datetime
import fnmatch
import os
from julendat.processtools.vis.VISLevel0050 import VISLevel0050

def configure(config_file):
    """Reads configuration settings and configure object.
    
    Args:
        config_file: Full path and name of the configuration file.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    toplevel_processing_plots_path = config.get('repository', \
                                          'toplevel_processing_plots_path')
    project_id = config.get('project','project_id')
    r_filepath = config.get('general', 'r_filepath')
    return toplevel_processing_plots_path, project_id, r_filepath

    
def main():
    """Main program function
    Process data from level 0000 to level 0050.
    """
    print
    print 'Module: ki_process_dkstation_level0050'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    config_file = "ki_config.cnf"
    toplevel_processing_plots_path, project_id, r_filepath = \
        configure(config_file=config_file)
    
    VISLevel0050(config_file=config_file, pattern="*fah01_0300.dat", \
                 loggers = ['wxt'])
    print "Finished"        

if __name__ == '__main__':
    main()

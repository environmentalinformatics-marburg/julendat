"""Aggragate station data by time.
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
from julendat.processtools.stations.dkstations.DKStationToLevel0050 import \
    DKStationToLevel0050

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
    input_path = toplevel_processing_plots_path + project_id
    
    station_dataset=locate("*.dat", "*ca05_cti05_0050*", input_path)
    
    for dataset in station_dataset:
        print " "
        print "Processing dataset ", dataset


# write.aggregate.ki.data("C:/tappelhans/uni/marburg/kili/testing/kili_data/ki_0000cof3_000wxt_201112010000_201112312355_eat_ca05_cti05_0005.dat",
#                         "c:/tappelhans/

        os.chdir(r_filepath)
        r_source = 'source("write.aggregate.ki.data.R")'
        r_script = 'write.aggregate.ki.data('
        r_inputfilepath = 'inputfilepath = "' + dataset + '",'
        r_outputfilepath = 'outputfilepath = "' + dataset + "_test" + '",'
        r_level = 'level = "month"' 
        
        r_cmd = r_source + "\n" + \
                r_script + "\n" + \
                r_inputfilepath + "\n" + \
                r_outputfilepath + "\n" + \
                r_level + ")\n"
        
        r_script = "aggregate0050.rscript" 
        f = open(r_script,"w")
        f.write(r_cmd)
        f.close()
        r_cmd = "R CMD BATCH " + r_script + " " + r_script + ".log"
        os.system(r_cmd)
        
if __name__ == '__main__':
    main()


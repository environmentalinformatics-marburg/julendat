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
    print 'Module: be_process_dkstation_level0050'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    config_file = "be_config.cnf"
    toplevel_processing_plots_path, project_id, r_filepath = \
        configure(config_file=config_file)
    
    VISLevel0050(config_file=config_file)
    '''
    input_path = toplevel_processing_plots_path + project_id
    print input_path
    os.chdir(r_filepath)
    r_source = 'source("print.be.strip.R")'
    r_script = 'print.be.strip('
    r_inputpath = 'inputpath = "' + input_path + '",'
    r_logger = 'logger = "rug",'
    r_prm = 'prm = "Ta_200",'
    r_fun = 'fun = mean,'
    r_arrange = 'arrange = "long",'
    r_range = 'range = c(0, 40),'
    r_pattern = 'pattern  = "*cti05_0050.dat",'
    r_colour = 'colour = VColList$Ta_200,'
    r_year = 'year = "2011"'
    
    r_cmd = r_source + "\n" + \
            r_script + "\n" + \
            r_inputpath + "\n" + \
            r_logger + " \n" + \
            r_prm + " \n" + \
            r_fun + " \n" + \
            r_arrange + " \n" + \
            r_range + " \n" + \
            r_pattern + " \n" + \
            r_colour + " \n" + \
            r_year + ")\n"
    
    r_script = "vis0050.rscript" 
    f = open(r_script,"w")
    f.write(r_cmd)
    f.close()
    r_cmd = "R CMD BATCH " + r_script + " " + r_script + ".log"
    print r_cmd
    os.system(r_cmd)
    '''
    print "Finished"        

if __name__ == '__main__':
    main()

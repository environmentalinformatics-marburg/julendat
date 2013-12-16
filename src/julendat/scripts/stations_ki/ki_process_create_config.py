"""Create config file for Kilimanjaro processing
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

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2013-08-20"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import os
from optparse import OptionParser

def main():
    """Main program function
    Create ki_config.cnf
    """
    print
    print 'Module: ki_process_create_config'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    parser = OptionParser()
    parser.add_option('-p', '--path', 
                  dest = "top_level_path", 
                  default = os.getcwd(),
                  )
    (options, args) = parser.parse_args()
    
    config_filepath = "ki_config.cnf"

    top_level_path = options.top_level_path  
    r_filepath = os.path.dirname(os.path.dirname(os.getcwd())) + \
        os.sep + 'rmodules'
    content = '[logger]\n' + \
              'initial_logger_file = noname.bin \n' + \
              'logger_time_zone = mez \n' + \
              'station_entries = dk_station_entries.cnf \n' + \
               '\n' + \
               '[repository] \n' + \
              'toplevel_path = '+ top_level_path + '\n' + \
              'toplevel_incoming_path = '+ top_level_path + 'incoming/' \
                + '\n' + \
              'toplevel_check_path = '+ top_level_path + 'incoming/check/' \
                + '\n' + \
              'toplevel_checked_path = '+ top_level_path + 'incoming/checked/' \
                              + '\n' + \
              'toplevel_processing_plots_path = ' + top_level_path + \
                'processing/plots/' + '\n' + \
              'toplevel_processing_logger_path = '+ top_level_path + 'processing/logger/\n' + \
              'toplevel_vis_path = '+ top_level_path + 'processing/vis/' + \
                '\n' + \
              'toplevel_temp_path = '+ top_level_path + 'temp/' + '\n' + \
               '\n' + \
               '[inventory] \n' + \
               'station_inventory = ki_config_station_inventory.cnf \n' + \
               'station_master = station_master.csv \n' + \
               '\n' + \
               '[project] \n' + \
               'project_id = ki \n' + \
               'level_0005_timezone = eat \n' + \
               '\n' + \
               '[general] \n'  + \
               'level0050_standards = ki_config_level0050_standards.cnf \n' + \
               'r_filepath = ' + r_filepath + '\n'
    
    config_file = open(config_filepath, 'w')
    config_file.write(content)
    config_file.close()

                  
if __name__ == '__main__':
    main()


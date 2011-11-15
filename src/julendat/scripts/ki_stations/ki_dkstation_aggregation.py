"""Aggregate logger data (DFG-Kilimanjaro).
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
__version__ = "2010-10-02"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import datetime
import fnmatch
import os
from julendat.processtools.resampling.stations.StationAggregation import \
    StationAggregation

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

def configure(config_file_path, config_file_variables):
    """Reads configuration settings and configure object.

    Args:
        config_file_path: Configuration file for path variables
        config_file_values: Configuration file for data values
        
    """
    config_file = config_file_path
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    toplevel_repository_path = config.get('repository', \
                                          'toplevel_repository_path')
    project_id = config.get('project','project_id')
    r_filepath = config.get('general', 'r_filepath')

    config_file = config_file_variables
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    variables = config.items('variables')

    return toplevel_repository_path, project_id, r_filepath, variables
        
def main():
    """Main program function
    Process data from level 0 to level 1.
    """
    print
    print 'Module: ki_dkstation_aggregation'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    toplevel_repository_path, project_id, r_filepath, variables = \
        configure(config_file_path='ki_stations.cnf', \
                  config_file_variables='ki_station_variables.cnf')
    
    input_path = toplevel_repository_path + os.sep + project_id
    station_dataset=locate("*.dat", "*ca01_nai05_0010*", input_path)
    # Daily aggregation
    for dataset in station_dataset:
        print(dataset)
        systemdate = datetime.datetime.now()
        StationAggregation(input_filepath=dataset, \
                               input_variables=variables, \
                               r_filepath=r_filepath, \
                               aggregation_mode="auto", \
                               output_start_time='20110401000000', \
                               output_end_time = '20110430235500', \
                               output_time_step = '3600')
        '''
        try:
            StationAggregation(input_filepath=dataset, \
                               input_variables=variables, \
                               r_filepath=r_filepath, \
                               run_mode="auto", \
                               output_start_time='20110401000000', \
                               output_end_time = '20110430235500', \
                               output_time_step = '3600')
        except Exception as inst:
            print "An error occured with the following dataset."
            print "Some details:"
            print "Filename: " + dataset
            print "Exception type: " , type(inst)
            print "Exception args: " , inst.args
            print "Exception content: " , inst        
        '''
if __name__ == '__main__':
    main()


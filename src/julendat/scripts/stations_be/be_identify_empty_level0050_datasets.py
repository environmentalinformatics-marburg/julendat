"""Identify and mark empty level 0050 files (DFG-Exploratories).
Copyright (C) 2011 Thomas Nauss, Insa Otte, Falk Haensel

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
__version__ = "2012-02-11"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import fnmatch
import os

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
    return config.get('repository', 'toplevel_processing_plots_path'), \
           config.get('project', 'project_id')

def main():
    """Main program function
    Move data from initial logger import to level 0 folder structure.
    """
    print
    print 'Module: be_identify_empty_level0050_datasets'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    config_file = "be_config.cnf"
    toplevel_processing_plots_path, project_id  = configure(config_file)
    
    dataset =locate("*0050.dat", "*", toplevel_processing_plots_path + \
                    project_id)
    for dataset in dataset:
        #print " "
        #print "Checking dataset ", dataset
        infile = open(dataset, "r")
        data_line = False
        first_line = True
        for line in infile:
            if len(line) > 23 and first_line == False:
                data_line = True
            first_line = False
        infile.close()
        if data_line == False:
            print "Marking empty dataset ", dataset
            cmd = "mv " + dataset + " " + dataset + ".empty"
            os.system(cmd)
    
    print "...finished."          
        
if __name__ == '__main__':
    main()
    

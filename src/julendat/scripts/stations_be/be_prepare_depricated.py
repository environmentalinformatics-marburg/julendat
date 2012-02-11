"""Prepare reprocessing of level 0000 to level 0050 files (DFG-Exploratories).
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
__version__ = "2012-02-06"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import fnmatch
import string
from datetime import datetime
import os
import csv
from julendat.processtools.stations.mntstations.MNTStationToLevel0000 import \
    MNTStationToLevel0000

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
    return config.get('repository', 'toplevel_check_path'), \
           config.get('repository', 'toplevel_checked_path')

def check_csv_type(dataset):
    be_standard = None
    infile = open(dataset, "r")
    
    identified_csv_type = False
    be_standard = False
    counter = 1
    while identified_csv_type == False:
        counter = counter + 1
        line = infile.next()
        try:
            date = datetime.strptime(\
                   string.strip(line[0:19]), \
                   "%d.%m.%Y %H:%M:%S")
            if line[19] == ";":
                be_standard = True
            if line[19] == ",":
                be_standard = False
            identified_csv_type = True
        except:
            try:
                date = datetime.strptime(\
                       string.strip(line[0:16]), \
                       "%d.%m.%Y %H:%M")
                if line[16] == ";":
                    be_standard = True
                if line[16] == ",":
                    be_standard = False
                identified_csv_type = True
            except:
                continue

    infile.close()
    return be_standard

def main():
    """Main program function
    Move data from initial logger import to level 0 folder structure.
    """
    print
    print 'Module: be_process_mntstation_level0000'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print   
    
    config_file = "be_config.cnf"
    toplevel_check_path, toplevel_checked_path  = configure(config_file)
    
    station_dataset=locate("*.csv*", "*", toplevel_check_path)
    if os.path.exists(toplevel_checked_path) != True:
        os.mkdir(toplevel_checked_path)
    for dataset in station_dataset:
        print " "
        print "Preparing dataset ", dataset
        be_standard = check_csv_type(dataset)
        print "BE Standard ", be_standard
        infile = open(dataset)        
        outfile = open(toplevel_checked_path + os.path.basename(dataset), "w")
        empty_line = 0
        last_line = None
        for line in infile:
            if be_standard == True:
                outline = line
            else:
                outline = line.replace(',',';')
                try:
                    date = datetime.strptime(\
                           string.strip(outline.split(';')[0][0:19]), \
                           "%d.%m.%Y %H:%M:%S")
                    date = outline.split(';')[0][0:19]
                    rest = outline.replace('.',',')
                    rest = rest.split(';')[1:]
                    outline = date + ";" + ('; '.join(str(i) for i in rest))
                except:
                    try:
                        date = datetime.strptime(\
                           string.strip(outline.split(';')[0][0:16]), \
                           "%d.%m.%Y %H:%M")
                        date = outline.split(';')[0][0:16]
                        rest = outline.replace('.',',')
                        rest = rest.split(';')[1:]
                        outline = date + ";" + ('; '.join(str(i) for i in rest))
                    except:
                        outline = line.replace(',',';')
                        outline = outline.replace('.',',')

            if len(outline) <= 2:
                empty_line = empty_line + 1
                if empty_line <= 1:
                    outfile.write(outline)
            elif string.count(outline, ';') == (len(outline)-2):
                empty_line = empty_line + 1
                if empty_line <= 1:
                    outfile.write(outline)
            else:
                outfile.write(outline)
                
            
if __name__ == '__main__':
    main()
    

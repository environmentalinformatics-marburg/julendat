"""Process D&K logger data from level 0 to level 1 (DFG-Kilimanjaro).
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
__version__ = "2010-08-06"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

from julendat.processtools.stations.DKStationLevel02Level1 import \
    DKStationLevel02Level1

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
    
    filepath = '/media/permanent/development/test/kilimanjaro/metstations/plots/ki/0000cof3/ra01_nai05_0000/ki_0000cof3_pu1_201106230955_201107071350_mez_ra01_nai05_0000.asc' 
    DKStationLevel02Level1(filepath=filepath, config_file='ki_stations.cnf')
        
if __name__ == '__main__':
    main()


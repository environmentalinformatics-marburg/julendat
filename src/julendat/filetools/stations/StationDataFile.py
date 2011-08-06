'''
Class for station data files.
Copyright (C) 2011 Thomas Nauss

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

@author: Thomas Nauss
@license: GNU General Public License
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>"
__version__ = "2010-08-04    "
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."

import os
from julendat.filetools.DataFile import DataFile
from julendat.metadatatools.stations.StationDataFilename \
    import StationDataFilename

class StationDataFile(DataFile):

    def set_filename(self):
        '''Set name of the data file.
        
        '''

        self.data_filename = StationDataFilename(\
                            filename=os.path.split(self.get_file())[1]) 
        



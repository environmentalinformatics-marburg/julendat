"""Handle station inventory files.
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
"""

__author__ = "Thomas Nauss <nausst@googlemail.com>"
__version__ = "2011-11-02"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

from julendat.filetools.stations.StationDataFile import StationDataFile


class StationInventoryFile(StationDataFile):
    """Instance for handling station inventory files.

    This instance can be used to handle station data files which is a
    defined combination of one or more sensors and one logger.
    This is also an abstract class for defining station data file functions.
    """
    pass
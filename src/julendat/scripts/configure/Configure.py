"""Auto-configure settings
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
__version__ = "2011-11-25"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import os

class Configure:
    """Instance for moving downloaded D&K logger data to level 0 folders.
    """

    def __init__(self):
        """Inits Configure.
        The instance is initialized by reading a configuration file and the 
        initialization of the proprietary station data file instance.
        If the run mode is set to "auto-gui", this is followed by an automatic
        configuration of filenames and filepathes and the movement of the
        station data file to the processing path structure.  
        
        Args:
            config_file: Configuration file.
            run_mode: Running mode (auto-gui, manual)
        """
        

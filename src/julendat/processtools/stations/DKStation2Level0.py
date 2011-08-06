'''
Move downloaded logger data to level 0 folder structure.
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

@author: Thomas Nauss, Tim Appelhans
@license: GNU General Public License
'''

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2010-08-04    "
__license__ = "GNU GPL, see http://www.gnu.org/licenses/."


import ConfigParser
from julendat.filetools.stations.dkstations.DKStationDataFile import DKStationDataFile
import os
import shutil
from julendat.metadatatools.stations.StationDataFilename import StationDataFilename
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.guitools.stations.GUIAutoPlotSelection import GUIAutoPlotSelection
from julendat.guitools.stations.GUIManualPlotSelection import GUIManualPlotSelection
import Tkinter

class DKStation2Level0:   
    """ Move data from initial logger import to level 0 folder structure.
    
    Constructor:
    DataFile(filepath="None", filetype="None", io_access="r")
    
    For Keyword arguments see __init__().
    
    """

    def __init__(self, configFile,runmode="auto-gui"):
        '''Constructor of the class.         

        __init__(self, file, filetype,io_access="r")
        
        @param file: Full path and name of the data file.
        @param filetype: Type of the data file.
        @param io_access: Read/write access to data file ('r' or 'w').

        '''

        self.set_runmode(runmode)
        self.configure(configFile)
        self.init_StationFile()
        if self.get_runFlag():
            self.autoconfigure()
        self.run()
            
    def run(self):
        '''Execute class functions according to runmode settings. 
        
        '''
        if self.get_runmode() == "manual":
            pass
        elif self.get_runmode() == "auto-gui":
            self.auto_gui()

    def auto_gui(self):
        '''Execute class functions in default auto-gui mode.
        
        '''
        if self.get_runFlag():
            gui = Tkinter.Tk()
            gui.title("Just to be sure...")
            gui.geometry('600x350+50+50')
            intro = "\n Please read very carefully. \n"
            question = "Are you standing on plot " + self.get_plotID() + "?"
            outro = "\n Press only <Yes> if you are sure."  + \
                    "\n If you press <No> you can specify the location manually.\n" 
            app = GUIAutoPlotSelection(gui,intro=intro,question=question,outro=outro)
            gui.mainloop()
            correct_plotID =  app.get_correct_plotID()
            gui.destroy()        
        
            if correct_plotID != True:
                plotID_list = ["cof1", "cof2", "cof3", "cof4", "not sure"]
                gui = Tkinter.Tk()
                gui.title("Just to be really sure...")
                gui.geometry('600x350+50+50')
                app = GUIManualPlotSelection(gui, plotID_list)
                gui.mainloop()
                gui.destroy()
                manual_plotID = app.get_correct_plotID()
        
                if manual_plotID == "not sure":
                    plotID = "xx000000"
                    postexflag="autoplot_" + self.get_plotID()
                else:
                    plotID = "xx" + manual_plotID
                    postexflag="autoplot_" + self.get_plotID()
            
                self.set_level0_filenames(projectID="ki", \
                    plotID=plotID,postexflag=postexflag)
            
            else:
                self.set_level0_filenames(projectID="ki")

            self.main()
        
        else:
            print "Nothing to do..."
            print "...finished."        
        

    def set_runmode(self,runmode):
        '''Set run mode.
        
        @param runmode: Running mode (default: auto-gui)
        '''
        self.runmode = runmode

    def get_runmode(self):
        '''Get run mode.
        '''
        return self.runmode

    def configure(self,configFile):
        '''Read configuration settings and configure object.
    
        @param configFile: Full path and name of the configuration file.
        '''
        self.configFile = configFile
        config = ConfigParser.ConfigParser()
        config.read(self.configFile)
        self.logger_file = config.get('logger', 'initial_logger_file')
        self.tl_data_path = config.get('repository', 'toplevel_repository_path')
        self.ki_station_inventory = config.get('inventory','ki_station_inventory')


    def init_StationFile(self):
        '''Initialize D&K station data file.
        '''
        try:
            self.loggerDataFile = DKStationDataFile(self.logger_file)
            self.runFlag = self.loggerDataFile.get_asciiFileExists()
        except:
            self.runFlag = False 

    def move_data(self):
        '''Move files.
        '''
        shutil.move(self.source,self.destination)

    def autoconfigure(self):
        '''Set necessary attributes automatically.
        '''

        inventory = StationInventory(self.ki_station_inventory)
        self.plotID, self.loggerID = \
            inventory.get_Inventory_from_serialNumber( \
                self.loggerDataFile.get_serialNumber())
        self.time_range = self.loggerDataFile.get_timeRange()

    def get_runFlag(self):
        '''Get runtime flag information.
        '''
        return self.runFlag

    def get_plotID(self):
        '''Get runtime flag information.
        '''
        return self.plotID
    
    def set_level0_filenames(self,projectID=None, \
                             plotID=None,postexflag=None):
        '''Set level0 filenames and path information
        '''
        if plotID == None:
            plotID = self.plotID

            
        self.filenames = StationDataFilename(\
                        toplevel_path=self.tl_data_path, \
                        projectID=projectID, \
                        plotID=plotID, \
                        stationType=self.loggerID, \
                        startTime=self.time_range[0], \
                        endTime=self.time_range[1], \
                        aggregation="nai"+str(self.time_range[1]), \
                        postexflag=postexflag)  
        self.filenames.set_filenameDictionary()

    def main(self):
        '''Map logger files to level 0 filename and directory structure.
        '''

        print self.filenames.get_filenameDictionary()["level_000_bin-filename"]
        print self.filenames.get_filenameDictionary()["level_000_bin-path"]
        print self.filenames.get_filenameDictionary()["level_000_bin-file"]
        print self.filenames.get_filenameDictionary()["level_001_ascii-filename"]
        print self.filenames.get_filenameDictionary()["level_001_ascii-path"]
        print self.filenames.get_filenameDictionary()["level_001_ascii-file"]

        # Check if path for level 0 files exists, otherwise create it        
        if not os.path.isdir(self.filenames.get_filenameDictionary()["level_000_bin-path"]):
            os.makedirs(self.filenames.get_filenameDictionary()["level_000_bin-path"])
        if not os.path.isdir(self.filenames.get_filenameDictionary()["level_001_ascii-path"]):
            os.makedirs(self.filenames.get_filenameDictionary()["level_001_ascii-path"])
        
        # Set full path and names of ASCII data files and move them
        self.source = self.loggerDataFile.asciiFile.get_file()
        self.destination =  self.filenames.get_filenameDictionary()["level_001_ascii-file"]
        print self.source
        print self.destination
        self.move_data()
        
        if os.path.isfile(self.loggerDataFile.binFile.get_file()) and self.loggerDataFile.get_asciiFileExists():
            # Move binary data
            self.source = self.loggerDataFile.binFile.get_file()
            self.destination = self.filenames.get_filenameDictionary()["level_000_bin-file"]
            print self.source
            print self.destination
            self.move_data()

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
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
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
        self.initial_logger_file = config.get('logger', 'initial_logger_file')
        self.tl_data_path = config.get('repository', 'toplevel_repository_path')
        self.ki_station_inventory = config.get('inventory','ki_station_inventory')

    def init_StationFile(self):
        '''Initialize D&K station data file.
        '''
        try:
            self.binary_logger_file = DKStationDataFile(\
                                      filepath=self.initial_logger_file)

            ascii_file_exsists = False
            ascii_file = self.binary_logger_file.get_filepath()[:-3] + "asc"
            if os.path.isfile(ascii_file):
                ascii_file_exsists = True
            else:
                ascii_file = self.binary_logger_file.get_filepath()[:-3] + "ASC"
                if os.path.isfile(ascii_file):
                    ascii_file_exsists = True
            if ascii_file_exsists == True:
                self.ascii_logger_file = DKStationDataFile(\
                                         filepath=ascii_file)
                self.runFlag = self.ascii_logger_file.get_file_exists()
            else:
                self.runFlag = False

        except:
            self.runFlag = False

    def get_runFlag(self):
        '''Get runtime flag information.
        '''
        return self.runFlag

    def autoconfigure(self):
        '''Set necessary attributes automatically.
        '''
        inventory = StationInventory(filepath=self.ki_station_inventory, \
                    serial_number = self.ascii_logger_file.get_serial_number())
        self.plot_id = inventory.get_plot_id()
        self.station_id = inventory.get_station_id()
        self.time_range = self.ascii_logger_file.get_time_range()


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
            question = "Are you standing on plot " + self.get_plot_id() + "?"
            outro = "\n Press only <Yes> if you are sure."  + \
                    "\n If you press <No> you can specify the location manually.\n" 
            app = GUIAutoPlotSelection(gui,intro=intro,question=question,outro=outro)
            gui.mainloop()
            correct_plot_id = app.get_correct_plot_id()
            gui.destroy()        
        
            if correct_plot_id != True:
                plot_id_list = ["cof1", "cof2", "cof3", "cof4", "not sure"]
                gui = Tkinter.Tk()
                gui.title("Just to be really sure...")
                gui.geometry('600x350+50+50')
                app = GUIManualPlotSelection(gui, plot_id_list)
                gui.mainloop()
                gui.destroy()
                manual_plot_id = app.get_correct_plot_id()
        
                if manual_plot_id == "not sure":
                    plot_id = "xx000000"
                    postexflag="autoplot_" + self.get_plot_id()
                else:
                    plot_id = "xx" + manual_plot_id
                    postexflag="autoplot_" + self.get_plot_id()
            
                self.set_level0_filenames(project_id="ki", \
                    plot_id=plot_id,postexflag=postexflag)
            
            else:
                self.set_level0_filenames(project_id="ki")

            self.main()
        
        else:
            print "Nothing to do..."
            print "...finished."        
        




    def move_data(self):
        '''Move files.
        '''
        shutil.move(self.source,self.destination)



    def get_plot_id(self):
        '''Get runtime flag information.
        '''
        return self.plot_id
    
    def set_level0_filenames(self,project_id=None, \
                             plot_id=None,postexflag=None):
        '''Set level0 filenames and path information
        '''
        if plot_id == None:
            plot_id = self.plot_id

            
        self.filenames = StationDataFilePath(\
                        toplevel_path=self.tl_data_path, \
                        project_id=project_id, \
                        plot_id=plot_id, \
                        station_id=self.station_id, \
                        start_time=self.time_range[0], \
                        end_time=self.time_range[1], \
                        aggregation="nai"+str(self.time_range[2]), \
                        postexflag=postexflag)  
        self.filenames.build_filename_dictionary()

    def main(self):
        '''Map logger files to level 0 filename and directory structure.
        '''

        print self.filenames.get_filename_dictionary()["level_000_bin-filename"]
        print self.filenames.get_filename_dictionary()["level_000_bin-path"]
        print self.filenames.get_filename_dictionary()["level_000_bin-filepath"]
        print self.filenames.get_filename_dictionary()["level_001_ascii-filename"]
        print self.filenames.get_filename_dictionary()["level_001_ascii-path"]
        print self.filenames.get_filename_dictionary()["level_001_ascii-filepath"]

        # Check if path for level 0 files exists, otherwise create it        
        if not os.path.isdir(self.filenames.get_filename_dictionary()["level_000_bin-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()["level_000_bin-path"])
        if not os.path.isdir(self.filenames.get_filename_dictionary()["level_001_ascii-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()["level_001_ascii-path"])
        
        # Set full path and names of ASCII data files and move them
        self.source = self.ascii_logger_file.get_filepath()
        self.destination =  self.filenames.get_filename_dictionary()["level_001_ascii-filepath"]
        print self.source
        print self.destination
        self.move_data()
        
        if os.path.isfile(self.binary_logger_file.get_filepath()) and \
                          self.ascii_logger_file.get_file_exists():
            # Move binary data
            self.source = self.binary_logger_file.get_filepath()
            self.destination = self.filenames.get_filename_dictionary()["level_000_bin-filepath"]
            print self.source
            print self.destination
            self.move_data()

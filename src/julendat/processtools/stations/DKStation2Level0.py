"""Move downloaded D&K logger data to level 0 folder structure.
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
__version__ = "2010-08-07"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import os
import sys
import shutil
import Tkinter
from julendat.filetools.stations.dkstations.DKStationDataFile import \
    DKStationDataFile
from julendat.metadatatools.stations.StationDataFilePath import \
    StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.guitools.stations.GUIAutoPlotSelection import GUIAutoPlotSelection
from julendat.guitools.stations.GUIManualPlotSelection import \
    GUIManualPlotSelection


class DKStation2Level0:   
    """Instance for moving downloaded D&K logger data to level 0 folders.
    """

    def __init__(self, config_file, run_mode="auto-gui"):
        """Inits DKStation2Level0.
        The instance is initialized by reading a configuration file and the 
        initialization of the proprietary station data file instance.
        If the run mode is set to "auto-gui", this is followed by an automatic
        configuration of filenames and filepathes and the movement of the
        station data file to the processing path structure.  
        
        Args:
            config_file: Configuration file.
            run_mode: Running mode (auto-gui, manual)
        """
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.init_StationFile()
        if self.get_run_flag():
            self.auto_configure()
            self.run()
        else:
            print "Nothing to do..."
            print "...finished."        

    def set_run_mode(self, run_mode):
        """Sets run mode.
        
        Args:
            run_mode: Running mode (default: auto-gui)
        """
        self.run_mode = run_mode

    def get_run_mode(self):
        """Gets run mode.
        
        Returns:
            Running mode
        """
        return self.run_mode

    def configure(self, config_file):
        """Reads configuration settings and configure object.
    
        Args:
            config_file: Full path and name of the configuration file.
            
        """
        self.config_file = config_file
        config = ConfigParser.ConfigParser()
        config.read(self.config_file)
        self.initial_logger_filepath = config.get('logger', 'initial_logger_filepath')
        self.tl_data_path = config.get('repository', 'toplevel_repository_path')
        self.project_id = config.get('project', 'project_id')
        self.station_inventory = config.get('inventory', 'station_inventory')

    def init_StationFile(self):
        """Initializes D&K station data file.
        """
        try:
            self.binary_logger_file = DKStationDataFile(\
                                      filepath=self.initial_logger_filepath)

            ascii_file_exsists = False
            ascii_filepath = self.binary_logger_file.get_filepath()[:-3] + "asc"
            if os.path.isfile(ascii_filepath):
                ascii_file_exsists = True
            else:
                ascii_filepath = self.binary_logger_file.get_filepath()[:-3] + "ASC"
                if os.path.isfile(ascii_filepath):
                    ascii_file_exsists = True

            if ascii_file_exsists == True:
                self.ascii_logger_file = DKStationDataFile(\
                                         filepath=ascii_filepath)
                self.run_flag = self.ascii_logger_file.get_file_exists()
            else:
                self.run_flag = False

        except:
            self.run_flag = False
            self.ascii_logger_file = DKStationDataFile(\
                                         filepath=ascii_filepath)

    def get_run_flag(self):
        """Gets runtime flag information.
        
        Returns:
            Runtime flag.
        """
        return self.run_flag

    def auto_configure(self):
        """Set necessary attributes automatically.
        """
        self.inventory = StationInventory(filepath=self.station_inventory, \
                    serial_number=self.ascii_logger_file.get_serial_number())
        
        self.time_range = self.ascii_logger_file.get_time_range()
        if self.inventory.get_found_station_inventory():
            self.plot_id = self.inventory.get_plot_id()
            self.station_id = self.inventory.get_station_id()

    def run(self):
        """Executes class functions according to run_mode settings. 
        """
        if self.get_run_mode() == "manual":
            pass
        elif self.get_run_mode() == "auto-gui":
            self.auto_gui()

    def auto_gui(self):
        """Executes class functions in default auto-gui mode.
        """
        auto_plot_selection = self.inventory.get_found_station_inventory()
            
        if self.get_run_flag():
            if auto_plot_selection:
                gui = Tkinter.Tk()
                gui.title("Just to be sure...")
                gui.geometry('600x350+50+50')
                intro = "\n Please read very carefully. \n"
                question = "Are you standing on plot " + self.get_plot_id() + "?"
                outro = "\n Press only <Yes> if you are sure." + \
                        "\n If you press <No> you can specify the location manually.\n" 
                app = GUIAutoPlotSelection(gui, intro=intro, question=question, outro=outro)
                gui.mainloop()
                correct_plot_id = app.get_correct_plot_id()
                gui.destroy()        
            else:
                correct_plot_id = False
        
            if correct_plot_id != True:
                #plot_id_list = ["cof1", "cof2", "cof3", "cof4", "not sure"]
                plot_id_list = self.inventory.get_plot_id_list()
                gui = Tkinter.Tk()
                if auto_plot_selection:
                    gui.title("Just to be really sure...")
                    message="ARE YOU SURE?"
                else:
                    gui.title("Manual plot selection...")
                    message="The station/logger serial number has not been " +\
                            "found in the station inventory file. \n" + \
                            "Please select the plot from the list. \n" + \
                            "Please inform us that the station file is not " +\
                            "up to date."
                gui.geometry('600x350+50+50')
                app = GUIManualPlotSelection(gui, plot_id_list,message)
                gui.mainloop()
                gui.destroy()
                manual_plot_id = app.get_correct_plot_id()
        
                if self.inventory.get_found_station_inventory() == False:
                    if manual_plot_id == "not sure":
                        plot_id = "xx000000"
                    else:
                        plot_id = "xx" + manual_plot_id
                    self.station_id = "xxx"
                    postexflag = "not_in_inventory"
                elif manual_plot_id == "not sure":
                    plot_id = "xx000000"
                    postexflag = "autoplot_" + self.get_plot_id()
                elif self.inventory.get_found_station_inventory():
                    plot_id = "xx" + manual_plot_id
                    postexflag = "autoplot_" + self.get_plot_id()
            
                self.set_level0_filenames(project_id=self.project_id, \
                    plot_id=plot_id, postexflag=postexflag)
            
            else:
                self.set_level0_filenames(project_id=self.project_id)

            self.main()
        
    def move_data(self):
        """Moves files.
        """
        shutil.move(self.source, self.destination)

    def get_plot_id(self):
        """Gets coded plot id flag information.
        
        Returns:
            Runtime coded plot ID 
        """
        return self.plot_id
    
    def set_level0_filenames(self, project_id=None, \
                             plot_id=None, postexflag=None):
        """Sets level0 filenames and path information
        """
        if plot_id == None:
            plot_id = self.plot_id
        self.filenames = StationDataFilePath(\
                        toplevel_path=self.tl_data_path, \
                        project_id=project_id, \
                        plot_id=plot_id, \
                        station_id=self.station_id, \
                        start_datetime=self.ascii_logger_file.get_start_datetime(), \
                        end_datetime=self.ascii_logger_file.get_end_datetime(), \
                        time_step_delta = self.ascii_logger_file.get_time_step_delta(), \
                        aggregation_level="na", \
                        postexflag=postexflag)  
        
        #self.filenames.build_filename_dictionary()

    def main(self):
        """Maps logger files to level 0 filename and directory structure.
        """
        print self.filenames.get_filename_dictionary()["level_000_bin-filename"]
        print self.filenames.get_filename_dictionary()["level_000_bin-path"]
        print self.filenames.get_filename_dictionary()["level_000_bin-filepath"]
        print self.filenames.get_filename_dictionary()["level_000_ascii-filename"]
        print self.filenames.get_filename_dictionary()["level_000_ascii-path"]
        print self.filenames.get_filename_dictionary()["level_000_ascii-filepath"]

        # Check if path for level 0 files exists, otherwise create it        
        if not os.path.isdir(self.filenames.get_filename_dictionary()["level_000_bin-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()["level_000_bin-path"])
        if not os.path.isdir(self.filenames.get_filename_dictionary()["level_000_ascii-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()["level_000_ascii-path"])
        
        # Set full path and names of ASCII data files and move them
        self.source = self.ascii_logger_file.get_filepath()
        self.destination = self.filenames.get_filename_dictionary()["level_000_ascii-filepath"]
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

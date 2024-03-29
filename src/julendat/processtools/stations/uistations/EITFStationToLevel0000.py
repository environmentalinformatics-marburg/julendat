"""Query throughfall information and store data to level 0 folder structure.
Copyright (C) 2012 Thomas Nauss, Tim Appelhans

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Please send any comments, suggestions, criticism, or (for our sake) bug
reports to nausst@googlemail.com
"""

__author__ = "Thomas Nauss <nausst@googlemail.com>, Tim Appelhans"
__version__ = "2012-10-08"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import ConfigParser
import os
import re
import sys
import shutil
import Tkinter
import datetime
from julendat.processtools.TimeInterval import TimeInterval
from julendat.filetools.stations.dkstations.DKStationDataFile import \
    DKStationDataFile
from julendat.metadatatools.stations.StationDataFilePath import \
    StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.guitools.stations.GUITFPlotSelection import GUITFPlotSelection
from julendat.guitools.stations.GUIManualPlotSelection import \
    GUIManualPlotSelection
from julendat.guitools.stations.GUITFBucketData import \
    GUITFBucketData
from julendat.guitools.stations.GUIMiscBucketData import \
    GUIMiscBucketData
from julendat.guitools.stations.GUITFIsotopeData import \
    GUITFIsotopeData
from julendat.guitools.stations.GUIAutoPlotSelection import \
    GUIAutoPlotSelection
from julendat.guitools.stations.GUIDone import \
    GUIDone


class EITFStationToLevel0000:   
    """Instance for querying and storing throughfall data to level 0 folders.
    """

    def __init__(self, config_file, run_mode="auto-gui", dataset="noname.asc"):
        """Inits EIStationToLevel0000.
        The instance is initialized by reading a configuration file and the 
        initialization of the throughfall station setup data file instance.
        If the run mode is set to "auto-gui", this is followed by an automatic
        configuration of filenames and filepathes and the storage of the
        throughfall data file to the processing path structure.  
        
        Args:
            config_file: Configuration file.
            run_mode: Running mode (auto-gui, manual)
        """
        self.temp_isotope_bottle = 50
        self.final_isotope_bottle = 20
        self.dataset = dataset
        self.set_run_mode(run_mode)
        self.configure(config_file)
        #self.init_StationFile()
        self.run_flag = True
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
        #self.initial_logger_filepath = \
        #    config.get('repository', 'toplevel_processing_logger_path') + \
        #    config.get('logger', 'initial_logger_file')
        self.logger_time_zone = config.get('logger', 'logger_time_zone')
        self.tl_data_path = config.get('repository', 
                                       'toplevel_processing_plots_path')
        self.project_id = config.get('project', 'project_id')
        self.logger_time_zone = config.get('project', 'level_0005_timezone')
        self.station_inventory = config.get('inventory', 'station_inventory')

    def init_StationFile(self):
        """Initializes  station data file.
        """
        try:
            self.binary_logger_file = DKStationDataFile(\
                                      filepath=self.binary_logger_filepath)
            # Check if ascii station logger file exists.
            #ascii_filepath = self.binary_logger_file.get_filepath()[:-3] + "asc"
            if os.path.isfile(self.ascii_logger_filepath):
                ascii_file_exsists = True
            #else:
            #    ascii_filepath = self.binary_logger_file.get_filepath()[:-3] + \
            #        "ASC"
            #    if os.path.isfile(ascii_filepath):
            #        ascii_file_exsists = True
            #    else:
            #        ascii_file_exsists = False

            # Init ascii station logger file.
            if ascii_file_exsists == True:
                self.ascii_logger_file = DKStationDataFile(\
                                         filepath=self.ascii_logger_filepath)
                self.ascii_logger_file.set_time_range_ascii()
                
                self.run_flag = self.ascii_logger_file.get_file_exists()
            else:
                self.run_flag = False

        except Exception as inst:
            print "Error in init_StationFile."
            print "Some details:"
            print "Filename: " + self.ascii_logger_filepath
            print "Exception type: " , type(inst)
            print "Exception args: " , inst.args
            print "Exception content: " , inst        
            #TODO(tnauss): Handle exception more properly.
            self.run_flag = False

    def get_run_flag(self):
        """Gets runtime flag information.
        
        Returns:
            Runtime flag.
        """
        return self.run_flag

    def auto_configure(self):
        """Set necessary attributes automatically.
           Get list of all throughfall plots from inventory file.
        """
        self.inventory = StationInventory(filepath=self.station_inventory, \
            logger_start_time = datetime.datetime.now(), \
            logger_end_time = datetime.datetime.now(), \
            serial_number = "00000000006")

        self.tfsampling = True
        self.tfinventory_plotid = []
        self.tfinventory_color = []
        self.tfinventory_buckets = []
        self.tfinventory_isotope_buckets = []
        self.tfinventory_serial_number = []
        for entry in range(0,len(self.inventory.get_plot_tf_metadata_tupple())):
            if self.inventory.get_plot_tf_metadata_tupple()[entry][1] != "NaN":
                self.tfinventory_plotid.append(\
                        self.inventory.get_plot_tf_metadata_tupple()[entry][0])
                self.tfinventory_color.append(\
                        self.inventory.get_plot_tf_metadata_tupple()[entry][1])
                self.tfinventory_buckets.append(\
                        self.inventory.get_plot_tf_metadata_tupple()[entry][2])
                self.tfinventory_isotope_buckets.append(\
                        self.inventory.get_plot_tf_metadata_tupple()[entry][3])
                self.tfinventory_serial_number.append(\
                        self.inventory.get_plot_tf_metadata_tupple()[entry][4])

    def run(self):
        """Executes class functions according to run_mode settings. 
        """
        #self.tfplot_id = "flm"
        #self.tfplot_color = "Red"
        #self.report_tf_bucket_data_gui()
        #self.report_misc_bucket_data_gui()
        #self.isotope_tf_instructions_gui()
        #self.isotope_misc_instructions_gui()
        #sys.exit()
        if self.get_run_mode() == "manual":
            pass
        elif self.get_run_mode() == "auto-resort":
            self.resort_file()
        elif self.get_run_mode() == "auto-gui":
            self.select_tfplot_gui()
            if self.tfplot_id != False:
                self.confirm_tfplot_gui()
            else:
                os.sys.exit()
            if self.correct_plot_id == True:
                self.report_datetime_gui()
                if self.tfsampling:
                    self.report_tf_bucket_data_gui()
                self.report_misc_bucket_data_gui()
                if self.tfsampling:
                    self.calculate_isotope_mix()
                self.write_dataset()
                if self.tfsampling:
                    if self.prepare_tf_isotope_probe:
                        self.isotope_tf_instructions_gui()
                self.isotope_misc_instructions_gui()
                self.done_gui()
            else:
                self.run()

    def resort_file(self):
        """Resort already processed files according to filename or content.
        """
        self.filenames = StationDataFilePath(filepath = self.dataset, \
                                             toplevel_path = self.tl_data_path)
        if self.filenames.get_standard_name() == False:
            input = []
            input_file = open(self.dataset, "r")
            for line in input_file:
                input.append(line)
            input_file.close()
            plot_id = input[0][6:10]
            try: 
                date =  input[8][0:10]
                time =  input[8][12:20]
            except:
                date =  input[7][0:10]
                time =  input[7][12:20]
                
            start_datetime = datetime.datetime.strptime(\
                             date + " " + time,"%Y-%m-%d %H:%M:%S")
            time_step_delta = TimeInterval(start_datetime - \
                              datetime.timedelta(hours=1), \
                              start_datetime)
            self.filenames = StationDataFilePath(\
                             toplevel_path=self.tl_data_path, \
                             project_id=self.project_id, \
                             plot_id=plot_id, \
                             station_id="000tfi", \
                             start_datetime=start_datetime, \
                             end_datetime=start_datetime, \
                             time_step_delta = time_step_delta, \
                             logger_time_zone=self.logger_time_zone, \
                             aggregation_level="na", \
                             postexflag=None)

        self.filenames.build_filename_dictionary()
        print self.filenames.get_filename_dictionary()['level_0000_ascii-path']
        
        if not os.path.isdir(self.filenames.get_filename_dictionary()\
                             ['level_0000_ascii-path']):
            os.makedirs(self.filenames.get_filename_dictionary()\
                        ['level_0000_ascii-path'])
        cmd = "mv " + self.dataset + " " + \
              self.filenames.get_filename_dictionary()['level_0000_ascii-filepath']
        print cmd
        os.system(cmd)    
        

    def set_level0_filenames(self):
        """Sets level0 filenames and path information
        """
        end_datetime = datetime.datetime.now()
        time_step_delta = TimeInterval(end_datetime - \
                                       datetime.timedelta(hours=1), \
                                       end_datetime)
        
        
        self.filenames = StationDataFilePath(\
                        toplevel_path=self.tl_data_path, \
                        project_id=self.project_id, \
                        plot_id=self.tfplot_id, \
                        station_id="000tfi", \
                        start_datetime=self.start_datetime, \
                        end_datetime=end_datetime, \
                        time_step_delta = time_step_delta, \
                        logger_time_zone=self.logger_time_zone, \
                        aggregation_level="na", \
                        postexflag=None)

        self.filenames.build_filename_dictionary()

    
    def write_dataset(self):
        """Compute isotope mixture based on submitted data.
        
        Returns:
            tfplot_id: Plot id of throughfall plot
            tfplot_color: Color code of throughfall plot      
        """
        
        self.set_level0_filenames()

        if not os.path.isdir(self.filenames.get_filename_dictionary()\
                             ["level_0000_ascii-path"]):
            os.makedirs(self.filenames.get_filename_dictionary()\
                        ["level_0000_ascii-path"])
        output_file = open(self.filenames.get_filename_dictionary()\
                           ["level_0000_ascii-filepath"],"w")
        output_file.write("Plot: " + self.tfplot_id + "\n" + \
                          "Color: " + self.tfplot_color + "\n" + \
                          "Serial number: " + \
                          self.tfinventory_serial_number[self.tfinventory_plotid.index(self.tfplot_id)] + "\n" + \
                          "Logging Methode: Manual \n" + \
                          "Interval: sub-weekly to monthly \n" + \
                          "Isotope TF canisters: ")
        if self.tfsampling:
            for i in range(0, len(self.tfplot_isotope_buckets) - 1):
                output_file.write(\
                            str(self.tfplot_isotope_buckets[i]).zfill(2) + ", ")
            output_file.write(str(self.tfplot_isotope_buckets[-1]).zfill(2) + \
                              "\n" + \
                              "Isotope TF mixture: ")
            for i in range(0, len(self.isotope_share) - 1):
                output_file.write(str(self.isotope_share[i]).zfill(2) + ", ")
            output_file.write(str(self.isotope_share[-1]).zfill(2))
        output_file.write("\n" + "Date, Time")
        if self.tfsampling:
            for i in range(0, self.tfplot_buckets):
                output_file.write(", B_" + str(i+1).zfill(2))
        output_file.write(", Fog, Rainfall \n")
        output_file.write(self.start_datetime.strftime("%Y-%m-%d") + ", " + \
                          self.start_datetime.strftime("%H:%M:%S"))
        if self.tfsampling:
            for i in self.bucket_values:
                output_file.write(", " + str(i))
        for i in self.misc_bucket_values:
            output_file.write(", " + str(i))
        output_file.close()

        
    def calculate_isotope_mix(self):
        """Compute isotope mixture based on submitted data.
        
        Returns:
            tfplot_id: Plot id of throughfall plot
            tfplot_color: Color code of throughfall plot      
        """
        self.prepare_tf_isotope_probe = True
        self.isotope_values = []
        
        for i in self.tfplot_isotope_buckets:
            self.isotope_values.append(float(self.bucket_values[int(i)-1]))
        self.isotope_sum = sum(self.isotope_values)

        self.isotope_share = []
        if self.isotope_sum <= 0.01:
            self.prepare_tf_isotope_probe = False
            self.isotope_sum = 1.0
            for i in range(0, len(self.tfplot_isotope_buckets)):
                self.isotope_share.append(-2.0)
        else:        
            for i in range(0, len(self.tfplot_isotope_buckets)):
                self.isotope_share.append(round(\
                    self.isotope_values[i]/self.isotope_sum * \
                    self.temp_isotope_bottle, 0))
            self.isotope_share[-1] = self.temp_isotope_bottle - \
                                     sum(self.isotope_share) + \
                                     self.isotope_share[-1]
            check = [x for x in self.isotope_share if x < 0.0]
            if check:
                check = False
            else: 
                check = True  
            if check == False:
                for i in range(0, len(self.tfplot_isotope_buckets)):
                    self.isotope_share.append(
                        self.isotope_values[i]//self.isotope_sum * \
                        self.temp_isotope_bottle)
                self.isotope_share[-1] = self.temp_isotope_bottle - \
                sum(self.isotope_share) + \
                                         self.isotope_share[-1]
        

    def select_tfplot_gui(self):
        """GUI for the selection of the throughfall plot.
        The selection is based on plot id and color.
        
        Returns:
            tfplot_id: Plot id of throughfall plot
            tfplot_color: Color code of throughfall plot      
        """
        gui = Tkinter.Tk()
        gui.title("Throughfall plot data report...")
        gui.geometry('600x350+50+50')
        intro = "\n Everybody be cool. You, be cool. \n"
        question = "Which plot would you like to report?"
        outro = "Select the color and plot id." + \
                "\n If you want to stop  the program, press <Cancel>." 
        app = GUITFPlotSelection(master = gui, \
                                intro=intro, question=question, outro=outro,
                                plot_id_list = self.tfinventory_plotid,
                                plot_color_list = self.tfinventory_color)
        gui.mainloop()
        self.tfplot_id = app.get_plot_id()
        self.tfplot_color = app.get_plot_color()
        self.tfplot_buckets = int(\
         self.tfinventory_buckets[self.tfinventory_plotid.index(self.tfplot_id)])
        self.tfplot_isotope_buckets = \
         self.tfinventory_isotope_buckets[self.tfinventory_plotid.index(self.tfplot_id)]
        gui.destroy()        
        if self.tfplot_isotope_buckets[0] == '0':
            self.tfsampling = False

        
    def confirm_tfplot_gui(self):
        """GUI for the confirmation of the throughfall plot.
        The user must confirm his initial selection (select_tfplot_gui).
        If he does not confirm it, he has the opportunity to start over again.
        
        Returns:
            correct_plot_id: Flag if plot selection is correct.
        """
        gui = Tkinter.Tk()
        gui.title("Just to be sure...")
        gui.geometry('600x350+50+50')
        intro = "\n Please read very carefully. \n"
        question = "Are you sure you want to process \n" \
                   "plot " + self.tfplot_id + " (" + \
                   self.tfplot_color + ")?"
        outro = "\n Press only <Yes> if you are sure." + \
                "\n If you press <No> you can select the plot again.\n" 
        app = GUIAutoPlotSelection(master = gui, \
                                intro=intro, question=question, outro=outro)
        gui.mainloop()
        self.correct_plot_id = app.get_correct_plot_id()
        gui.destroy()        


    def report_datetime_gui(self):
        """GUI to commit the manually measured data values.
        
        Returns:
            tfplot_id: Plot id of throughfall plot
            tfplot_color: Color code of throughfall plot      
        """
        gui = Tkinter.Tk()
        gui.title("Report data")
        gui.geometry('600x350+50+50')
        intro = "\n Enter the date and time you visited the plot \n"
        question = None
        outro = None 
        entry_label = ["Year", "Month", "Day", "Hour", "Minute"]
        app = GUIMiscBucketData(master = gui,
                              intro=intro, question=question, outro=outro,
                              entry_label = entry_label,
                              plot_id = self.tfplot_id, 
                              plot_color = self.tfplot_color)
        gui.mainloop()
        self.start_datetime = datetime.datetime.strptime(\
                                '-'.join(app.get_values()),"%Y-%m-%d-%H-%M")
        gui.destroy()  


    def report_tf_bucket_data_gui(self):
        """GUI to commit the manually measured data values.
        
        Returns:
            tfplot_id: Plot id of throughfall plot
            tfplot_color: Color code of throughfall plot      
        """
        gui = Tkinter.Tk()
        gui.title("Report data")
        gui.geometry('600x350+50+50')
        intro = "\n Enter canister volumes (and: you, be cool)! \n"
        question = None
        outro = "Canisters marked with * are used for isotope analysis." 
        app = GUITFBucketData(master = gui, \
                              intro=intro, question=question, outro=outro, \
                              plot_id = self.tfplot_id, \
                              plot_color = self.tfplot_color, \
                              buckets_number =  self.tfplot_buckets, \
                              marked_buckets =  self.tfplot_isotope_buckets)
        gui.mainloop()
        self.bucket_values = app.get_values()
        gui.destroy()  
        
    def report_misc_bucket_data_gui(self):
        """GUI to commit the manually measured data values.
        
        Returns:
            tfplot_id: Plot id of throughfall plot
            tfplot_color: Color code of throughfall plot      
        """
        gui = Tkinter.Tk()
        gui.title("Report data")
        gui.geometry('600x350+50+50')
        intro = "\n Enter canister volumes (and: you, be cool)! \n"
        question = None
        outro = None 
        entry_label = ["Canister Fog", "Canister Rainfall"]
        app = GUIMiscBucketData(master = gui,
                              intro=intro, question=question, outro=outro,
                              entry_label = entry_label,
                              plot_id = self.tfplot_id, 
                              plot_color = self.tfplot_color)
        gui.mainloop()
        self.misc_bucket_values = app.get_values()
        gui.destroy()  


    def isotope_tf_instructions_gui(self):
        """GUI to commit the manually measured data values used for isotope 
        analysis.
        
        Returns:
            tfplot_id: Plot id of throughfall plot
            tfplot_color: Color code of throughfall plot      
        """
        gui = Tkinter.Tk()
        gui.title("Isotope analysis")
        gui.geometry('600x350+50+50')
        header = "YOU, BE COOL!"
        intro = "\n Please prepare the " + str(self.temp_isotope_bottle) + \
                 "ml probe for throughfall analysis."+ \
                "\n Extract given ml and pour them TOGETHER in " + \
                str(self.temp_isotope_bottle) + " ml bottle. \n" 
        outro = None 
        app = GUITFIsotopeData(master = gui, \
                              header=header, intro=intro, \
                              bucket_id=self.tfplot_isotope_buckets, \
                              bucket_amount = self.isotope_share,\
                              outro=outro,
                              plot_id = self.tfplot_id, 
                              plot_color = self.tfplot_color)
        gui.mainloop()
        gui.destroy()  


    def isotope_misc_instructions_gui(self):
        """GUI to commit the manually measured data values used for isotope 
        analysis.
        
        Returns:
            tfplot_id: Plot id of throughfall plot
            tfplot_color: Color code of throughfall plot      
        """
        header = "YOU, BE COOL!"
        if self.tfsampling:
            if self.prepare_tf_isotope_probe:
                gui = Tkinter.Tk()
                gui.title("Isotope analysis")
                gui.geometry('600x350+50+50')
                intro = "\n Please fill " + str(self.final_isotope_bottle) + " ml" + \
                        "\n of the just prepared " + str(self.temp_isotope_bottle) + \
                        " ml mixing bottle" + \
                        "\n into the final isotope glass bottle. \n"
                bucket_id = ["Througfall"]
                bucket_amount = [self.final_isotope_bottle]
                outro = None 
                app = GUITFIsotopeData(master = gui, \
                                      header = header, intro=intro, \
                                      bucket_id=bucket_id, \
                                      bucket_amount = bucket_amount,\
                                      outro=outro,
                                      plot_id = self.tfplot_id, 
                                      plot_color = self.tfplot_color)
                gui.mainloop()
                gui.destroy()  

        if int(self.misc_bucket_values[0]) > 0:
            gui = Tkinter.Tk()
            gui.title("Isotope analysis")
            gui.geometry('600x350+50+50')
            header = "YOU, BE COOL!"
            intro = "\n Please prepare the " + str(self.final_isotope_bottle) + \
                    " ml probes for fog analysis."+ \
                    "\n Extract given ml and pour them in a " + \
                    str(self.final_isotope_bottle) + " ml glass bottle. \n" 
            bucket_id = ["Fog"]
            bucket_amount = [self.final_isotope_bottle]
            outro = "If you have less than 20 ml, just pour in everyhting. \n " 
            app = GUITFIsotopeData(master = gui, \
                                  header = header, intro=intro, \
                                  bucket_id=bucket_id, \
                                  bucket_amount = bucket_amount,\
                                  outro=outro,
                                  plot_id = self.tfplot_id, 
                                  plot_color = self.tfplot_color)
            gui.mainloop()
            gui.destroy()  

        if int(self.misc_bucket_values[1]) > 0:
            gui = Tkinter.Tk()
            gui.title("Isotope analysis")
            gui.geometry('600x350+50+50')
            intro = "\n Please prepare the " + str(self.final_isotope_bottle) + \
                    " ml probes for rainfall analysis."+ \
                    "\n Extract given ml and pour them in a " + \
                    str(self.final_isotope_bottle) + " ml glass bottle. \n" 
            bucket_id = ["Rainfall"]
            bucket_amount = [self.final_isotope_bottle]
            outro = "If you have less than 20 ml, just pour in everyhting. \n " 
            app = GUITFIsotopeData(master = gui, \
                                  header = header, intro=intro, \
                                  bucket_id=bucket_id, \
                                  bucket_amount = bucket_amount,\
                                  outro=outro,
                                  plot_id = self.tfplot_id, 
                                  plot_color = self.tfplot_color)
            gui.mainloop()
            gui.destroy()
            

    def done_gui(self):
        """GUI for the confirmation that everything has been done.
        
        """
        gui = Tkinter.Tk()
        gui.title("Just to be sure...")
        gui.geometry('600x350+50+50')
        header = "YOU HAVE BEEN COOL!"
        intro = "\n All right! \n"
        comment = "You've done a great job!"
        outro = "\n Press <Done> to exit the program."
        app = GUIDone(master=gui, header = header, intro=intro, \
                      comment=comment, outro=outro)
        gui.mainloop()
        self.correct_plot_id = app.get_correct_plot_id()
        gui.destroy()        
  

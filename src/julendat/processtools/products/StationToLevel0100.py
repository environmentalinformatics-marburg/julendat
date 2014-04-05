"""Process level 0050 station data to quality controlled level 0100.
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
__version__ = "2012-01-18"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import sys
import csv
import os
import string
import ConfigParser
from julendat.processtools import time_utilities
from julendat.filetools.stations.dkstations.DKStationDataFile import DKStationDataFile
import shutil
import time
import datetime
from julendat.metadatatools.stations.StationDataFilePath import StationDataFilePath
from julendat.metadatatools.stations.StationInventory import StationInventory
from julendat.metadatatools.stations.Level01Standards import Level01Standards


class StationToLevel0100:   
    """Instance for processing station level 0050 to level 0100 data.
    """

    def __init__(self, filepath, config_file,run_mode="auto"):
        """Inits StationToLevel0100. 
        
        Args:
            filepath: Full path and name of the level 0050 file
            config_file: Configuration file.
            run_mode: Running mode (auto, manual)
        """
        self.set_run_mode(run_mode)
        self.configure(config_file)
        self.init_filenames(filepath)
        if self.get_run_flag():
            self.run()
        else:
            raise Exception, "Run flag is false."

    def set_run_mode(self,run_mode):
        """Sets run mode.
        
        Args:
            run_mode: Running mode (default: auto)
        """
        self.run_mode = run_mode

    def get_run_mode(self):
        """Gets run mode.
        
        Returns:
            Running mode
        """
        return self.run_mode

    def configure(self,config_file):
        """Reads configuration settings and configure object.
    
        Args:
            config_file: Full path and name of the configuration file.
        """
        self.config_file = config_file
        config = ConfigParser.ConfigParser()
        config.read(self.config_file)
        self.tl_data_path = config.get('repository', 'toplevel_processing_plots_path')
        self.station_inventory = config.get('inventory','station_inventory')
        self.project_id = config.get('project','project_id')
        self.level0050_standards = config.get('general','level0050_standards')
        self.r_filepath = config.get('general','r_filepath')

    def init_filenames(self, filepath):
        """Initializes D&K station data file.
        
        Args:
            filepath: Full path and name of the level 0 file
        """
        try:
            self.filenames = StationDataFilePath(filepath=filepath, \
                toplevel_path=self.tl_data_path)
            self.filenames.build_filename_dictionary()
            self.run_flag = True
        except:
            raise Exception, "Can not compute station data filepath"
            self.run_flag = False

    def get_run_flag(self):
        """Gets runtime flag information.
        
        Returns:
            Runtime flag.
        """
        return self.run_flag

    def run(self):
        """Executes class functions according to run_mode settings. 
        """
        if self.get_run_mode() == "0100":
            self.ascii_path = self.filenames.get_filename_dictionary()\
                                  ["level_0100_ascii-path"]
            self.ascii_filepath = self.filenames.get_filename_dictionary()\
                                      ["level_0100_ascii-filepath"]
            self.target_level = "0100"
        elif self.get_run_mode() == "0250":
            self.ascii_path = self.filenames.get_filename_dictionary()\
                                  ["level_0250_ascii-path"]
            self.ascii_filepath = self.filenames.get_filename_dictionary()\
                                      ["level_0250_ascii-filepath"]
            self.target_level = "0250"
        self.auto()

    def auto(self):
        """Executes class functions in default auto mode.
        """
        # BUG - write 100 250 SF 20140320
        #if not os.path.isfile(self.ascii_filepath):
        self.main()
        #else:
            #pass

    def main(self):
        """Processes level 0050 station files to level 0100.
        """
        self.get_level0100_quality_settings()
        self.process_range_test()
        self.process_step_test()


    def get_level0100_quality_settings(self):
        """Sets quality settings for level 0100 station data files
        """
        level0100_standard = Level01Standards(\
            filepath=self.level0050_standards, \
            station_id=self.filenames.get_station_id())
        self.level0100_quality_settings = \
            level0100_standard.get_level0100_quality_settings()

    def process_range_test(self):
        """Process range test on level 0050 file.
        
        """
        if not os.path.isdir(self.ascii_path):
            os.makedirs(self.ascii_path)
        
        rthv_max = self.level0100_quality_settings['rthv_max']
        rthv_max = [x.split(",") for x in rthv_max]
        rthv_max = [item for sublist in rthv_max for item in sublist]
        if self.get_run_mode() == "0250":
            try:
                p_index = list(self.level0100_quality_settings['quality_parameter']).index("P_RT_NRT")
                rthv_max[p_index] = str(float(rthv_max[p_index]) * 60.0)
            except:
                None
        rthv_max = [float(x) for x in rthv_max]
        rthv_max =   ', '.join(map(str,rthv_max))
        
        output_filepath = self.ascii_filepath
        
        r_source = 'source("' + self.r_filepath + os.sep + \
                'run_QCRange.R")'
        r_keyword = "run_QCRange"
        r_ifp = 'input_filepath="' + self.filenames.get_filepath() + '"'
        r_ofp = 'output_filepath="' + output_filepath + '"'
        r_prm = 'parameter=c("' + \
            '", "'.join(self.level0100_quality_settings['quality_parameter']) \
             + '")'
        r_thvi = 'thv_min=c(' + \
            ', '.join(self.level0100_quality_settings['rthv_min']) + ')'
        r_thva = 'thv_max=c(' + rthv_max + ')'
        r_qfpos = 'qfpos=c(' + \
            ', '.join(self.level0100_quality_settings['qfpos']) + ')'
        r_qvalues = 'qfvalues=c(' + \
            ', '.join(self.level0100_quality_settings['rqfvalues']) + ')'
        r_flag_col = 'flag_col="Qualityflag"'
        r_plevel = 'plevel = ' + self.target_level

        print r_thva
        
        act_wd = os.getcwd()
        os.chdir(self.r_filepath)
        r_cmd = r_source + '\n' + \
                r_keyword + '(\n' + \
                r_ifp + ',\n' + \
                r_ofp + ',\n' + \
                r_prm + ',\n' + \
                r_thvi + ',\n' + \
                r_thva + ',\n' + \
                r_qfpos + ',\n' + \
                r_qvalues + ',\n' + \
                r_flag_col + ',\n' + \
                r_plevel + ')\n'
        
        r_script = "qcrange.rscript" 
        f = open(r_script,"w")
        f.write(r_cmd)
        f.close()
        r_cmd = 'R CMD BATCH ' + r_script  + ' ' + r_script + '.log'
        os.system(r_cmd)
        os.chdir(act_wd)

    def process_step_test(self):
        """Process step test on level 0050 file.
        
        """
        if not os.path.isdir(self.ascii_path):
            os.makedirs(self.ascii_path)
        
        slmts_max = self.level0100_quality_settings['slmts_max']
        slmts_max = [x.split(",") for x in slmts_max]
        slmts_max = [item for sublist in slmts_max for item in sublist]
        if self.get_run_mode() == "0250":
            try:
                p_index = list(self.level0100_quality_settings['quality_parameter']).index("P_RT_NRT")
                slmts_max[p_index] = str(float(slmts_max[p_index]) * 60.0)
            except:
                None
        slmts_max = [float(x) for x in slmts_max]
        slmts_max =   ', '.join(map(str,slmts_max))

        output_filepath = self.ascii_filepath
        
        r_source = 'source("' + self.r_filepath + os.sep + \
                'run_QCSteps.R")'
        r_keyword = "run_QCSteps"
        r_ifp = 'input_filepath="' + output_filepath + '"'
        r_ofp = 'output_filepath="' + output_filepath + '"'
        r_prm = 'parameter=c("' + \
            '", "'.join(self.level0100_quality_settings['quality_parameter']) \
             + '")'
        r_perc = 'percentil=c(' + \
            ', '.join(self.level0100_quality_settings['spercentil']) + ')'
        r_qfpos = 'qfpos=c(' + \
            ', '.join(self.level0100_quality_settings['qfpos']) + ')'
        r_qvalues = 'qfvalues=c(' + \
            ', '.join(self.level0100_quality_settings['sqfvalues']) + ')'
        r_limit_output = 'limit_output = NULL'
        r_pos_date = 'pos_date = 1'
        r_flag_col = 'flag_col="Qualityflag"'
        r_lmts = 'lmts=data.frame(min=c(' + \
            ', '.join(self.level0100_quality_settings['slmts_min']) + \
            '), max=c(' + slmts_max + '))'
        r_plevel = 'plevel = ' + self.target_level
        
        print r_lmts
        
        act_wd = os.getcwd()
        os.chdir(self.r_filepath)
        r_cmd = r_source + '\n' + \
                r_keyword + '(\n' + \
                r_ifp + ',\n' + \
                r_ofp + ',\n' + \
                r_prm + ',\n' + \
                r_perc + ',\n' + \
                r_qfpos + ',\n' + \
                r_qvalues + ',\n' + \
                r_limit_output + ',\n' + \
                r_pos_date + ',\n' + \
                r_flag_col + ',\n' + \
                r_lmts + ',\n' + \
                r_plevel + ')\n'
        r_script = "qcstep.rscript" 
        f = open(r_script,"w")
        f.write(r_cmd)
        f.close()
        r_cmd = 'R CMD BATCH ' + r_script  + ' ' + r_script + '.log'
        os.system(r_cmd)
        os.chdir(act_wd)

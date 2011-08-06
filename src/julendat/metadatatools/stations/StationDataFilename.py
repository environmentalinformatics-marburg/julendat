'''
Class for station data file names.
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

class StationDataFilename:   
    """Class for station data file names.
    
    Constructor:
    DataFile(filepath="None", filetype="None", io_access="r")
    
    For Keyword arguments see __init__().
    
    """

    def __init__(self, filename=None,toplevel_path=None,projectID=None,plotID=None, \
                 stationType=None,startTime=None,endTime=None, \
                 calibrationLevel=None,aggregation=None, \
                 quality=None,extension=None,postexflag=None):
        '''Constructor of the class.         

        __init__(self, file, filetype,io_access="r")
        
        @param file: Full path and name of the data file.
        @param filetype: Type of the data file.
        @param io_access: Read/write access to data file ('r' or 'w').

        '''

        self.set_toplevel_path(toplevel_path)
            
        if filename == None:
            self.set_projectID(projectID)
            self.set_plotID(plotID)
            self.set_stationType(stationType)
            self.set_startTime(startTime)
            self.set_endTime(endTime)
            self.set_calibrationLevel(calibrationLevel)
            self.set_aggregation(aggregation)
            self.set_quality(quality)
            self.set_extension(extension)
            self.set_postexflag(postexflag)
        
        self.set_filename(filename)
        
        self.checkStandard()
        if self.standardName:
            self.set_filenameDictionary()

    def set_filenameDictionary(self):
        '''Set dictionary for data filenames of different levels.
        
        '''
               
        self.filenameDictionary = {}

        calibration_level="rb01"
        quality = "0000"
        extension="bin"
        self.filenameDictionary['level_000_bin-filename'] = \
            self.construct_filename(\
                calibrationLevel=calibration_level, \
                quality=quality, \
                extension=extension)
        self.filenameDictionary['level_000_bin-path'] = \
            self.construct_filepath(\
                calibrationLevel=calibration_level, \
                quality=quality)
        self.filenameDictionary['level_000_bin-file'] = \
            self.filenameDictionary['level_000_bin-path'] + \
            self.filenameDictionary['level_000_bin-filename']

        calibration_level="ra01"
        quality = "0000"
        extension="asc"
        self.filenameDictionary['level_001_ascii-filename'] = \
            self.construct_filename(\
                calibrationLevel=calibration_level, \
                quality=quality, \
                extension=extension)
        self.filenameDictionary['level_001_ascii-path'] = \
            self.construct_filepath(\
                calibrationLevel=calibration_level, \
                quality=quality)
        self.filenameDictionary['level_001_ascii-file'] = \
            self.filenameDictionary['level_001_ascii-path'] + \
            self.filenameDictionary['level_001_ascii-filename']


    def get_filenameDictionary(self):
        '''Get dictionary for data filenames of different levels.
        
        '''
        return self.filenameDictionary


    def construct_filename(self,projectID=None,plotID=None, \
                 stationType=None,startTime=None,endTime=None, \
                 calibrationLevel=None,aggregation=None, \
                 quality=None,extension=None,postexflag=None):
        '''Construct filename.
        
        '''
        if projectID == None:
            projectID = self.get_projectID()
        if plotID == None:
            plotID = self.get_plotID()
        if stationType == None:
            stationType = self.get_stationType()
        if startTime == None:
            startTime = self.get_startTime()
        if endTime == None:
            endTime = self.get_endTime()
        if calibrationLevel == None:
            calibrationLevel = self.get_calibrationLevel()
        if aggregation == None:
            aggregation = self.get_aggregation()
        if quality == None:
            quality = self.get_quality()
        if extension == None:
            extension = self.get_extension()
        if postexflag == None:
            postexflag = self.get_postexflag()
        
        filename = projectID + "_" + \
                   plotID + "_" + \
                   stationType + "_" + \
                   startTime + "_" + \
                   endTime + "_" + \
                   calibrationLevel + "_" + \
                   aggregation + "_" + \
                   quality + "." + \
                   extension
        if postexflag != None:
            filename = filename + "." + postexflag 
        
        return filename


    def construct_filepath(self,projectID=None,plotID=None, \
                            calibrationLevel=None,aggregation=None, \
                            quality=None):
        '''Construct filename.
        
        '''
        if projectID == None:
            projectID = self.get_projectID()
        if plotID == None:
            plotID = self.get_plotID()
        if plotID[0:2] == "xx":
            plotID = "conflict" + os.sep + plotID
        if calibrationLevel == None:
            calibrationLevel = self.get_calibrationLevel()
        if aggregation == None:
            aggregation = self.get_aggregation()
        if quality == None:
            quality = self.get_quality()
        
        filepath = self.get_toplevel_path() + os.sep + \
                   projectID  + os.sep + \
                   plotID  + os.sep + \
                   calibrationLevel + "_" + aggregation + "_" + quality + os.sep
        
        return filepath


    def checkStandard(self):
        '''Check if file is named according to the naming convention.
        
        '''
        filename = self.get_filename()
        if filename[2] == "_" and filename[11] == "_" \
            and filename[15] == "_" and filename[28]  == "_" \
            and filename[41] == "_" and filename[46] == "_" \
            and filename[52] == "_":
            self.standardName  = True
            
        else:
            self.standardName = False
            
        
    
    def set_filename(self,filename):
        '''Set filename of the data file.
        
        '''
        if filename != None:
            self.filename = filename
            self.set_extension()
        else:
            self.filename = self.get_projectID() + "_" + \
                            self.get_plotID() + "_" + \
                            self.get_stationType() + "_" + \
                            self.get_startTime() + "_" + \
                            self.get_endTime() + "_" + \
                            self.get_calibrationLevel() + "_" + \
                            self.get_aggregation() + "_" + \
                            self.get_quality() + "." + \
                            self.get_extension()
    

    def get_filename(self):
        '''Get filename provided during object initialization.
        '''
        return self.filename


    def set_projectID(self, projectID):
        '''Set project ID of the data file.
        
        @param projectID: Project ID
        
        '''
        if projectID == None:
            projectID = "00"
        self.projectID = projectID


    def get_projectID(self):
        '''Get project ID of the data file.
        
        '''
        return self.projectID


    def set_plotID(self, plotID):
        '''Set plot ID of the data file.
        
        @param plotID: plot ID of the data file
        
        '''
        if plotID == None:
            plotID = "00000000"
        elif plotID[0:2] == "xx":
            plotID = "xx" + plotID[2:].zfill(6)  
        else:
            plotID = plotID.zfill(8)
        
        self.plotID = plotID


    def get_plotID(self):
        '''Get plot ID of the data file.
        
        '''
        return self.plotID

         
    def set_stationType(self, stationType):
        '''Set station type of the data file.
        
        @param stationType: Station type of the data file
        
        '''
        if stationType == None:
            stationType = "000"
        self.stationType = stationType


    def get_stationType(self):
        '''Get station type of the data file.
        
        '''
        return self.stationType

         
    def set_startTime(self, startTime):
        '''Set start time of the data file.
        
        @param startTime: Start time of the data file
        
        '''
        if startTime == None:
            startTime = "000000000000"
        self.startTime = startTime


    def get_startTime(self):
        '''Get start time of the data file.
        
        '''
        return self.startTime

         
    def set_endTime(self, endTime):
        '''Set end time of the data file.
        
        @param endTime: End time of the data file
        
        '''
        if endTime == None:
            endTime = "000000000000"
        self.endTime = endTime


    def get_endTime(self):
        '''Get end time of the data file.
        
        '''
        return self.endTime

         
    def set_calibrationLevel(self, calibrationLevel):
        '''Set calibration level of the data file.
        
        @param calibrationLevel: calibration level of the data file
        
        '''
        if calibrationLevel == None:
            calibrationLevel = "0000"
        self.calibrationLevel = calibrationLevel


    def get_calibrationLevel(self):
        '''Get calibration level of the data file.
        
        '''
        return self.calibrationLevel

         
    def set_aggregation(self, aggregation):
        '''Set aggregation of the data file.
        
        @param aggregation: Time aggregation
        
        '''
        if aggregation == None:
            aggregation = "00000"
        self.aggregation = aggregation


    def get_aggregation(self):
        '''Get time aggregation of the data file.
        
        '''
        return self.aggregation

         
    def set_quality(self, quality):
        '''Set quality flag of the data file.
        
        @param quality: Qualilty flag
        
        '''
        if quality == None:
            quality = "00000"
        self.quality = quality


    def get_quality(self):
        '''Get quality flag of the data file.
        
        '''
        return self.quality

         
    def set_extension(self, extension=None):
        '''Set extension of the data file.
        
        @param extension: File name extension
        
        '''
        if extension == None:
            try:
                extension = self.get_filename()[-3:]
            except:
                extension = "dat"
        self.extension = extension


    def get_extension(self):
        '''Get extension of the data file.
        
        '''
        return self.extension


    def set_postexflag(self, postexflag):
        '''Set post extension of the data file.
        
        @param extension: File name extension
        
        '''
        self.postexflag = postexflag


    def get_postexflag(self):
        '''Get post extension of the data file.
        
        '''
        return self.postexflag

    
    def set_toplevel_path(self, toplevel_path):
        '''Set toplevel path of the data file neseccary for dictionary.
        
        @param toplevel_path: Toplevel path
        
        '''
        if toplevel_path == None:
            toplevel_path = os.getcwd()
        self.toplevel_path = toplevel_path


    def get_toplevel_path(self):
        '''Get toplevel path of the data file neseccary for dictionary.
        
        '''
        return self.toplevel_path

         

'''
Created on Aug 13, 2011

@author: tnauss
'''


from julendat.processtools.TimePoint import TimePoint
import time
import datetime
import sys

class TimeInterval(TimePoint):



    def __init__(self,time_value_01=None, time_value_02=None):
        if isinstance(time_value_01, str):
            self.set_time_step_delta_from_str(time_value_01)
        else:
            if isinstance(time_value_01, datetime.timedelta):
                self.set_time_step(time_step_delta=time_value_01)    
            else:
                self.time_value_01 = TimePoint(time_value_01)
                self.time_value_02 = TimePoint(time_value_02)
                self.set_time_step()   

            self.set_time_step_delta_str()
            self.set_time_step_level_str()
        self.set_data_file_time_value()
        self.set_data_file_time_value_eifc()

    def set_time_step_delta_from_str(self, time_step_delta_str):
        time_step_delta_str = time_step_delta_str
        if len(time_step_delta_str) > 2:
            time_step_delta_str = time_step_delta_str[2:] 
        
        self.time_step_delta_str = time_step_delta_str[1:]
        self.time_step_level_str = time_step_delta_str[0]
        
        if self.time_step_level_str == "s":
            self.time_step_delta = int(self.time_step_delta_str) 
        elif self.time_step_level_str == "i":
            self.time_step_delta = int(self.time_step_delta_str) * 60 
        elif self.time_step_level_str == "h":
            self.time_step_delta = int(self.time_step_delta_str) * 3600 
        elif self.time_step_level_str == "d":
            self.time_step_delta = int(self.time_step_delta_str) * 24 * 3600 
        elif self.time_step_level_str == "m":
            self.time_step_delta = int(self.time_step_delta_str) * 24 * 30 * 3600 
        self.set_time_step_level()
        
    def set_time_step(self, time_step_delta=None):
        if time_step_delta != None:
            time_step_delta = time_step_delta
        else:
            time_step_delta = self.time_value_02.get_dto() - \
                              self.time_value_01.get_dto()
        self.time_step_delta = time_step_delta

    def get_time_step(self):
        return self.time_step_delta


    def set_time_step_delta_str(self, time_step_delta=None):
        """Sets time step of the data file as string.

        Args:
            time step of the data file as datetime.timedelta object.
        """
        y = "0000"
        m = "00"
        d = "00"
        h = "00"
        i = "00"
        s = "00"

        if time_step_delta == None:
            time_step_delta = self.time_step_delta
        seconds = time_step_delta.total_seconds()
        if seconds < 60.0:
            s = time.strftime("%S",time.strptime(str(int(seconds)),"%S"))
            time_step_delta_str = s.zfill(2)
            time_step_level = "seconds"
        elif seconds >= 60.0:
            i = seconds // 60.0
            remainder = seconds - (i*60.0)
            s = time.strftime("%S",time.strptime(str(int(remainder)),"%S"))
            if i < 60.0:
                i = time.strftime("%M",time.strptime(str(int(i)),"%M"))
                time_step_delta_str = i.zfill(2)
                time_step_level = "minutes"
            elif i >= 60.0:
                h = i // 60.0
                remainder = i - (h*60)
                i = time.strftime("%M",time.strptime(str(int(remainder)),"%M"))
                if h < 24.0:
                    h = time.strftime("%H",time.strptime(str(int(h)),"%H"))
                    time_step_delta_str = h.zfill(2)
                    time_step_level = "hours"
                elif h >= 24.0:
                    d = h // 24.0
                    remainder = h - (d*24)
                    h = time.strftime("%H",time.strptime(str(int(remainder)),"%H"))
                    if d <= 100:
                        d = time.strftime("%d",time.strptime(str(int(d)),"%d"))
                        time_step_delta_str = d.zfill(2)
                        time_step_level = "days"
                    else:
                        m = d // 30
                        m = time.strftime("%m",time.strptime(str(int(m)),"%m"))
                        time_step_delta_str = m.zfill(2)
                        time_step_level = "months"
                        
        self.time_step_delta_str = time_step_delta_str
        self.time_step_level = time_step_level

    def get_time_step_delta_str(self):
        return self.time_step_delta_str
    
    def set_time_step_level(self):
        """Gets coded time step level of the data file.

        Returns:
            Coded time step level of the data file
        """
        if self.time_step_level_str == "s":
            self.time_step_level = "seconds"
        elif self.time_step_level_str == "i":
            self.time_step_level = "minutes"
        elif self.time_step_level_str == "h":
            self.time_step_level = "hours"
        elif self.time_step_level_str == "d":
            self.time_step_level = "days"
        elif self.time_step_level_str == "m":
            self.time_step_level = "months"

    def set_time_step_level_str(self):
        """Gets coded time step level of the data file.

        Returns:
            Coded time step level of the data file
        """
        if self.time_step_level == "seconds":
            self.time_step_level_str = "s"
        elif self.time_step_level == "minutes":
            self.time_step_level_str = "i"
        elif self.time_step_level == "hours":
            self.time_step_level_str = "h"
        elif self.time_step_level == "days":
            self.time_step_level_str = "d"
        elif self.time_step_level == "months":
            self.time_step_level_str = "m"

    def get_time_step_level_str(self):
        return self.time_step_level_str
    
    def set_data_file_time_value(self):
        self.data_file_time_value = self.get_time_step()
    
    def set_data_file_time_value_eifc(self):
        #TODO: tnauss: Change entire routine
        if self.time_step_level == "seconds":
            self.data_file_time_value_eifc = str(self.get_time_step())[5:]
        elif self.time_step_level == "minutes":
            self.data_file_time_value_eifc = str(self.get_time_step())[2:4]
        elif self.time_step_level == "hours":
            self.data_file_time_value_eifc = str(self.get_time_step())[0:1]
        elif self.time_step_level == "days":
            self.data_file_time_value_eifc = str(self.get_time_step())[0:2]
        elif self.time_step_level == "months":
            if isinstance(self.get_time_step(), int):
                self.data_file_time_value_eifc = str(self.get_time_step())[0:2]
            else:
                self.data_file_time_value_eifc = str(int(self.get_time_step().days//30))[0:2]
        self.data_file_time_value_eifc = self.data_file_time_value_eifc.zfill(2)

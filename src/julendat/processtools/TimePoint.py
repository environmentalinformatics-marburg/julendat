'''
Created on Aug 13, 2011

@author: tnauss
'''


import datetime
import time

class TimePoint(object):
    '''
    classdocs
    '''


    def __init__(self,time_value):
        '''
        Constructor
        '''
        if  isinstance(time_value, str):
            if len(time_value) == 12:
                self.set_y2i_dto_from_string(time_value)
            elif len(time_value) == 14:
                self.set_y2s_dto_from_string(time_value)
        else:
            self.dto = time_value
            self.set_y2i_string_from_dto(time_value)
            self.set_y2s_string_from_dto(time_value)
        
        self.set_data_file_values()
            
    def set_y2i_dto_from_string(self, time_string):
        self.dto = datetime.datetime.strptime(time_string, "%Y%m%d%H%M")
        self.set_y2i_string(time_string)

    def set_y2s_dto_from_string(self, time_string):
        self.dto = datetime.datetime.strptime(time_string, "%Y%m%d%H%M%S")        
        self.set_y2s_string(time_string)        

    def get_dto(self):
        return self.dto

    def set_y2i_string(self, time_string):
        self.y2i_string = time_string

    def get_y2i_string(self):
        return self.y2i_string

    def set_y2s_string(self, time_string):
        self.y2s_string = time_string

    def get_y2s_string(self):
        return self.y2s_string
        
    def set_y2i_string_from_dto(self, time_dto):
        self.set_y2i_string(time.strftime("%Y%m%d%H%M", time_dto.timetuple()))
        
    def set_y2s_string_from_dto(self, time_dto):
        self.set_y2s_string(time.strftime("%Y%m%d%H%M%S", time_dto.timetuple()))

    def set_data_file_values(self):
        self.set_data_file_time_value()
        self.set_data_file_time_value_str()
    
    def set_data_file_time_value(self):
        self.data_file_time_value = self.get_dto()
    
    def set_data_file_time_value_str(self):
        self.data_file_time_value_str = self.get_y2i_string()
            
    def get_data_file_time_value(self):
        return self.data_file_time_value
    
    def get_data_file_time_value_str(self):
        return self.data_file_time_value_str

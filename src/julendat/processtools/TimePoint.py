'''
Created on Aug 13, 2011

@author: tnauss
'''


import datetime
import time

class TimePoint(object):


    def __init__(self,time_value):

        if  isinstance(time_value, str):
            if len(time_value) == 10 and time_value[4] == "-":
                self.set_y2d_dto_from_isostr(time_value)
            elif len(time_value) == 12:
                self.set_y2i_dto_from_eifc(time_value)
            elif len(time_value) == 14:
                self.set_y2s_dto_from_eifc(time_value)
        else:
            self.dto = time_value
            self.set_y2i_eifc_from_dto(time_value)
            self.set_y2s_eifc_from_dto(time_value)
            self.set_y2s_isostr_from_dto(time_value)
        
        self.set_data_file_values()
            
    def set_y2d_dto_from_isostr(self, time_string):
        self.dto = datetime.datetime.strptime(time_string, "%Y-%m-%d")
        self.set_y2i_eifc_from_dto(self.get_dto())
        self.set_y2s_isostr_from_dto(self.dto)

    def set_y2i_dto_from_eifc(self, time_string):
        self.dto = datetime.datetime.strptime(time_string, "%Y%m%d%H%M")
        self.set_y2i_eifc(time_string)
        self.set_y2s_isostr_from_dto(self.dto)

    def set_y2s_dto_from_eifc(self, time_string):
        self.dto = datetime.datetime.strptime(time_string, "%Y%m%d%H%M%S")        
        self.set_y2s_eifc(time_string)        
        self.set_y2s_isostr_from_dto(self.dto)

    def get_dto(self):
        return self.dto

    def set_y2i_eifc(self, time_string):
        self.y2i_eifc = time_string

    def get_y2i_eifc(self):
        return self.y2i_eifc

    def set_y2s_eifc(self, time_string):
        self.y2s_eifc = time_string

    def set_y2s_isostr(self, time_string):
        self.y2s_isostr = time_string
        
    def get_y2s_eifc(self):
        return self.y2s_eifc

    def get_y2s_isostr(self):
        return self.y2s_isostr
            
    def set_y2i_eifc_from_dto(self, time_dto):
        self.set_y2i_eifc(time.strftime("%Y%m%d%H%M", time_dto.timetuple()))
        
    def set_y2s_eifc_from_dto(self, time_dto):
        self.set_y2s_eifc(time.strftime("%Y%m%d%H%M%S", time_dto.timetuple()))

    def set_y2s_isostr_from_dto(self, time_dto):
        self.set_y2s_isostr(time.strftime("%Y-%m-%d %H:%M:%S", time_dto.timetuple()))

    def set_data_file_values(self):
        self.set_data_file_time_value()
        self.set_data_file_time_value_eifc()
        self.set_data_file_time_value_isostr()
    
    def set_data_file_time_value(self):
        self.data_file_time_value = self.get_dto()
    
    def set_data_file_time_value_eifc(self):
        self.data_file_time_value_eifc = self.get_y2i_eifc()

    def set_data_file_time_value_isostr(self):
        self.data_file_time_value_isostr = self.get_y2s_isostr()
                    
    def get_data_file_time_value(self):
        return self.data_file_time_value

    def get_data_file_time_value_eifc(self):
        return self.data_file_time_value_eifc
    
    def get_data_file_time_value_isostr(self):
        return self.data_file_time_value_isostr
'''
Created on Aug 13, 2011

@author: tnauss
'''


import time
import datetime




def convert_timezone(time_value=None, time_zone=None):
    time_zone = "eat"
    if time_zone == "eat": 
        time_value = time_value + datetime.timedelta(minutes=120)

    return time_value
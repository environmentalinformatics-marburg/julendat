'''
Created on Aug 13, 2011

@author: tnauss
'''


import datetime




def convert_timezone(time_value=None, time_zone=None):
    if time_zone == "eat": 
        time_value = time_value + datetime.timedelta(minutes=120)
    elif time_zone == "mez": 
        time_value = time_value + datetime.timedelta(minutes=0)

    return time_value

def timezone_difference(time_zone=None):
    if time_zone == "eat": 
        time_difference = 2*60*60
    elif time_zone == "mez": 
        time_difference = 0*60*60
    return time_difference
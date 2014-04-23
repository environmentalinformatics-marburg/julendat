"""Create timeseries of climate elements.
Copyright (C) 2012 Insa Otte

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

__author__ = "Insa Otte"
__version__ = "2012-01-16"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import datetime
import time
import optparse
import os
import csv
import sys

def main():
    """Main program function
    Create timeseries of climate elements
    """
    print
    print 'Module: timeseries of climate elements'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print

    # Set framework for command line arguments and runtime configuration.
    parser = optparse.OptionParser(\
        "usage: %prog [options] data_file_01 " + \
        "data_file_02")
    parser.add_option("-s","--sdt", dest="start_datetime",  \
        default = "1900", \
        help="Start year of the output time series (YYYY).", \
        metavar="integer", type="int")
    parser.add_option("-e","--edt", nargs=1, dest="end_datetime",  \
        default = "2014", \
        help="End year of the output time series (YYYY)", \
        metavar="integer", type="int")
    parser.add_option("-p", "--pla", dest="top_level_station_path", \
        default = "/home/dogbert/workspace/Explo_split/", \
        help = "Name of top level station path", \
        metavar="string", type="str")
    parser.add_option("-o", "--out", dest="output_path", \
        default = "/home/dogbert/workspace/", \
        help = "Name of output path", \
        metavar="string", type="str")
    parser.set_description('Options for module timeseries.')
    (options, args) = parser.parse_args()

    if options.top_level_station_path == None:
        parser.print_help()
    else:
        top_level_station_path = options.top_level_station_path   
    start_datetime = options.start_datetime
    end_datetime = options.end_datetime
    output_path = options.output_path

    # Look for subfolders in top level path
    data_output = []
    a = os.walk(top_level_station_path)

    for station_id in a.next()[1]:
        print station_id
        station_path = top_level_station_path + os.sep + station_id

        # Set filepath with respect to actual station
        act_file_1 = station_path + os.sep + "de.dwd.nkdz.TAMM.xml"
        act_file_2 = station_path + os.sep + "de.dwd.nkdz.RRMS.xml"
        act_file_3 = station_path + os.sep + "de.dwd.nkdz.SDMS.xml"

        outfile = output_path + os.sep + "stations.txt"

        print "Processing files:"
        print act_file_1
        print act_file_2
        print act_file_3
        print outfile
        
        # Check if input files exist
        ta_exists = False
        p_exists = False
        sd_exists = False
        if os.path.isfile(act_file_1):
            ta_exists = True
            data_1 = open(act_file_1, 'r')
        if os.path.isfile(act_file_2):
            p_exists = True
            data_2 = open(act_file_2, 'r')
        if os.path.isfile(act_file_3):
            sd_exists = True
            data_3 = open(act_file_3, 'r')
       
        # Open files
        header =  "Datetime, Aggregationtime, Station, lat, lon, " + \
                  "alt, Qualityflag, Ta_200, P_RT_NRT, SD"
        
        first_row = False
        lat = False
        lon = False
        alt = False
        dataset_1 = []
        if ta_exists:
            for row in data_1:
                try:
                    date = row.split(">")[0].split('"')[1]
                    value_1 = float(row.split(">")[1].split("<")[0])
                    dataset_1.append([date, value_1])
                    if first_row == False:
                        lat = row.split('"')[5]
                        lon = row.split('"')[7]
                        alt = row.split('"')[9]
                        first_row = True
                except:
                    continue
    
        dataset_2 = []
        if p_exists:
            for row in data_2:
                try:
                    date = row.split(">")[0].split('"')[1]
                    value_2 = float(row.split(">")[1].split("<")[0])
                    dataset_2.append([date, value_2])
                    if first_row == False:
                        lat = row.split('"')[5]
                        lon = row.split('"')[7]
                        alt = row.split('"')[9]
                        first_row = True
                except:
                    continue

        dataset_3 = []
        if sd_exists:
           for row in data_3:
               try:
                   date = row.split(">")[0].split('"')[1]
                   value_3 = float(row.split(">")[1].split("<")[0])
                   dataset_3.append([date, value_3])
                   if first_row == False:
                        lat = row.split('"')[5]
                        lon = row.split('"')[7]
                        alt = row.split('"')[9]
                        first_row = True
               except:
                   continue
        
        print len(dataset_1)
        print len(dataset_2)
        print len(dataset_3)
        
        for act_year in range(start_datetime, end_datetime+1):
            for act_month in range(1, 13):
                act_time = str(act_year) + "-" + str(act_month)
                act_time = datetime.datetime.strptime(act_time, \
                                                      "%Y-%m")
                temp = [time.strftime("%Y-%m",act_time.timetuple())]
                temp = temp + ["s1m01"] + [station_id] + [lat] + \
                       [lon] + [alt] + ['xxxxxxxxx']              

                found_corresponding_data = False
                for i in range(len(dataset_1)):
                    if act_time == datetime.datetime.strptime(\
                                       dataset_1[i][0],"%Y-%m"):
                        temp = temp + [dataset_1[i][1]]
                        found_corresponding_data = True
                if found_corresponding_data != True:
                    temp = temp + ['NaN']  
        
                found_corresponding_data = False
                for i in range(len(dataset_2)):
                    if act_time == datetime.datetime.strptime(\
                                       dataset_2[i][0],"%Y-%m"):
                        temp = temp + [dataset_2[i][1]]
                        found_corresponding_data = True
                if found_corresponding_data != True:
                    temp = temp + ['NaN']
        
                found_corresponding_data = False
                for i in range(len(dataset_3)):
                    if act_time == datetime.datetime.strptime(\
                                       dataset_3[i][0],"%Y-%m"):
                        temp = temp + [dataset_3[i][1]]
                        found_corresponding_data = True
                if found_corresponding_data != True:
                    temp = temp + ['NaN']
            
                data_output.append(temp)
        
    print "Writing data..."
    outfile = open(outfile,"w")
    outfile.write(header + '\n')
    writer = csv.writer(outfile, delimiter=',')
    for row in data_output:
        writer.writerow(row)
    outfile.close()
        
if __name__ == '__main__':
    main()

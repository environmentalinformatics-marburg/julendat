# Module eumeltools
"""Provide general functions for our pyhton modules.

The current version encompasses the following functions:
-- function mask_dimensions: Create array mask with respect to dimensions
-- function mask_values: Create array mask with respect to min/max values
-- function array_read: Read data from a textfile into an n-dimensional array.
-- function string_contains_any: Check if string contains any of search term.
-- function string_contains_all: Check if string contains all of search term.
-- function string_matches_all: Check if string contains exact search term.
-- function set_bit: Set a specific bit
-- function clear_bit: Clear a specific bit
-- function check_bit: Check a specific bit
-- function next_neighbor: Perform a next_neighbor interpolation 

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
"""

import numpy
import sys
import re

__author__ = "Thomas Nauss <thomas.nauss@uni-bayreuth.de>"
__version__ = "2011-11-02"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"


def mask_dimensions(datadimensions, dimension_ranges):
    """Mask array with respect to array dimensions.

    mask_dimensions(datadimensions, dimension_ranges)
    
    Keyword arguments:
    -- datadimensions: Dimensions of the dataset for which the map is created
    -- dimension_ranges: Tuple containing ranges of the dimensions (dim1, dim2)

    """

    print 'Set map for dataset with respect to array dimensions...'
    row_range, col_range = dimension_ranges
    if row_range is None:
        row_range = 0, datadimensions[0]
    if col_range is None:
        col_range = 0, datadimensions[1]
    mask = numpy.zeros((datadimensions[0],
                        datadimensions[1]),'f')
    for row in range(row_range[0],row_range[1]):
        for col in range(col_range[0],col_range[1]):
            mask[row,col] = 1.0
   
    mask_1d = numpy.ravel(mask)
    return mask, mask_1d


def mask_values(datasets, value_range):
    """Mask array with respect to array values.

    mask_values(datasets, value_range)
    
    Keyword arguments:
    -- datasets: Array or tuple of arrays containing dataset values
    -- value_range: Value range for which the map should be created (min,max)

    """

    print 'Set map for dataset with respect to array values...'
    if value_range is None:
        value_range = numpy.min(datasets), numpy.max(datasets)
    mask = {}
    setcounter = -1
    if isinstance(datasets, tuple):
        for dataset in datasets:
            setcounter = setcounter + 1
            mask[setcounter] = numpy.logical_and(dataset >= value_range[0],
                                                 dataset <= value_range[1])
    else:
        setcounter = setcounter + 1
        mask[setcounter] = numpy.logical_and(datasets >= value_range[0],
                                             datasets <= value_range[1])
    
    if setcounter > 0:
        for maskcounter in range(setcounter):
            mask[0] = numpy.logical_and(mask[maskcounter],mask[maskcounter+1])

    mask_1d = numpy.ravel(mask[0])

    # Return value_range, too, since it might have been None in the begining.
    return mask[0], mask_1d, value_range


def array_read(filename, datatype, skip):
    """Read data from an array-like ASCII file
    
    Read data from ASCII file with an arbitrary number of columns and arbitrary
    types of data for each column. The data is returned in a multidimensional
    array.
    
    array_read(filename, datatype, skip):

    Keyword arguments:
    -- filename: Name of the input file
    -- datatype: Datatype of each column, comma seperated
                 ('string'=string, 'int16'=integer, 'float32'=float)
    -- skip: Number of lines to be skiped in the begining of the file
        
    """

    # Check if file exists and open it; exit if not.
    try:
        file = open(filename, 'r')
    except IOError:
        print 'File not found: ' + filename
        sys.exit()

    # Initialize an array with n dimensions
    # (one for each datatype defined in datatype).
    data = [[] for dummy in xrange(len(datatype))]

    # Read input file line by line, split each line into several columns
    # and write the first n columns into the data array.
    for iCounter in range (skip):
        file.readline()
    for line in file:
        fields = line.strip().split()
        for i in xrange(len(datatype)):
            data[i].append(fields[i])

    # Convert datatypes of each column according to the user defined datatypes.
    for i in xrange(len(datatype)):
        data[i] = numpy.cast[datatype[i]](data[i])
    file.close()
    return data


def string_contains_any(string,search_term):
    """Check if string contains any of the search term and return True/False.
    
    string_contains_any(string, search_term)
    
    Keyword arguments:
    -- string: String to be searched.
    -- search_term: Search term.
        
    """

    return 1 in [check in string for check in search_term]


def string_contains_all(string, search_term):
    """Check if string contains all of the search term and return True/False.
    
    string_contains_all(string, search_term)
    
    Keyword arguments:
    -- string: String to be searched.
    -- search_term: Search term.
        
    """

    return 0 not in [check in string for check in search_term]


def string_matches_all(string, search_term):
    """Check if a string contains the exact search term and return True/False.
    
    string_matches_all(string, search_term)
    
    Keyword arguments:
    -- string: String to be searched.
    -- search_term: Search term.
        
    """

    return re.search(search_term, string)


def set_bit(value, bit_number):
    """Set a specific bit to 1.
    
    set_bit(value, bit_number)
    
    Keyword arguments:
    -- value: Value in which bit should be set.
    -- bit_number: Bit number to be set to 1.
        
    """

    return value | 1 << (bit_number)


def clear_bit(value, bit_number):
    """Set a specific bit to 0.
    
    clear_bit(value, bit_number)
    
    Keyword arguments:
    -- value: Value in which bit should be cleared.
    -- bit_number: Bit number to be set to 0.
        
    """

    return value & ~( 1 << (bit_number) )


def check_bit(value, bit_number):
    """Check if a specific bit is 1/0 (True/False).
   
    check_bit(value, bit_number)
    
    Keyword arguments:
    -- value: Value in which bit should be checked.
    -- bit_number: Bit number to be checked.
        
    """

    return (value & (1<<(bit_number))) != 0


def next_neighbor(data, target_row, target_col,row_extend,col_extend):
    """Compute a next neighbor interpolation.
    
    Set value of the actual row,col position of a 2D array according to a
    next neighbor resampling.
    
    next_neighbor(data, target_row, target_col)
    
    Keyword arguments:
    -- data: Rank 2 array [row,col] containing all data values (invalid = -1)
    -- target_row: Row position for which the value should be resampled.
    -- target_col: Col position for which the value should be resampled.
    -- row_extend: Minimum [0] and maximum [1] row in data with valid values.
    -- col_extend: Minimum [0] and maximum [1] col in data with valid values.
        
    """
    
    search_pattern_row = [-1,1,0,0,-1,1,1,-1]
    search_pattern_col = [0,0,-1,1,-1,-1,1,1]
    rows = data.shape[0]
    cols = data.shape[1]
    target_val = -1.0
    found = False
    run = 0
    while run < 50 and found == False:
        run = run + 1
        search = 0
        while search <= 7 and found == False:
            search_row = target_row + run*search_pattern_row[search]
            search_col = target_col + run*search_pattern_col[search]
            if search_row >= row_extend[0] and \
               search_row <= row_extend[1] and \
               search_col >= col_extend[0] and \
               search_col <= col_extend[1]:
                if data[search_row,search_col] >= 0.0:
                    target_val = data[search_row,search_col]
                    found = True
            search = search + 1

    return target_val


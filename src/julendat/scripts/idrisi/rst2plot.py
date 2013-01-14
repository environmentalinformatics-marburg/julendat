"""Create publication quality plots from Idrisi raster files.
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

__author__ = "Thomas Nauss <nausst@googlemail.com>"
__version__ = "2012-01-04"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"

import numpy
import optparse
import os
from julendat.filetools.raster.idrisi.IdrisiDataFile import IdrisiDataFile 
from julendat.plottingtools.Data2Plot import Data2Plot
from julendat.processtools import eumeltools

#TODO(tnauss): Adjust to julendat.

def main():
    """Main program function
    Create publication quality maps from Idrisi raster files.
    """
    print
    print 'Module: rst2plot'
    print 'Version: ' + __version__
    print 'Author: ' + __author__
    print 'License: ' + __license__
    print

    # Set framework for command line arguments and define runtime configuration.
    parser = optparse.OptionParser("usage: %prog [options] data_files")
    parser.add_option("-o", "--out", dest="output_plotfile",
                      help="Full path/name of the output plot(s) (can be tuple).",
                      metavar="string")
    parser.add_option("-c", "--col", nargs=2, dest="col_range",
                      help="Col range of dataset included in plot (default: all).",
                      metavar="int", type=int)
    parser.add_option("-r", "--row", nargs=2, dest="row_range",
                      help=" range of dataset included in plot (default: all).",
                      metavar="int", type=int)
    parser.add_option("-v", "--val", nargs=2, dest="value_range",
                      help="Value range to be considered (default: all).",
                      metavar="float", type=float)
    parser.add_option("-f", "--fil", dest="colormap",
                      help="Colormap used for some plots (default: see Data2Plot).",
                      metavar="string")
    parser.add_option("-x", "--xlb", dest="xlabel",
                      help="Label for first input file (default: file id).",
                      metavar="string")
    parser.add_option("-y", "--ylb", dest="ylabel",
                      help="Label for second input file (default: file id).",
                      metavar="string")
    parser.add_option("-t", "--til", nargs=2, dest="title",
                      help="Title for plots (default: file id).",
                      metavar="string")
    parser.set_description('Options for module rst2plot.')
    (options, args) = parser.parse_args()
    
    if len(args) != 2:
        parser.print_help()
        parser.error("No input file(s) given.")
    
    # Set filenames and variables
    scenes ={}
    for i in range(len(args)):
        scenes[i] = args[i]
    if options.output_plotfile != None: 
        output_plotfile = options.output_plotfile
    else:
        output_plotfile = os.getcwd() + os.sep + "plot.png"
    if options.col_range != None: 
        col_range = (options.col_range[0],options.col_range[1]+1)
    else:
        col_range = None
    if options.row_range != None: 
        row_range = (options.row_range[0],options.row_range[1]+1)
    else:
        row_range = None
    if options.value_range != None: 
        value_range = (options.value_range)
    else:
        value_range = None
    if options.colormap != None: 
        colormap = options.colormap
    else:
        colormap = None
    if options.xlabel != None: 
        xlabel = options.xlabel
    else:
        xlabel = None
    if options.ylabel != None: 
        ylabel = options.ylabel
    else:
        ylabel = None
    if options.title != None: 
        title = options.title
    else:
        title = None
    
    # Read Idrisi datasets
    print 'Reading latitude/longitude and variable data..'
    scene = {}
    for i in range(len(scenes)):
        scene[i] = IdrisiDataFile(scenes[i],'rst')
    
    # Set title and labels for axis and legend 
    if title is None:
        title = scene[0].get_variable_name(), scene[1].get_variable_name()
    if xlabel is None:
        xlabel = scene[0].get_variable_name()
    if ylabel is None:
        ylabel = scene[1].get_variable_name()
    
    # Set array map with respect to col/row range
    dummy, mask_dimensions = \
        eumeltools.mask_dimensions((scene[0].get_metadata()['rows'],
                                    scene[0].get_metadata()['cols']),
                                    (row_range, col_range))
    
    # Set array map with respect to value range
    dummy, mask_values, dummy = \
        eumeltools.mask_values((scene[0].get_data(),scene[1].get_data()),
                               value_range)
    
    # Set final mask and compress dataset arrays
    mask = numpy.logical_and(mask_dimensions, mask_values)
    data = {}
    data[0] = numpy.ravel(scene[0].get_data())
    data[0] = numpy.compress(mask==1,scene[0].get_data())
    data[1] = numpy.ravel(scene[1].get_data())
    data[1] = numpy.compress(mask==1,scene[1].get_data())

    # Initialize plot class and create plots
    print 'Initializing plot class...'
    plot = Data2Plot((data[0], data[1]), output_plotfile,
                     title, xlabel, ylabel,
                     value_range, colormap)
    plot.compute_statistics()
    plot.make_scatterplot()
    plot.make_errorplot()
    plot.make_hexplot()
    plot.make_hexerrorplot()
    plot.make_histogramplot()
    
    print '...finished.'

if __name__ == '__main__':
    main()

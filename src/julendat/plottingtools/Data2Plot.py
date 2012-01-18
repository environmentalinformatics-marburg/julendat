"""Create publication-quality plots.
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
__version__ = "2011-11-02"
__license__ = "GNU GPL, see http://www.gnu.org/licenses/"
import pylab
import matplotlib.cm as cm
from scipy import stats


class Data2Plot(object):
    """Instance for creating publication-quality plots.
    
    The instance is a representation of a DTP plot object and includes
    the following functions:

        function compute_statistics: Compute basic regression statistics to be
            included in histogram plot title
        function compute_ratio: Compute ratio of the two input datasets to
            produce error plots
        function make_scatterplot: Create a publication-quality scatterplot                      
        function make_error plot: Create a publication-quality error plot                     
        function make_hexplot: Create a publication-quality hexagon scatter plot                      
        function make_hexerrorplot: Create a publication-quality hexagon error
            plot                      
        function make_histogramplot: Create a publication-quality histogram plot                    
    """

    def __init__(self, datasets, plotfile,
                 title=None, xlabel=None, ylabel=None,
                 value_range=None, colormap=None):
        """Inits Data2Map.
        
        Args:
            datasets : Two numpy arrays holding the actual data values
            plotfile : String or tuple with full path of the output plot file(s)
            title : Title of the plot files (default: None)
            xlabel : Label of the x axis (default: None)
            ylabel : Label of the y axis (default: None)
            value_range : Range of values to be plotted (default: all)
            colormap : matplotlib.cm colormap for hexagon plots (default: Greys)
        """
        self.dataset = {}
        self.dataset[0], self.dataset[1] = datasets
        self.plotfile = plotfile
        if title is None:
            self.title = 'file #1','file #2'
        else:
            self.title = title
        if xlabel is None:
            self.xlabel = ''
        else:
            self.xlabel = xlabel
        if ylabel is None:
            self.ylabel = ''
        else:
            self.ylabel = ylabel
        if value_range is None:
            self.value_range = min(min(self.dataset[0]),min(self.dataset[1])), \
                               max(max(self.dataset[0]),max(self.dataset[1]))
        else:
            self.value_range = value_range
        if colormap is None:
            self.colormap = cm.ScalarMappable(cmap='Greys').get_cmap()
        else:
            self.colormap = cm.ScalarMappable(cmap=colormap).get_cmap()
        if colormap == 'Greys' or colormap is None:
            self.pylabplotcolor1 = 'k'
            self.pylabplotcolor2 = '0.50'
        else:
            self.pylabplotcolor1 = 'b'
            self.pylabplotcolor2 = 'r'
        self.ratio = None
        self.slope  = None
        self.intercept = None
        self.r = None
        self.r2 = None


    def compute_statistics(self):
        """Make some statistics that can be included into the histogram plots.
        """
        self.slope, self.intercept, self.r = \
            stats.linregress(self.dataset[0], self.dataset[1])[0:3]
        self.r2 = self.r**2
        print 'Statistic results (slope, intercept, r, r2) are:'
        print self.slope, self.intercept, self.r, self.r2


    def compute_ratio(self):
        """Compute ratio of the two input datasets in order to 
        produce error plots.
        """
        if self.ratio is None:
            self.ratio = self.dataset[1] / self.dataset[0]


    def make_scatterplot(self):
        """Make scatterplot using the pylab plot function.
        """
        print 'Creating scatterplot...'
        pylab.clf()
        pylab.figure(figsize=(8,8))
        pylab.axis('scaled')
        pylab.plot(self.dataset[0], self.dataset[1], self.pylabplotcolor1+'.')
        pylab.axis([self.value_range[0]-1, self.value_range[1]+1,
                    self.value_range[0]-1, self.value_range[1]+1])
        pylab.xlabel(self.xlabel, fontsize=20)
        pylab.ylabel(self.ylabel, fontsize=20)
        pylab.title(self.title[0] + ' vs. ' + self.title[1])
        pylab.grid(True)
        if isinstance(self.plotfile, str):
            pylab.savefig(self.plotfile[:-4] + '_scatter' + self.plotfile[-4:])
        elif isinstance(self.plotfile, tuple):
            for filename in self.plotfile:
                pylab.savefig(filename[:-4] + '_scatter' + filename[-4:])
        pylab.clf()


    def make_errorplot(self):
        """Make errorplot using the pylab plot function.
        """
        print 'Creating error plot...'
        self.compute_ratio()
        pylab.clf()
        pylab.figure(figsize=(8,8))
        pylab.plot(self.dataset[0], self.ratio, self.pylabplotcolor1+'o')
        pylab.axis([self.value_range[0], self.value_range[1], 0.0, 2.0])
        pylab.xlabel(self.xlabel, fontsize=20)
        pylab.ylabel(self.ylabel + '/' + self.xlabel, fontsize=20)
        pylab.title(self.title[0] + ' / ' + self.title[1])
        pylab.grid(True)
        if isinstance(self.plotfile, str):
            pylab.savefig(self.plotfile[:-4] + '_error' + self.plotfile[-4:])
        elif isinstance(self.plotfile, tuple):
            for filename in self.plotfile:
                pylab.savefig(filename[:-4] + '_error' + filename[-4:])
        pylab.clf()

    
    def make_hexplot(self):
        """Make hexagon scatter plot using the pylab plot function.
        """
        print 'Creating hexagon plot...'
        pylab.clf()
        pylab.figure(figsize=(8,8))
        pylab.axis('scaled')
        pylab.hexbin(self.dataset[0], self.dataset[1],
                     bins='log', cmap=self.colormap)
        pylab.colorbar().set_label('log10(N)')
        pylab.axis([self.value_range[0]-1, self.value_range[1]+1,
                    self.value_range[0]-1, self.value_range[1]+1])
        pylab.xlabel(self.xlabel, fontsize=20)
        pylab.ylabel(self.ylabel, fontsize=20)
        pylab.title(self.title[0] + ' vs. ' + self.title[1])
        pylab.grid(True)
        if isinstance(self.plotfile, str):
            pylab.savefig(self.plotfile[:-4] + '_hexbin' + self.plotfile[-4:])
        elif isinstance(self.plotfile, tuple):
            for filename in self.plotfile:
                pylab.savefig(filename[:-4] + '_hexbin' + filename[-4:])
        pylab.clf()


    def make_hexerrorplot(self):
        """Make hexagon error plot using the pylab plot function.
        """
        print 'Creating hexagon error plot...'
        self.compute_ratio()
        pylab.clf()
        pylab.figure(figsize=(8,8))
        pylab.hexbin(self.dataset[0], self.ratio, bins='log',
                     cmap=self.colormap)
        pylab.colorbar().set_label('log10(N)')
        pylab.axis([self.value_range[0], self.value_range[1], 0.0, 2.0])
        pylab.xlabel(self.xlabel, fontsize=20)
        pylab.ylabel(self.ylabel + '/' + self.xlabel, fontsize=20)
        pylab.title(self.title[0] + ' / ' + self.title[1])
        pylab.grid(True)
        if isinstance(self.plotfile, str):
            pylab.savefig(self.plotfile[:-4] + '_hexbin_error' + 
                          self.plotfile[-4:])
        elif isinstance(self.plotfile, tuple):
            for filename in self.plotfile:
                pylab.savefig(filename[:-4] + '_hexbin_error' + filename[-4:])
        pylab.clf()


    def make_histogramplot(self):
        """Make histogram plot using the pylab plot function.
        """
        print 'Creating histogram plot...'
        max_b = (int(self.value_range[1]) + 1)*5
        b = range(0,max_b)
        for t in range(0,max_b):
                b[t] = float(t)/5.0
        pylab.figure(figsize=(8,8))
        n0, bins0, patches0 = pylab.hist(self.dataset[0], 
                                         bins=b, normed=1, histtype='step',
                                         facecolor='b', edgecolor=self.pylabplotcolor1,
                                         visible=1)
        n1, bins1, patches1 = pylab.hist(self.dataset[1], 
                                         bins=b, normed=1, histtype='step',
                                         facecolor='r', edgecolor=self.pylabplotcolor2,
                                         visible=1)
        pylab.xlabel(self.xlabel)
        pylab.ylabel('Frequency')
        if self.r is None:
            pylab.title('')
        else:
            pylab.title('r = ' + str(self.r) + ',r2 = ' + str(self.r2))
        pylab.legend( (patches0[0], patches1[0]), 
                      (self.xlabel,self.ylabel), shadow=True)
        if isinstance(self.plotfile, str):
            pylab.savefig(self.plotfile[:-4] + '_histogram' + 
                          self.plotfile[-4:])
        elif isinstance(self.plotfile, tuple):
            for filename in self.plotfile:
                pylab.savefig(filename[:-4] + '_histogram' + filename[-4:])
        pylab.clf()

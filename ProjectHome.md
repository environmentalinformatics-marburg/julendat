## Utilities for handling environmental data sets ##

The julendat framework combines tools for handling and processing environmental data sets. A data set in this context is an ASCII or binary file. In general, such a data file is associated with metadata provided within the file (e. g. HDF) or as a separate file (e. g. Idrisi raster format).

Julendat has just been started and is work in progress. However, all routines included in this repository are functional.

The individual data sets are organized by their data structure and source and are implemented as class objects. So far, the following data sets can be handled (better or worse):
- Station data (i. e. tabulated datasets)
- Raster data (Idrisi raster format, HDF EOS)

With respect to data handling and processing, the following options are implemented:
- Station data: Import initial climate station logger files from Driesen & Kern loggers and process climate station data sets from level 0 to level 1
- Raster data: Generate press quality maps, plots and histogramms.

In the near future you will find more information on the [wiki](JulendatMain.md) pages.

<br>

<h2>Implementation</h2>
The processing modules are generally implemented in Python. Statistical data processing functions use R routines in addition.<br>
<br>
<br>

<h2>Coming up next</h2>
During the next month we will include data quality correction routines for the station data sets.<br>
<br>
<br>

<h2>Pre-defined modules for handling data sets with julendat</h2>
Please refer to <a href='http://code.google.com/p/julendat-processing-packages/source/checkout'>julendat processing packages</a> to get access to existing modules which utilize the julendat framework. These modules can be used as is to e. g. create publication quality maps/plots or perform the station data processing. To get information on how to run the modules just type<br>
<br>
<code>python name-of-the-module.py</code>

at the command prompt. The <code>PYTHONPATH</code> must include the <code>src</code> directory of the julendat package.<br>
<br>
In the near future you will find more information on the Wiki pages.<br>
<br>
<br>

<h2>Homepage</h2>
You can find our homepage at <a href='http://environmentalinformatics-marburg.de/'>http://environmentalinformatics-marburg.de/</a>

<a href='http://environmentalinformatics-marburg.de/'><img src='http://umweltinformatik-marburg.de/fileadmin/templates/images/Logos/logo.png' /></a>
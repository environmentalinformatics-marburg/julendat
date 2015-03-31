# What is julendat? #

The julendat framework combines tools for handling and processing environmental data sets. A data set in this context is an ASCII or binary file. In general, such a data file is associated with metadata provided within the file (e. g. HDF) or as a separate file (e. g. Idrisi raster format).

The individual data sets are organized by their data structure and source and are implemented as class objects. So far, the following data sets can be handled (better or worse): - Station data (i. e. tabulated datasets) - Raster data (Idrisi raster format, HDF EOS)

With respect to data handling and processing, the following options are implemented:
  * Station data: Import initial climate station logger files from different logger manufactors and process station data sets to higher level products (e.g. time aggregation, quality control, gap filling)
  * Raster data: Generate press quality maps, plots and histogramms.
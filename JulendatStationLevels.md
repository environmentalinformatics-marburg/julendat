# What is a process level? #

A process level denotes a certain state of processing to a specific dataset. Raw data is generally marked as level 0, higher level data is marked as e. g. 0.5, 1.0, 2.5. In julendat, a 4 digit process level is used with the rightmost 2 digits representing the decimal places. Hence, a level 0 file has the id 0000 and a level 1.5 file would be 0150.

# What process levels are included in julendat? #

The file format for station data processing is comma separated with dots as decimal character. Each line represents one recording time.

For station data processing, the following levels are included in julendat:

  * ProcessLevel0000: Initial import of the logger data. The file name is adjusted to fit the [julendat naming convention](StationNamingConvention.md).
  * ProcessLevel0005: Adjustment of file header to a single-line header and inclusion of 8 columns (column 1 to 8). These columns are also included in all higher level products. The information given in these columns are
    * Datetime: Date and time of the record
    * Timezone: Time zone of the time information
    * Aggregationtime: Time over which the respective measurements are aggregated
    * PlotId: Id of the observation plot
    * EpPlotId: Alternative id of the observation plot
    * StationId: Id of the station type
    * Processlevel: Process level
    * Qualityflag: Quality flag
    * CycleCounter: This parameter is only included in some datasets. It gives the number of individual measurements which have been aggregated to the actual stored value (e. g. if the storage interval is one hour, this counter is most likely 59).
    * ProcessLevel0050: Calibration of data values (e. g. conversion of voltage to radiation)
    * ProcessLevel0100: Quality check of initial data values (i.e. level 0050) with respect to value range and value change over time.
    * ProcessLevel0200: Hourly aggregation of data values. New columns are included in the file given some additional statistics. The paramters will be
      * xxx: Aggregated parameter value (e.g. for mean temperature, the column header is Ta\_200)
      * xxx\_min: Minimum parameter value recorded during the aggregation interval (e.g. Ta\_200\_min)
      * xxx\_max: Maximum parameter value recorded during the aggregation interval (e.g. Ta\_200\_max)
      * xxx\_median: Median parameter value recorded during the aggregation interval (e.g. Ta\_200\_median)
      * xxx\_stdv: Standard deviation of the parameter values recorded during the aggregation interval (e.g. Ta\_200\_max)
      * xxx\_25: 25% percentil of the parameter values recorded during the aggregation interval (e.g. Ta\_200\_25)
      * xxx\_75: 75% percentil of the parameter values recorded during the aggregation interval (e.g. Ta\_200\_75)
      * xxx\_n: Number of parameter values used during the aggregation interval (i.e. equal meaning as CycleCounter above, e.g. Ta\_n)
      * xxx\_nan: Number of data gaps during the aggregation interval (e.g. Ta\_200\_nan)
    * [ProcessLevel0250](ProcessLevel0100.md): Second quality check this time for the aggregated level 0200 parameters
    * ProcessLevel0300 and 310: Generation of continous hourly time series where data gaps are filled.
    * ProcessLevel0400: Generation of monthly aggregated files
    * ProcessLevel0405: Generation of daily aggregated files
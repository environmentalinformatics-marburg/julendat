
setClass("be.data",
         representation(
           Datetime = "POSIXct",
           Date = "list",
           Time = "list",
           Origin = "character",
           Timezone = "character",
           Aggregationtime = "character",
           PlotId = "list",
           EpPlotId = "character",
           StationId = "list",
           Processlevel = "character",
           Qualityflag = "character",
           CycleCounter = "numeric",
           Parameter = "list"
           )
         )

as.be.data <- function(input_filepath) {
  
  df <- read.table(input_filepath, header = T, sep = ",", fill = T,
                   stringsAsFactors = F, na.strings = "", as.is = T)
  
  year <- substr(df$Datetime, 1, 4)
  month <- substr(df$Datetime, 6, 7)
  day <- substr(df$Datetime, 9,10)
  hour <- substr(df$Datetime, 12, 13)
  minute <- substr(df$Datetime, 15, 16)
  origin <- paste(year[1], "01-01", sep = "-")
  
  plot_long <- df$PlotId
  plot_short <- substr(df$PlotId, 4, 8)
  station_long <- df$StationId
  station_short <- substr(df$StationId, 3, 6)  
  
  beData <- new("be.data",  
                Datetime = as.POSIXct(df$Datetime, tz = "UTC"),
                Date = list(Unique = paste(unique(year), unique(month), 
                                           sep = ""),
                            Year = year,
                            Month = month,
                            Day = day),
                Time = list(Hour = hour,
                            Minute = minute),
                Origin = origin,
                Timezone = unique(na.exclude(df$Timezone)),
                Aggregationtime = unique(na.exclude(df$Aggregationtime)),
                PlotId = list(Unique = unique(na.exclude(plot_short)),
                              Longname = plot_long,
                              Shortname = plot_short),
                EpPlotId = df$EpPlotId,
                StationId = list(Unique = unique(na.exclude(station_short)),
                                 Longname = station_long,
                                 Shortname = station_short),
                Processlevel = unique(na.exclude(df$Processlevel)),
                Qualityflag = as.character(df$Qualityflag),
                CycleCounter = df$CycleCounter,
                Parameter = as.list(df[10:length(df)])
                )
  
  return(beData)
}

# 
# input_filepath <- "c:/tappelhans/uni/marburg/kili/testing/be_data/be_000HEG01_00CEMU_200901010000_200901312330_mez_ca05_cti30_0005.dat"
# #input_filepath <- "c:/tappelhans/uni/marburg/kili/testing/kili_data/ki_0000cof3_000pu1_201104010000_201104302355_eat_ca05_cti05_0005.dat"
#input_filepath <- "c:/tappelhans/uni/marburg/kili/testing/be_data/be_000SEG01_00CEMU_200904010000_200904302330_mez_ca05_cti30_0005.dat"
 
#test <- as.be.data(input_filepath)
#str(test)

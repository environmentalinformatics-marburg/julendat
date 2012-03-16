
setClass("kili.data",
         representation(
           Datetime = "POSIXct",
           Date = "list",
           Time = "list",
           Origin = "character",
           Timezone = "character",
           Aggregationtime = "character",
           PlotId = "list",
           StationId = "list",
           Processlevel = "character",
           Qualityflag = "character",
           Parameter = "list"
           )
         )

as.kili.data <- function(input_filepath) {
  
  df <- read.table(input_filepath, header = T, sep = ",", fill = T,
                   stringsAsFactors = F, na.strings = "")
  
  year <- substr(df$Datetime, 1, 4)
  month <- substr(df$Datetime, 6, 7)
  day <- substr(df$Datetime, 9,10)
  hour <- substr(df$Datetime, 12, 13)
  minute <- substr(df$Datetime, 15, 16)
  origin <- paste(year[1], "01-01", sep = "-")
  
  plot_long <- df$PlotId
  plot_short <- substr(df$PlotId, 5, 8)
  station_long <- df$StationId
  station_short <- substr(df$StationId, 4, 7)  
  
  kiliData <- new("kili.data",  
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
                  StationId = list(Unique = unique(na.exclude(station_short)),
                                   Longname = station_long,
                                   Shortname = station_short),
                  Processlevel = unique(na.exclude(df$Processlevel)),
                  Qualityflag = as.character(df$Qualityflag),
                  Parameter = as.list(df[9:length(df)])
                  )
  
  return(kiliData)
}

# 
# input_filepath <- "c:/tappelhans/uni/marburg/kili/testing/kili_data/ki_0000cof3_000wxt_201109010000_201109302355_eat_ca05_cti05_0005.dat"
# #input_filepath <- "c:/tappelhans/uni/marburg/kili/testing/kili_data/ki_0000cof3_000pu1_201104010000_201104302355_eat_ca05_cti05_0005.dat"
# #input_filepath <- "c:/tappelhans/uni/marburg/kili/testing/kili_data/ki_0000foc1_000rug_201110010000_201110312355_eat_ca05_cti05_0005.dat"
# 
# test <- as.kili.data(input_filepath)
# str(test)

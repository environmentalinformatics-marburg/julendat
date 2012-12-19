
setClass("ki.data",
         representation(
           Datetime = "POSIXct",
           Date = "list",
           Time = "list",
           AggregationLevels = "list",
           Origin = "character",
           Season = "character",
           Timezone = "character",
           Aggregationtime = "character",
           PlotId = "list",
           EpPlotId = "character",
           StationId = "list",
           Processlevel = "character",
           Qualityflag = "character",
           Valid = "list",
           Parameter = "list",
           PrmHisto = "list"
           )
         )

as.ki.data <- function(input_filepath) {
  
  stopifnot(require(ggplot2, quietly = TRUE))
  stopifnot(require(reshape, quietly = TRUE))
  
  df <- read.table(input_filepath, header = T, sep = ",", fill = T,
                   stringsAsFactors = F, na.strings = "")
  year <- substr(df$Datetime, 1, 4)
  len <- length(year)
  origin <- paste(year[1], "01-01", sep = "-")
  
  if (len < 1000) df$Datetime <- as.POSIXct(strptime(df$Datetime, 
                                                     format = "%Y%m%d%H"), 
                                            origin = origin)

  month <- try(substr(df$Datetime, 6, 7))
  day <- try(substr(df$Datetime, 9,10))
  hour <- try(substr(df$Datetime, 12, 13))
  minute <- try(substr(df$Datetime, 15, 16))
  
  agghour <- try(paste(year, month, day, hour, sep = ""))
  aggday <- try(paste(year, month, day, sep = ""))
  aggmonth <- try(paste(year, month, sep = ""))
#   aggqh <- as.numeric(minute)
#   aggqh <- aggqh %/% 15
#   aggqh <- factor(aggqh, labels = c("00", "15", "30", "45"))
#   aggqh <- paste(year, month, day, hour, aggqh, sep = "")
  
  agg3h <- as.numeric(hour)
  agg3h <- agg3h %/% 3
  labs3hupper <- as.character(seq(12, 21, 3))
  labs3hlower <- paste("0", as.character(seq(0, 9 , 3)), sep = "")
  labs3h <- c(labs3hlower, labs3hupper)
  agg3h <- factor(agg3h, labels = labs3h)
  agg3h <- paste(year, month, day, agg3h, sep = "")
  
  agg6h <- as.numeric(hour)
  agg6h <- agg6h %/% 6
  labs6hupper <- as.character(seq(12, 18, 6))
  labs6hlower <- paste("0", as.character(seq(0, 9, 6)), sep = "")
  labs6h <- c(labs6hlower, labs6hupper)
  agg6h <- factor(agg6h, labels = labs6h)
  agg6h <- paste(year, month, day, agg6h, sep = "")

  switch(unique(month),
         "12" = season <- "DJF",
         "01" = season <- "DJF",
         "02" = season <- "DJF",
         "03" = season <- "MAM",
         "04" = season <- "MAM",
         "05" = season <- "MAM",
         "06" = season <- "JJA",
         "07" = season <- "JJA",
         "08" = season <- "JJA",
         "09" = season <- "SON",
         "10" = season <- "SON",
         "11" = season <- "SON")
         
  season <- rep(season, length(month))
  
  plot <- df$PlotId
  #plot_short <- substr(df$PlotId, 5, 8)
  station_long <- df$StationId
  station_short <- substr(df$StationId, 4, 7)  
  
  df2 <- data.frame(df[9:length(df)])
  ok <- complete.cases(df)
  nok <- which(!complete.cases(df))
  validn <- sum(ok)
  nna <- NROW(df) - validn
#  print(nna)
  df2 <- melt(df2)

  graph <- ggplot(df2, aes(x = value, y = ..scaled..))
  graph <- graph + geom_density(fill = "darkblue", alpha = 0.5) +
    facet_wrap(~ variable, scales = "free")
  
  kiData <- new("ki.data",  
                Datetime = as.POSIXct(df$Datetime, tz = "UTC"),
                Date = list(Unique = paste(unique(year), unique(month), 
                                           sep = ""),
                            Year = year,
                            Month = month,
                            Day = day),
                Time = list(Hour = hour,
                            Minute = minute),
                AggregationLevels = list(#AggQh = aggqh,
                                         Agg1h = agghour,
                                         Agg3h = agg3h,
                                         Agg6h = agg6h,
                                         AggDay = aggday,
                                         AggMonth = aggmonth,
                                         AggYear = year),
                Origin = origin,
                Season = season,
                Timezone = unique(na.exclude(df$Timezone)),
                Aggregationtime = unique(na.exclude(df$Aggregationtime)),
                PlotId = list(Unique = unique(na.exclude(plot)),
                              #Longname = plot_long,
                              Shortname = plot),
                EpPlotId = df$EpPlotId,
                StationId = list(Unique = unique(na.exclude(station_short)),
                                 Longname = station_long,
                                 Shortname = station_short),
                Processlevel = unique(na.exclude(df$Processlevel)),
                Qualityflag = as.character(df$Qualityflag),
                Valid = list(N = validn, NAIndex = nok),
                Parameter = as.list(df[9:length(df)]),
                PrmHisto = list(graph)
                )
  
  return(kiData)
}

# 
# input_filepath <- "/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/ca05_cti05_0050/ki_0000cof1_000rug_201102010000_201102282355_eat_ca05_cti05_0050.dat"
# input_filepath <- "c:/tappelhans/uni/marburg/kili/testing/kili_data/ki_0000cof3_000pu1_201104010000_201104302355_eat_ca05_cti05_0005.dat"
# input_filepath <- "c:/tappelhans/uni/marburg/kili/testing/kili_data/ki_0000foc3_000rug_201110010000_201110312355_eat_ca05_cti05_0005.dat"
# 
# test <- as.ki.data(input_filepath)
# str(test)
# test@PrmHisto

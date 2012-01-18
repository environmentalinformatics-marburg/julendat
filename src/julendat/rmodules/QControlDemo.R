qcontroldemo <- function(inpath, outpath, para, maxlimit, digit) {
  
  ## input/definition section
  df <- read.table(inpath, header = T, sep = ",", fill = T,
                   stringsAsFactors = F)
  
  qual <- rep("0000000000000000", length(df[,1]))
  qualleft <- substr(qual, 1, (digit - 1))
  qualact <- substr(qual, digit, (digit + 1))
  qualright <- substr(qual, (digit + 2), length(qual))
  
  ## test section
  qualact <- ifelse(df[para] > maxlimit, "r2", "r1")

  qual <- paste(qualleft, qualact, qualright, sep = "")
  
  ## output section
  df["Qualityflag"] <- qual
  write.table(df, outpath, col.names = T, row.names = F, sep = ",")

}

## EXAMPLE
#inpath <- "c:/tappelhans/uni/marburg/lehre/2011/ws/r_course/projektarbeit/ki_0000foc3_000rug_201110010000_201110312355_eat_ca05_cti05_0005.dat"
#outpath <- "c:/tappelhans/uni/marburg/lehre/2011/ws/r_course/projektarbeit/ki_0000foc3_000rug_201110010000_201110312355_eat_ca05_cti05_0010.dat"
#para <- "Ta_200"
#maxlimit <- 15
#digit <- 3
#qcontroldemo(inpath, outpath, para, maxlimit, digit)

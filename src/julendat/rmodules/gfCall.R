# Load function 'gfWrite'
source("gfWrite.R")

# Execute gfWrite
gfWrite(files.dep = list.files("/home/dogbert/software/testing/julendat/processing/plots/ki", pattern = glob2rx("*201201010000*ca05_cti05_0050.dat"), recursive = TRUE, full.names = TRUE)[1],
        files.indep = c(list.files("/home/dogbert/software/testing/julendat/processing/plots/ki", pattern = glob2rx("*201201010000*ca05_cti05_0050.dat"), recursive = TRUE, full.names = TRUE)[-1]),
        filepath.output = "/home/dogbert/software/testing/julendat/processing/plots/ki/0000cof1/ca05_cti05_0150/imputation_test.dat",
        filepath.coords = "/home/dogbert/software/development/julendat/src/julendat/scripts/stations_ki/stations_master_20121103.csv",
        quality.levels = c(12, 21),
        na.limit = 0.1,
        n.plot = 10,
        prm.dep = c("Ta_200", "rH_200"), 
        prm.indep = c(NA, "Ta_200"))

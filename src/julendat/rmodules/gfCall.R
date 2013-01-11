# Load function 'gfWrite'
source("gfWrite.R")

# Execute gfWrite
gfWrite(files.dep = "/media/permanent/r_mulreg/data/year/complete/ki_0000cof5_000rug_201201010000_201212310000_eat_qc25_fah01_0290.dat",
        files.indep = c("/media/permanent/r_mulreg/data/year/complete/ki_0000gra5_000rug_201201010000_201212310000_eat_qc25_fah01_0290.dat",
                        "/media/permanent/r_mulreg/data/year/complete/ki_0000flm1_000rug_201201010000_201212310000_eat_qc25_fah01_0290.dat", 
                        "/media/permanent/r_mulreg/data/year/complete/ki_0000sav3_000rug_201201010000_201212310000_eat_qc25_fah01_0290.dat", 
                        "/media/permanent/r_mulreg/data/year/complete/ki_0000sav4_000rug_201201010000_201212310000_eat_qc25_fah01_0290.dat", 
                        "/media/permanent/r_mulreg/data/year/complete/ki_0000sav5_000rug_201201010000_201212310000_eat_qc25_fah01_0290.dat"),
        filepath.output = "/home/dogbert/software/testing/julendat/processing/plots/ki/0000cof1/ca05_cti05_0150/imputation_test_3.dat",
        filepath.coords = "/home/dogbert/software/development/julendat/src/julendat/rmodules/station_master.csv",
        quality.levels = c(12, 22),
        gap.limit = 360, 
        na.limit = 0.3,
        time.window = 480,
        n.plot = 10,
        prm.dep = c("Ta_200", "rH_200"), 
        prm.indep = c(NA, "Ta_200"), 
        family = gaussian, 
        plevel = sprintf("%04.0f", 100))

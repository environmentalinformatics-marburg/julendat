source("run_QCRange.R")
run_QCRange(
  input_filepath=c("/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/ca05_cti05_0050/ki_0000cof1_000rug_201102010000_201102282355_eat_ca05_cti05_0050.dat"),
  output_filepath = "/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/ca05_cti05_0050/ki_0000cof1_000rug_201102010000_201102282355_eat_ca05_cti05_0050_test.dat",
  parameter=c("Ta_200","rH_200"),
  thv_min=c(-40.0, 0.0),
  thv_max=c(40.0, 100.0),
  qfpos=c(2,5),
  qfvalues=c(1,2),
  flag_col = "Qualityflag")
source("run_QCSteps.R")
run_QCSteps (
  input_filepath=c("/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/ca05_cti05_0050/ki_0000cof1_000rug_201102010000_201102282355_eat_ca05_cti05_0050.dat"),
  output_filepath = "/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/ca05_cti05_0050/ki_0000cof1_000rug_201102010000_201102282355_eat_ca05_cti05_0050_test.dat",
  parameter=c("Ta_200", "rH_200"),
  percentil =c(5),
  qfpos=c(2,5),
  qfvalues=c(10,20),
  limit_output = NULL,# can also be a destination folder to which a table with the calculated limits is saved
  pos_date = 1,
  flag_col = "Qualityflag",
  lmts=data.frame(min=c(0.001, 0), max=c(0.1, 30)),  # optional. if used - needs to be a dataframe
  plevel = 156)
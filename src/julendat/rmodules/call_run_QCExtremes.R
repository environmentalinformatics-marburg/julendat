source("run_QCExtremes.R")
run_QCExtremes(
  input_filepath=c("/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/ca05_cti05_0050/ki_0000cof1_000rug_201102010000_201102282355_eat_ca05_cti05_0050.dat"),
  output_filepath = "/home/ede/software/testing/julendat/processing/plots/ki/0000cof1/test.dat",
parameter=c("Ta_200", "rH_200"),
percentil =c(5),
qfpos=c(2,5),
qfvalues=c(1,2)
)
# split_for_benchmarks
Code to run and evaluate algorithms that split sequence families into training and test sets that are sufficiently different.

instructions.txt describes how to generate the data and figures in the paper [LINK COMING SOON]. 

The splitting algorithms analyzed are implemented in this forked version of HMMER's profmark: https://github.com/spetti/hmmer/tree/master/profmark. To run the algorithms, it is also necesary to to have this forked version of EASEL: https://github.com/spetti/easel.

The directory benchmarking_code contains code that calls splitting algorithms and homology search methods (which create the data) and code that produces the figures. 

The directory benchmakring_data contains the data we generated and used in the paper. 


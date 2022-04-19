# split_for_benchmarks
Code to run and evaluate algorithms that split sequence families into training and test sets that are sufficiently different.

instructions.txt describes how to generate the data and figures in the paper: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009492. 

The splitting algorithms analyzed are implemented in the development branch of HMMER's profmark: https://github.com/EddyRivasLab/hmmer/tree/develop. To run the algorithms, the following version of EASEL is needed: https://github.com/EddyRivasLab/easel/tree/develop.

The directory benchmarking_code contains code that calls splitting algorithms and homology search methods (which create the data) and code that produces the figures. 

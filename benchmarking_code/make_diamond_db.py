import subprocess
import os
from subprocess import call

split_directory='/n/home01/spetti/spetti_space/benchmarks/splits/'

load_module_command="module load diamond/0.9.5-fasrc01"

algs=['blue1','cobalt1','cluster','random70', 'blue40','cobalt40']


for alg in algs:
    batchfileName = "/tmp/mkddb_"+alg
    batchfile = open(batchfileName, "w")
    batchfile.write("#!/bin/bash \n")
    batchfile.write("#SBATCH -c 1 \n")
    batchfile.write("#SBATCH -N 1 \n")
    batchfile.write("#SBATCH -t 0:10:00 \n")
    batchfile.write("#SBATCH -p eddy \n")
    batchfile.write("#SBATCH --mem=4000 \n")
   # batchfile.write("#SBATCH --nice=1000 \n")
    batchfile.write("#SBATCH -o /n/home01/spetti/benchmarking/output/%j.out \n")
    batchfile.write("#SBATCH -e /n/home01/spetti/benchmarking/output/%j.err \n")
    #batchfile.write("#SBATCH --mail-type=END \n")

    batchfile.write(load_module_command)
    batchfile.write('\n')
    batchfile.write("diamond makedb --in "+split_directory+alg+".fa --db "+split_directory+alg+".fa")
    batchfile.write('\n')

    batchfile.close()

    sbatchstring =["sbatch", batchfileName]
    call(sbatchstring)
    #print(commandstring)
    os.remove(batchfileName)

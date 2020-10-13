#! /usr/bin/python
import subprocess
import os
from subprocess import call

#run homology search methods on synthetic sequences for benchmarking

#where to find positive and negative seqs
split_directory='/n/home01/spetti/spetti_space/benchmarks/splits/'

#where to output results
methods_directory='/n/home01/spetti/spetti_space/benchmarks/'

hmmer_path="/n/home01/spetti/hmmer"
profmark_path= hmmer_path+'/profmark/'


algs=['blue1','cobalt1','cluster','random70','cobalt40', 'blue40']
methods=['psiblast','blast','hmmsearch', 'diamond', 'diamond-sen']

pm_command={}
pm_command['psiblast']='x-psiblast+'
pm_command['blast']='x-fps-ncbiblast+'
pm_command['hmmsearch']='x-hmmsearch'
pm_command['diamond']='x-fps-diamond'
pm_command['diamond-sen']='x-fps-diamond-sen'



source={}
source['psiblast']='/n/sw/eb/apps/centos7/MPI/GCC/8.2.0-2.31.1/OpenMPI/3.1.3/BLAST+/2.9.0 '
source['blast']="/n/sw/eb/apps/centos7/MPI/GCC/8.2.0-2.31.1/OpenMPI/3.1.3/BLAST+/2.9.0 "
source['hmmsearch']="/n/home01/spetti/hmmer "
source['diamond']="/n/helmod/apps/centos7/Core/diamond/0.9.5-fasrc01 "
source['diamond-sen']="/n/helmod/apps/centos7/Core/diamond/0.9.5-fasrc01 "




for method in methods:
    for alg in algs:
        batchfileName = "/tmp/"+method+"_"+alg
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

        batchfile.write('mkdir -p ' + methods_directory+method)
        batchfile.write("\n")

        commandstring=profmark_path+"pmark-master.pl "+ source[method] + hmmer_path+ " "+ methods_directory+ method +"/"+alg+" 100 "+ split_directory+alg+ " " +profmark_path+pm_command[method]
        batchfile.write(commandstring)
        batchfile.write("\n")
        batchfile.close()

        sbatchstring =["sbatch", batchfileName]
        call(sbatchstring)
        print(commandstring)
        os.remove(batchfileName)


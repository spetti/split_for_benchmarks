#! /usr/bin/python
import os
from subprocess import call

# split pfam-seed families into training and test sets and synthesize +/- seqs
# output will be used for benchmarking homology search algs

algs=['blue1','cobalt1', 'random70', 'cluster', 'blue40','cobalt40']
t1="0.25"
t2="0.50"

create_profmark="/n/home01/spetti/hmmer/profmark/create-profmark "
out_location="/n/home01/spetti/spetti_space/benchmarks/splits/"
if not os.path.exists(out_location):
    os.makedirs(out_location)

db=" /n/eddyfs01/data/dbs/pfam-33.1/Pfam-A.seed"
uniprot=" /n/eddyfs01/data/dbs/uniprot-0219/uniprot_sprot.fasta" 

command={}
command['blue1']='--blue'
command['cobalt1']='--cobalt'
command['blue10']='--blue -R 10'
command['cobalt10']='--cobalt -R 10'
command['random70']='--random --rp 0.70'
command['cluster']='--cluster'
command['blue40']='--blue -R 40'
command['cobalt40']='--cobalt -R 40'
flags=' -1 '+t1+' -2 ' +t2+' --mintrain 10 --mintest 2 --single --maxtest 10 --pid '

for alg in algs:
    batchfileName = "/tmp/" +alg
    batchfile = open(batchfileName, "w")
    batchfile.write("#!/bin/bash \n")
    batchfile.write("#SBATCH -c 1 \n")
    batchfile.write("#SBATCH -N 1 \n")
    batchfile.write("#SBATCH -t 5:00:00 \n")
    batchfile.write("#SBATCH -p eddy \n")
    batchfile.write("#SBATCH --mem=4000 \n")
   # batchfile.write("#SBATCH --nice=1000 \n")
    batchfile.write("#SBATCH -o /n/home01/spetti/output/%j.out \n")
    batchfile.write("#SBATCH -e /n/home01/spetti/output/%j.err \n")
    batchfile.write("#SBATCH --mail-type=END \n")

    commandstring=create_profmark+command[alg]+flags+out_location+alg+db+uniprot
    batchfile.write(commandstring)
    batchfile.write("\n")
    batchfile.close()
    sbatchstring =["sbatch", batchfileName]
    call(sbatchstring)
    print(commandstring)
    os.remove(batchfileName)






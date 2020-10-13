#! /usr/bin/python
import os
import glob
from subprocess import call
import time


algs=['blue','cobalt', 'cluster', 'random70']
out_location="/n/home01/spetti/spetti_space/pass_rate_benchmark/splits"

t1="0.25"
t2="0.50"

command={}
command['blue']='--blue -T 40'
command['cobalt']='--cobalt -T 40'
command['random70']='--random --rp 0.70'
command['cluster']='--cluster'


sf='full'
dbs=["/n/eddyfs01/data/dbs/pfam-33.1/Pfam-A.seed",
     '/n/home01/spetti/spetti_space/pass_rate_benchmark/full_under_5000.msa',
     '/n/home01/spetti/spetti_space/pass_rate_benchmark/full_5000_10000.msa']


info={}
info["/n/eddyfs01/data/dbs/pfam-33.1/Pfam-A.seed"]='seed'
info['/n/home01/spetti/spetti_space/pass_rate_benchmark/full_under_5000.msa']="full_u_5000"
info['/n/home01/spetti/spetti_space/pass_rate_benchmark/full_5000_10000.msa']="full_5000_10000"

uniprot=" /n/eddyfs01/data/dbs/uniprot-0219/uniprot_sprot.fasta" 

if True:
    for db in dbs:
        for alg in algs:
            if alg=='blue' and db!="/n/eddyfs01/data/dbs/pfam-33.1/Pfam-A.seed":
                continue
            print(info[db], alg)
            sf=info[db][0:4]

            batchfileName = "/tmp/" +alg+ "_"+sf
            batchfile = open(batchfileName, "w")
            batchfile.write("#!/bin/bash \n")
            batchfile.write("#SBATCH -c 2 \n")
            batchfile.write("#SBATCH -N 1 \n")
            batchfile.write("#SBATCH -t 24:00:00 \n")
            batchfile.write("#SBATCH -p eddy \n")
            batchfile.write("#SBATCH --mem=8000 \n")
           # batchfile.write("#SBATCH --nice=1000 \n")
            batchfile.write("#SBATCH -o /n/home01/spetti/output/%j.out \n")
            batchfile.write("#SBATCH -e /n/home01/spetti/output/%j.err \n")
            batchfile.write("#SBATCH --mail-type=END \n")
            name=alg+'_'+info[db]
            if sf=='seed':
                commandstring="/n/home01/spetti/hmmer/profmark/create-profmark "+command[alg]+' -1 '+t1+' -2 ' +t2+' --mintrain 10 --mintest 2 --dev --conn '+out_location+"/"+name+' '+db+uniprot
            if sf=='full':
                commandstring="/n/home01/spetti/hmmer/profmark/create-profmark "+command[alg]+' -1 '+t1+' -2 ' +t2+' --mintrain 400 --mintest 20 --dev --conn '+out_location+"/"+name+' '+db+uniprot

            batchfile.write(commandstring)
            batchfile.write("\n")
            batchfile.close()
            sbatchstring =["sbatch", batchfileName]
            call(sbatchstring)
            #print(commandstring)
            os.remove(batchfileName)


alg='blue'
base='/n/home01/spetti/spetti_space/pass_rate_benchmark/full_under_5000'
for i in range(1,9):
    batchfileName = "/tmp/" +alg+ "_"+str(i)
    batchfile = open(batchfileName, "w")
    batchfile.write("#!/bin/bash \n")
    batchfile.write("#SBATCH -c 2 \n")
    batchfile.write("#SBATCH -N 1 \n")
    batchfile.write("#SBATCH -t 24:00:00 \n")
    batchfile.write("#SBATCH -p eddy \n")
    batchfile.write("#SBATCH --mem=8000 \n")
   # batchfile.write("#SBATCH --nice=1000 \n")
    batchfile.write("#SBATCH -o /n/home01/spetti/output/%j.out \n")
    batchfile.write("#SBATCH -e /n/home01/spetti/output/%j.err \n")
    #batchfile.write("#SBATCH --mail-type=END \n")
    name=alg+'_'+"full_u_5000"+"_"+str(i)
    db=base+"_"+str(i)+".msa"
    commandstring="/n/home01/spetti/hmmer/profmark/create-profmark "+command[alg]+' -1 '+t1+' -2 ' +t2+' --mintrain 400 --mintest 20 --dev --conn '+out_location+"/"+name+' '+db+uniprot

    batchfile.write(commandstring)
    batchfile.write("\n")
    batchfile.close()
    sbatchstring =["sbatch", batchfileName]
    call(sbatchstring)
    #print(commandstring)
    os.remove(batchfileName)



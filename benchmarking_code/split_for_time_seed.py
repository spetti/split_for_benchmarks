#! /usr/bin/python
import os
import glob
from subprocess import call
import subprocess
import time


algs=['blue','cobalt', 'random70', 'cluster']

sto_directory="/n/home01/spetti/spetti_space/sto_files_33/"

for i in range(100,131):
    if i%2==1:
        time.sleep(350)

    
    out_directory="/n/home01/spetti/spetti_space/time_benchmark"+str(i)+"E/"

    subprocess.run(['mkdir','-p',out_directory])

    command={}
    command['blue']='--blue'
    command['cobalt']='--cobalt'
    command['random70']='--random --rp 0.70'
    command['cluster']='--cluster'

    num_per_batch=10000

    for alg in algs:
        subprocess.run(['mkdir','-p',out_directory+alg])



    finished={}
    for alg in algs:
        finished[alg]={}
        for filename in os.listdir(sto_directory):
            if filename.endswith("seed.sto"):
                name=filename[2:12]
                finished[alg][name]=0

        for filename in os.listdir(out_directory+alg):
                if filename.endswith(".tbl") or filename.endswith(".time"):
                    finished[alg][filename[0:10]]+=1

    for alg in algs:
        batch_num=1
        counter=0
        for filename in os.listdir(sto_directory):
            if filename.endswith("seed.sto"):

                name=filename[2:12]
                od=out_directory+alg
                db=sto_directory+filename
                if finished[alg][name]!=2:

                    if counter==0:
                        batchfileName = "/tmp/" +alg
                        batchfile = open(batchfileName, "w")
                        batchfile.write("#!/bin/bash \n")
                        batchfile.write("#SBATCH -c 2 \n")
                        batchfile.write("#SBATCH -N 1 \n")
                        batchfile.write("#SBATCH --exclusive \n")
                        batchfile.write("#SBATCH -t 10:00 \n")
                        batchfile.write("#SBATCH -p eddy \n")
                        batchfile.write("#SBATCH --mem=8000 \n")
                        #batchfile.write("#SBATCH --nice=1000 \n")
                        batchfile.write("#SBATCH -o "+out_directory+alg+"_"+str(batch_num)+".names \n")
                        batchfile.write("#SBATCH -e "+out_directory+alg+"_"+str(batch_num)+".times \n")


                   
                    commandstring="time /n/home01/spetti/hmmer/profmark/create-profmark "+command[alg]+' -1 0.25 -2 0.50 --dev --noavg '+od+"/"+name+' '+db+" /n/eddyfs01/data/dbs/uniprot-0219/uniprot_sprot.fasta" 

                    batchfile.write(commandstring)
                    batchfile.write("\n")
                    
                    batchfile.write("head -2 /n/home01/spetti/spetti_space/sto_files_33/"+filename+" | tail -1 | awk '{ print $3 }'  \n")


                    counter+=1
                    if counter>=num_per_batch:
                        batch_num+=1
                        counter=0
                        batchfile.close()
                        sbatchstring =["sbatch", batchfileName]
                        call(sbatchstring)
                        os.remove(batchfileName)

        if counter !=0:
            batchfile.close()
            sbatchstring =["sbatch", batchfileName]
            call(sbatchstring)
            #print(commandstring)
            os.remove(batchfileName)


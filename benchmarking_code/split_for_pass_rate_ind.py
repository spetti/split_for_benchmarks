#! /usr/bin/python
import os
import glob
from subprocess import call
import time


algs=['blue','cobalt', 'cluster', 'random70']
#algs=['random70']
#algs=['cluster']
#algs=['cobalt', 'cluster']
#algs=['blue']
out_location="/n/home01/spetti/spetti_space/pass_rate_benchmark/splits"
uniprot=" /n/eddyfs01/data/dbs/uniprot-0219/uniprot_sprot.fasta" 

t1="0.25"
t2="0.50"

command={}
command['blue']='--blue -T 40'
command['cobalt']='--cobalt -T 40'
command['random70']='--random --rp 0.70'
command['cluster']='--cluster'

nbatch=5
nbphour=80
counter=0
bn=0
ns=0
nsub=0
done={}
for alg in algs:
    done[alg]=[]
for filename in os.listdir('/n/home01/spetti/spetti_space/pass_rate_benchmark/splits/'):
    for alg in algs:
        if filename.startswith(alg):
            done[alg].append(filename)
#print(done) 

blue_med=True
if blue_med:
    for filename in os.listdir('/n/home01/spetti/spetti_space/pass_rate_benchmark/med_full_msa/'):
        alg='blue'
        name=alg+'_'+filename
        if name+".tbl" in done[alg]:
            ns+=1
            continue
        if counter==0:
            batchfileName = "/tmp/" +alg+ "_"+filename
            batchfile = open(batchfileName, "w")
            batchfile.write("#!/bin/bash \n")
            batchfile.write("#SBATCH -c 2 \n")
            batchfile.write("#SBATCH -N 1 \n")
            batchfile.write("#SBATCH -t 24:00:00 \n")
            batchfile.write("#SBATCH -p eddy \n")
            batchfile.write("#SBATCH --mem=8000 \n")
            batchfile.write("#SBATCH --nice=1000 \n")
            batchfile.write("#SBATCH -o /n/home01/spetti/output/%j.out \n")
            batchfile.write("#SBATCH -e /n/home01/spetti/output/%j.err \n")
            #batchfile.write("#SBATCH --mail-type=END \n")

        db='/n/home01/spetti/spetti_space/pass_rate_benchmark/med_full_msa/'+filename

        commandstring="/n/home01/spetti/hmmer/profmark/create-profmark "+command[alg]+' -1 '+t1+' -2 ' +t2+' --mintrain 400 --mintest 20 --dev --conn '+out_location+"/"+name+' '+db+uniprot
        #print(commandstring)
        batchfile.write(commandstring)
        batchfile.write("\n")

        counter +=1
        nsub+=1
        if counter==nbatch:
            bn+=1
            batchfile.close()
            sbatchstring =["sbatch", batchfileName]
            call(sbatchstring)
            #print("closed file!!!!!!!!!!!!!!!!!!")
            os.remove(batchfileName)
            counter=0

    if counter>0:
        batchfile.close()
        sbatchstring =["sbatch", batchfileName]
        call(sbatchstring)
        os.remove(batchfileName)

    print("submitted: "+str(nsub))
    print("skipped: "+str(ns))
    print("total: "+ str(ns+nsub))
    exit()




for filename in os.listdir('/n/home01/spetti/spetti_space/pass_rate_benchmark/big_full_msa/'):
    for alg in algs:
        name=alg+'_'+filename
        if name+".tbl" in done[alg]:
            ns+=1
            continue
        if counter==0:
            batchfileName = "/tmp/" +alg+ "_"+filename
            batchfile = open(batchfileName, "w")
            batchfile.write("#!/bin/bash \n")
            batchfile.write("#SBATCH -c 3 \n")
            batchfile.write("#SBATCH -N 1 \n")
            batchfile.write("#SBATCH -t 24:00:00 \n")
            batchfile.write("#SBATCH -p eddy \n")
            batchfile.write("#SBATCH --mem=12000 \n")
           # batchfile.write("#SBATCH --nice=1000 \n")
            batchfile.write("#SBATCH -o /n/home01/spetti/output/%j.out \n")
            batchfile.write("#SBATCH -e /n/home01/spetti/output/%j.err \n")
            #batchfile.write("#SBATCH --mail-type=END \n")
        
        db='/n/home01/spetti/spetti_space/pass_rate_benchmark/big_full_msa/'+filename
        
        commandstring="/n/home01/spetti/hmmer/profmark/create-profmark "+command[alg]+' -1 '+t1+' -2 ' +t2+' --mintrain 400 --mintest 20 --dev --conn '+out_location+"/"+name+' '+db+uniprot
        #print(commandstring)
        batchfile.write(commandstring)
        batchfile.write("\n")
        
        counter +=1
        nsub+=1
        if counter==nbatch:
            bn+=1
            batchfile.close()
            sbatchstring =["sbatch", batchfileName]
            call(sbatchstring)
            #print("closed file")
            os.remove(batchfileName)
            counter=0
            if bn%nbphour==0:
                print("submitted: "+str(nsub))
                print("skipped: "+str(ns))
                print("total: "+ str(ns+nsub))
                print("sleeping")
                time.sleep(3600)
            
if counter>0:
    batchfile.close()
    sbatchstring =["sbatch", batchfileName]
    call(sbatchstring)
    os.remove(batchfileName)
    
print("submitted: "+str(nsub))
print("skipped: "+str(ns))
print("total: "+ str(ns+nsub))


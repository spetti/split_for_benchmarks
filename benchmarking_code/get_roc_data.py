#! /usr/bin/python
import subprocess
import os

# parse the output of pmark-master.pl and create XMGRACE xydydy file for plotting ROC curve

algs=['blue1','cobalt1','cluster','random70','blue40','cobalt40']
methods=['diamond', 'blast', 'hmmsearch','psiblast', 'diamond-sen']

split_directory='/n/home01/spetti/spetti_space/benchmarks/splits/'
methods_directory='/n/home01/spetti/spetti_space/benchmarks/'

hmmer_path="/n/home01/spetti/hmmer"
profmark_path=hmmer_path+"/profmark/"

for alg in algs:
    for method in methods:
        out_file_dir=methods_directory+method+"/"

        new_out = open(out_file_dir+alg+'.cat','w') 
        for file in os.listdir(out_file_dir+alg):
            if file[-3:]=='out':
                with open(out_file_dir+alg+'/'+file,"r") as fh:
                    for y in fh:
                        new_out.write(y)
        new_out.close()

        x=subprocess.run(['sort', '-g', out_file_dir+alg+'.cat', '-o', out_file_dir+alg+'.cat' ])
        if x.returncode!=0:
            raise ValueError ("didn't successfully sort .cat")

        #get grace file
        x=subprocess.run([profmark_path+'rocplot',split_directory+alg, out_file_dir+alg+'.cat' ], stdout=subprocess.PIPE)
        new_xy=open(out_file_dir+alg+".xy", 'w')
        new_xy.write(x.stdout.decode())
        new_xy.close()
        if x.returncode!=0:
            raise ValueError ("didn't successfully run get_roc_data")

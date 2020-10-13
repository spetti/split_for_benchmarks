#! /usr/bin/python
import subprocess
import os


#restrict benchmarks to data from families split succesfully by some subset of algorithms

algs=['blue1','cobalt1','cluster','random70']
l=len(algs)
methods=['hmmsearch']

split_directory='/n/home01/spetti/spetti_space/benchmarks/splits/'
methods_directory='/n/home01/spetti/spetti_space/benchmarks/'

hmmer_path="/n/home01/spetti/hmmer"
profmark_path= hmmer_path+'/profmark/'

for method in methods:

    out_file_dir=methods_directory+method+"/"
    output_dir=methods_directory+method+"/common_results_"+str(l)+'/'
    subprocess.run(['mkdir', '-p',output_dir])


    #dictionary fam-name: number of times successfully split
    occ={} 

    #read in all .tbl files 
    for alg in algs:
        with open(split_directory+alg+".tbl","r") as fh:
            for y in fh:
                y=y.split()
                if len(y)< 7:
                    print(y)
                fam_name=y[0]
                if fam_name in occ:
                    occ[fam_name]+=1
                else:
                    occ[fam_name]=1



    for alg in algs:

        #read all .tbl files, write to new tbl file if occ[fam_name] >=l
        new_tbl = open(output_dir+alg+'.tbl','w') 
        with open(split_directory+alg+".tbl","r") as fh:
            for y in fh:
                z=y
                y=y.split()
                fam_name=y[0]
                if occ[fam_name]>=l:
                    new_tbl.write(z)
        new_tbl.close()

       # read .pos files, write to new pos file if occ[fam_name]>=l
        new_pos= open(output_dir+alg+'.pos','w') 
        with open(split_directory+alg+".pos","r") as fh:
            for y in fh:
                z=y
                y=y.split('/')
                fam_name=y[0]
                if occ[fam_name]>=l:
                    new_pos.write(z)   
        new_pos.close()

        #copy over .neg file
        new_neg=output_dir+alg+'.neg'
        x=subprocess.run(["cp", split_directory+alg+".neg", new_neg])
        if x.returncode!=0:
            raise ValueError ("didn't successfully copy .neg")

      # transfer lines of .out files if correspond to a model of a fam with occ[fam_name]>=l
        new_out = open(output_dir+alg+'.out','w') 
        for file in os.listdir(out_file_dir+alg):
            if file[-3:]=='out':
                with open(out_file_dir+alg+'/'+file,"r") as fh:
                    for y in fh:
                        z=y
                        y=y.split()
                        fam_name=y[3]
                        s_fam_name=y[2].split('/')[0]
                        if occ[fam_name]>=l:
                            if s_fam_name[:5]=='decoy' or occ[s_fam_name]>=l:
                                new_out.write(z)
        new_out.close()

        x=subprocess.run(['sort', '-g', output_dir+alg+'.out', '-o', output_dir+alg+'.out' ])
        if x.returncode!=0:
            raise ValueError ("didn't successfully sort .out")

        #get grace file
        x=subprocess.run([profmark_path+'rocplot',output_dir+alg, output_dir+alg+'.out' ], stdout=subprocess.PIPE)
        new_xy=open(output_dir+alg+".xy", 'w')
        new_xy.write(x.stdout.decode())
        new_xy.close()
        if x.returncode!=0:
            raise ValueError ("didn't successfully run rocplot")

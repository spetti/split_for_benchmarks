#!/bin/bash
#SBATCH -J mpi_job
#SBATCH -o mpi.out
#SBATCH -e mpi.err
#SBATCH -p eddy_hmmer
#SBATCH -t 11-00:00
#SBATCH --mem-per-cpu=6800
#SBATCH -n 100
#SBATCH -N 5-7 


module load intel/2017c impi/2017.4.239 HH-suite/3.0-beta.3

cd /n/home01/spetti/spetti_space/benchmarks/hhblits_test

rm -f blue1_a3m_wo_ss.ff{data,index}*

srun -n 100 --mpi=pmi2 hhblits_mpi -i /n/home01/spetti/spetti_space/benchmarks/hhblits_test/blue1.fa -d /n/home01/spetti/spetti_space/hh_databases/UniRef30_2020_03 -oa3m blue1_a3m_wo_ss -n 2 -cpu 100 -v 2
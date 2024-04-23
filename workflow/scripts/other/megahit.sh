#!bin/bash/
###########################
#README
###########################
#This script runs MEGAHIT the same way it was ran in the tool evaluation,
# using the files from an already run project with the workflow.
#This script will only work if a project has already been ran using the workflow.

###########################
#ARGUMENTS
###########################
#$1: Project filepath

for d in $2/bbmap/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  
  #Creating the output directory
  mkdir -p $2/megahit/${id}
  
  #Running MEGAHIT
  megahit -1 $1/samples/${id}/rawdata/fw.fastq -2 $1/samples/${id}/rawdata/rv.fastq -o $2/megahit/${id} -t 16
done

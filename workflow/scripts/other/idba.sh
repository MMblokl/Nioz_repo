#!bin/bash
###########################
#README
###########################
#This script runs IDBA-UD the same way it was ran in the tool evaluation,
# using the files from an already run project with the workflow.
#This script will only work if a project has already been ran using the workflow.

###########################
#ARGUMENTS
###########################
#$1: Project filepath
###########################

#Exits if the path is not given.
if [[ $# -eq 0 ]] ; then
    echo 'No file name given. Exiting.'
    exit 0
fi

for d in $2/bbmap/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  
  #Creating the output directory
  mkdir -p $2/idba/${id}
  
  #Converting the fastq files into a fasta file
  fq2fa --merge $1/samples/${id}/rawdata/fw.fastq $1/samples/${id}/rawdata/rv.fastq $1/idba/${id}/fastareads.fa #merge the paired end fastq files into one fasta file

  #Running idba-ud
  idba_ud -r $1/idba/${id}/fastareads.fa -o $1/idba/${id}/ --mink 60 --maxk 60 --num_threads 16

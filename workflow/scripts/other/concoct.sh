#!bin/bash/
###########################
#README
###########################
#This script runs CONCOCT the same way it was ran during the tool evaluation.
#This script will only work if a project has already been ran using the workflow.

###########
#ARGUMENTS
###########
#$1: Project file path.
###########

#Exits if the path is not given.
if [[ $# -eq 0 ]] ; then
    echo 'No file name given. Exiting.'
    exit 0
fi


#Loop through all IDs in the bbmap dir. This can be done is any of the directories
# really but this is fine.
for d in $2/bbmap/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  
  #Creating the output directory
  mkdir $1/concoct/${id}/

  #Generate a coverage file and a composistion file to run concoct with.
  cut_up_fasta.py $1/bbmap/${id}/contigs_filtered.fasta -c 10000 -o 0 --merge_last -b $1/concoct/${id}/contigs_10k.bed > $1/concoct/${id}/contigs_10k.fa
  concoct_coverage_table.py $1/concoct/${id}/contigs_10k.bed $1/bbmap/*_sorted.bam > $1/concoct/${id}/coverage_table.tsv

  #Run concoct using the coverage and composistion file.
  concoct --composition_file $1/concoct/${id}/contigs_10k.fa --coverage_file $1/concoct/${id}/coverage_table.tsv -b $1/concoct/${id}/ --threads 16

  #Merge the binning output and extract the fasta bins as separate files.
  merge_cutup_clustering.py $1/concoct/${id}/clustering_gt1000.csv > $1/concoct/${id}/clustering_merged.csv
  mkdir -p $1/concoct/${id}/bins/
  extract_fasta_bins.py $1/bbmap/${id}/contigs_filtered.fasta $1/concoct/${id}/clustering_merged.csv --output_path $1/concoct/${id}/bins/
done
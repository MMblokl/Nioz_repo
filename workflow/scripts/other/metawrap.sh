###########################
#README
############################
#This script runs metaWRAP the same way it was ran in the tool evaluation,
# using the files from an already run project with the workflow.
#This script will only work if a project has already been ran using the workflow.


################################
#ARGUMENTS
################################
#$1: File containing every forward and reverse reads of all replicate samples.
# This refers to the file that would have to be created before running the workflow,
# the same one refered to in the README, containing the ID_1.fastq files for forward reads
# and ID_2.fastq files for reverse reads.
#$2: Filepath to the project folder.



#Loop through all sample IDs using the bbmap output folder from the project.
for d in $2/bbmap/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  mkdir -p $2/metawrap/${id}/work_files
  
  #This portion here copies all replicate alignment files into the metawrap working
  # dir "work_files".
  #The reason why the same directory is looped through again is simply to get the 
  # second set of ids in order to copy the correct files to the work_files dir.
  for d2 in $2/bbmap/*/
  do
    id2=$(echo $d2 | awk -F "/" '{print $(NF-1)}')
    cp $2/bbmap/${id}/${id2}_sorted.bam $2/metawrap/${id}/work_files/${id2}.bam
  done

  #Running the three binners.
  metaWRAP binning --metabat2 -a $2/bbmap/${id}/contigs_filtered.fasta -o $2/metawrap/${id}/ -t 16 -l 1000 $1/*_1.fastq $1/*_2.fastq
  metaWRAP binning --concoct -a $2/bbmap/${id}/contigs_filtered.fasta -o $2/metawrap/${id}/ -t 16 -l 1000 $1/*_1.fastq $1/*_2.fastq
  metaWRAP binning --maxbin2 -a $2/bbmap/${id}/contigs_filtered.fasta -o $2/metawrap/${id}/ -t 16 -l 1000 $1/*_1.fastq $1/*_2.fastq
  
  #Running the bin_refinement module.
  metaWRAP bin_refinement -o $2/metawrap/${id} -t 16 -m 40 -A $2/metawrap/${id}/concoct_bins -B $2/metawrap/${id}/metabat2_bins -C $2/metawrap/${id}/maxbin2_bins
done

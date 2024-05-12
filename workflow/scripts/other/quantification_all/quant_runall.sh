#!bin/bash/

#This script runs all scripts and the complete quantification script that contains all methods
# that were evaluated, including the final method.

#Like stated in the README, numpy is required for certain scripts.
#Make sure this package is accessible from the directory this script is run from.

################################
#ARGUMENTS:
#1: The filepath to the workflow project folder. This is to locate all the files needed to run 
# all quantification methods.

if [[ $# -eq 0 ]] ; then
    echo 'No file name given. Exiting.'
    exit 0
fi

for d in $1/filtered_bins/*/
do
  echo $d
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  mkdir -p $1/quant_all_methods/${id}/reads
  mkdir -p $1/quant_all_methods/${id}/depths
  mkdir -p $1/quant_all_methods/${id}/histo
  mkdir -p $1/quant_all_methods/${id}/salmon
  bash salmon_quant.sh ${id} $1/bbmap/${id}/contigs_filtered.fasta $1/samples/${id}/rawdata/fw.fastq $1/samples/${id}/rawdata/rv.fastq $1/quant_all_methods/${id}/salmon/
  Rscript collect_contig_depth.R $1/metabinner/${id}/mb2_master_depth.txt ${id} $1/quant_all_methods/${id}/contig_depth.txt
  python3 find_residuals.py ${id} $1/bbmap/${id}/contigs_filtered.fasta $1/filtered_bins/${id} $1/quant_all_methods/${id}/unbinned.txt
  python3 separate_binreads.py ${id} $1/bbmap/${id}/${id}_sorted.bam $1/filtered_bins/${id} $1/quant_all_methods/${id} $1/quant_all_methods/${id}/unbinned.txt $1/quant_all_methods/${id}/contig_depth.txt
  bash get_read_mapping.sh $1/bbmap/${id}/${id}_sorted.bam $1/quant_all_methods/${id}/readmapping.txt
  python3 kmercount_histo.py ${id} $1/quant_all_methods/${id}/histo $1/quant_all_methods/${id}/reads/
  Rscript calc_genomesize.R $1/quant_all_methods/${id}/histo $1/quant_all_methods/${id}/genomesizes.tab
  python3 quantification.py ${id} $1/filtered_bins/${id} $1/quant_all_methods/${id}/unbinned.txt $1/quant_all_methods/${id}/readmapping.txt $1/quant_all_methods/${id}/contig_depth.txt $1/quant_all_methods/${id}/salmon/quant.sf $1/quant_all_methods/${id}/genomesizes.tab $1/quant_all_methods/${id}/quant_table.txt

  #Optional script if you want to use true abundances.
  
  #This script cross references the true abundances and creates the deviation number files. This requires a file that has csv files containing true abundances.
  # How to make these files is explained in the local README.
  #python3 quant_check.py $1/quant_all_methods/${id}/quant_table.txt PATH_TO_ABUNDANCE_DIR/${id}.csv $1/gtdbtk/${id}/classification.tsv $1/quant_all_methods/${id}/

done

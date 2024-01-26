#!bin/bash/
echo "Usage concoct.sh contigs.fasta outputdir sorted_indexed_bamfile(s)"

#Contigs = $1
#outdir = $2
#Bamfiles = ${*:3}


#Create the output dir
mkdir -p outdir/

#Generate a coverage file and a composistion file to run concoct with.
cut_up_fasta.py $1 -c 10000 -o 0 --merge_last -b $2/contigs_10k.bed > $2/contigs_10k.fa
concoct_coverage_table.py $2/contigs_10k.bed ${*:3} > $2/coverage_table.tsv

#Run concoct using the coverage and composistion file.
concoct --composition_file $2/contigs_10k.fa --coverage_file $2/coverage_table.tsv -b ~$2 --threads 16

#Merge the binning output and extract the fasta bins as separate files.
merge_cutup_clustering.py $2/clustering_gt1000.csv > $2/clustering_merged.csv
mkdir $2/bins/
extract_fasta_bins.py $1 $2/clustering_merged.csv --output_path $2/bins/
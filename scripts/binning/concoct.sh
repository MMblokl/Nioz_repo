#!bin/bash/
source $HOME/.bashrc.conda3 concoct
#for d in ~/assembly/cami/*/
#do
#  echo $d
#  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
#  mkdir -p ~/binning/${id}/concoct/
#  cut_up_fasta.py ~/binning/${id}/mapping/${id}_1000bp.fasta -c 10000 -o 0 --merge_last -b ~/binning/${id}/concoct/contigs_10k.bed > ~/binning/${id}/concoct/contigs_10k.fa
#  concoct_coverage_table.py ~/binning/${id}/concoct/contigs_10k.bed ~/binning/${id}/mapping/sorted_*.bam > ~/binning/${id}/concoct/coverage_table.tsv
#  concoct --composition_file ~/binning/${id}/concoct/contigs_10k.fa --coverage_file ~/binning/${id}/concoct/coverage_table.tsv -b ~/binning/${id}/concoct --threads 16
#  merge_cutup_clustering.py ~/binning/${id}/concoct/clustering_gt1000.csv > ~/binning/${id}/concoct/clustering_merged.csv
#  mkdir ~/binning/${id}/concoct/bins/
#  extract_fasta_bins.py ~/binning/${id}/mapping/${id}_1000bp.fasta ~/binning/${id}/concoct/clustering_merged.csv --output_path ~/binning/${id}/concoct/bins/
#done

for d in ~/assembly/cellmock/*/
do
  echo $d
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  mkdir -p ~/binning/${id}/concoct/
  cut_up_fasta.py ~/binning/${id}/mapping/${id}_1000bp.fasta -c 10000 -o 0 --merge_last -b ~/binning/${id}/concoct/contigs_10k.bed > ~/binning/${id}/concoct/contigs_10k.fa
  concoct_coverage_table.py ~/binning/${id}/concoct/contigs_10k.bed ~/binning/${id}/mapping/sorted_*.bam > ~/binning/${id}/concoct/coverage_table.tsv
  concoct --composition_file ~/binning/${id}/concoct/contigs_10k.fa --coverage_file ~/binning/${id}/concoct/coverage_table.tsv -b ~/binning/${id}/concoct --threads 16
  merge_cutup_clustering.py ~/binning/${id}/concoct/clustering_gt1000.csv > ~/binning/${id}/concoct/clustering_merged.csv
  mkdir ~/binning/${id}/concoct/bins/
  extract_fasta_bins.py ~/binning/${id}/mapping/${id}_1000bp.fasta ~/binning/${id}/concoct/clustering_merged.csv --output_path ~/binning/${id}/concoct/bins/
done

#!bin/bash/

#CAMI dataset

source ~/.bashrc.conda3 MetaBinner
#for d in ~/assembly/cami/*/
#do
#  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
#  mkdir -p ${id}/metabinner/
#  ~/.conda/envs/MetaBinner/bin/scripts/jgi_summarize_bam_contig_depths --outputDepth ~/binning/${id}/metabinner/mb2_master_depth.txt --noIntraDepthVariance ~/binning/${id}/mapping/*.bam #This was taken from the script gen_kmer that came with metabinner. That script does an alignment with BWA, and since the fiels are already aligned with bbmap, this script is not needed in its entirety and only the final part.
#  cat ~/binning/${id}/metabinner/mb2_master_depth.txt | awk '{if ($2>'"1000"') print $0 }' | cut -f -1,4- > ~/binning/${id}/metabinner/coverage_profile.tsv
#  cd ~/.conda/envs/MetaBinner/bin/scripts/
#  python3 gen_kmer.py ~/binning/${id}/mapping/${id}_1000bp.fasta 1000 4
#  cd ~/binning/
#  mv ~/binning/${id}/mapping/*_f1000.csv ~/binning/${id}/metabinner/
#  cd ~/binning
#  run_metabinner.sh -a ~/binning/${id}/mapping/${id}_1000bp.fasta -o ~/binning/${id}/metabinner -d ~/binning/${id}/metabinner/coverage_profile.tsv -k ~/binning/${id}/metabinner/*_f1000.csv -p ~/.conda/envs/MetaBinner/bin -t 16
#done

#mock community files

for d in ~/assembly/cellmock/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  mkdir -p ${id}/metabinner
  ~/.conda/envs/MetaBinner/bin/scripts/jgi_summarize_bam_contig_depths --outputDepth ~/binning/${id}/metabinner/mb2_master_depth.txt --noIntraDepthVariance ~/binning/${id}/mapping/*.bam
  cat ~/binning/${id}/metabinner/mb2_master_depth.txt | awk '{if ($2>'"1000"') print $0 }' | cut -f -1,4- > ~/binning/${id}/metabinner/coverage_profile.tsv
  cd ~/.conda/envs/MetaBinner/bin/scripts/
  python3 gen_kmer.py ~/binning/${id}/mapping/${id}_1000bp.fasta 1000 4
  cd ~/binning/
  mv ~/binning/${id}/mapping/*_f1000.csv ~/binning/${id}/metabinner/
  cd ~/binning/
  run_metabinner.sh -a ~/binning/${id}/mapping/${id}_1000bp.fasta -o ~/binning/${id}/metabinner -d ~/binning/${id}/metabinner/coverage_profile.tsv -k ~/binning/${id}/metabinner/*_f1000.csv -p ~/.conda/envs/MetaBinner/bin -t 16
done

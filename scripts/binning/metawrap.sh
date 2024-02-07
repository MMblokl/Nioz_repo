#!bin/bash/
source $HOME/.bashrc.conda3 metawrap
#for d in ~/assembly/cami/*/
#do
#  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
#  echo $id
#  mkdir -p ~/binning/${id}/metawrap/work_files
#  for d2 in ~/assembly/cami/*/
#  do
#    id2=$(echo $d2 | awk -F "/" '{print $(NF-1)}')
#    cp ~/binning/${id}/mapping/sorted_${id2}.bam ~/binning/${id}/metawrap/work_files/${id2}.bam
#  done
#  metaWRAP binning --metabat2 --interleaved -a ~/binning/${id}/mapping/${id}_1000bp.fasta -o ~/binning/${id}/metawrap/ -t 16 -m 32 -l 1000 ~/assembly/cami/*/*sample_*.fastq
#  metaWRAP binning --maxbin2 --interleaved -a ~/binning/${id}/mapping/${id}_1000bp.fasta -o ~/binning/${id}/metawrap/ -t 16 -m 32 -l 1000 ~/assembly/cami/*/*sample_*.fastq
#  metaWRAP binning --concoct --interleaved -a ~/binning/${id}/mapping/${id}_1000bp.fasta -o ~/binning/${id}/metawrap/ -t 16 -m 32 -l 1000 ~/assembly/cami/*/*sample_*.fastq
#  metaWRAP bin_refinement -o ~/binning/${id}/metawrap -t 16 -m 40 -A ~/binning/${id}/metawrap/concoct_bins -B ~/binning/${id}/metawrap/metabat2_bins -C ~/binning/${id}/metawrap/maxbin2_bins   
#done

for d in ~/assembly/cellmock/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  echo $id
#  mkdir -p ~/binning/${id}/metawrap/work_files
#  for d2 in ~/assembly/cellmock/*/
#  do
#    id2=$(echo $d2 | awk -F "/" '{print $(NF-1)}')
#    cp ~/binning/${id}/mapping/sorted_${id2}.bam ~/binning/${id}/metawrap/work_files/${id2}.bam
#  done
#  metaWRAP binning --metabat2 -a ~/binning/${id}/mapping/${id}_1000bp.fasta -o ~/binning/${id}/metawrap/ -t 16 -l 1000 ~/assembly/cellmock/*/*_1.fastq ~/assembly/cellmock/*/*_2.fastq
#  metaWRAP binning --maxbin2 -a ~/binning/${id}/mapping/${id}_1000bp.fasta -o ~/binning/${id}/metawrap/ -t 16 -l 1000 ~/assembly/cellmock/*/*_1.fastq ~/assembly/cellmock/*/*_2.fastq
#  metaWRAP binning --concoct -a ~/binning/${id}/mapping/${id}_1000bp.fasta -o ~/binning/${id}/metawrap/ -t 16 -l 1000 ~/assembly/cellmock/*/*_1.fastq ~/assembly/cellmock/*/*_2.fastq
  metaWRAP bin_refinement -o ~/binning/${id}/metawrap -t 16 -m 40 -A ~/binning/${id}/metawrap/concoct_bins -B ~/binning/${id}/metawrap/metabat2_bins -C ~/binning/${id}/metawrap/maxbin2_bins
done

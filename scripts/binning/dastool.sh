#!bin/bash/
source $HOME/.bashrc.conda3 dastool
for d in ~/binning/*/mapping
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
#  cat ${id}/concoct/clustering_gt1000.csv | sed "s/.concoct_part_.,/\t/" > ~/binning/${id}/concoct/contig2bin.tsv
#  for mbbin in ${id}/metawrap/maxbin2_bins/*
#  do
#    mbbinnum=$(echo $mbbin | awk -F "/" '{print $NF}' | awk -F ".fa" '{print $1}')
#    mbcontig=$(cat $mbbin | egrep ">" | tr -d ">")
#    for xb in $mbcontig
#    do
#      printf "${xb}\t${mbbinnum}\n" >> ~/binning/${id}/metawrap/maxbin2_bins/contig2bin.tsv
#    done
#  done
#  for mbin in ${id}/metawrap/metabat2_bins/*
#  do
#    mbinnum=$(echo $mbin | awk -F "/" '{print $NF}' | awk -F ".fa" '{print $1}')
#    mcontig=$(cat $mbin | egrep ">" | tr -d ">")
#    for xm in $mcontig
#    do
#      printf "${xm}\t${mbinnum}\n" >> ~/binning/${id}/metawrap/metabat2_bins/contig2bin.tsv
#    done
#  done
##  for bin in ${id}/metawrap/concoct_bins/*
#  do
#    binnum=$(echo $bin | awk -F "/" '{print $NF}' | awk -F ".fa" '{print $1}')
#    contig=$(cat $bin | egrep ">" | tr -d ">")
##    for m in $contig
#    do
#      printf "${m}\t${binnum}\n" >> ~/binning/${id}/metawrap/concoct_bins/contig2bin.tsv
#    done
#  done
#  mkdir -p ~/binning/${id}/dastool/
  line1=~/binning/${id}/concoct/contig2bin.tsv
  line2=~/binning/${id}/metawrap/maxbin2_bins/contig2bin.tsv
  line3=~/binning/${id}/metawrap/metabat2_bins/contig2bin.tsv
  line4=~/binning/${id}/metabinner/metabinner_res/metabinner_result.tsv
  line5=~/binning/${id}/metawrap/concoct_bins/contig2bin.tsv
DAS_Tool -i ${line1},${line2},${line3},${line4},${line5} \
-l concoct,maxbin_metawrap,metabat_metawrap,metabinner,concoct_metawrap \
-c ~/binning/${id}/mapping/${id}_1000bp.fasta \
-o ~/binning/${id}/dastool/ \
--threads 16 \
--write_bins
done

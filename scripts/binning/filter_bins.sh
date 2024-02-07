#cat checkm/2018.08.15_09.49.32_sample_0/concoct/storage/bin_stats_ext.tsv | egrep -o "'Completeness': [0-9]{1,2}.[0-9]{1,2}.{0,}'Contamination': [0-9]{1,2}.[0-9]{1,2}"
#cat checkm/2018.08.15_09.49.32_sample_0/concoct/storage/bin_stats_ext.tsv | awk -F "\t" '{print $1}'
#!bin/bash/
for d in ~/binning/*/mapping
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  echo $id
  while read -r line
  do
    echo $line | awk -F "\t" '{print $1}'
    echo $line | egrep -o "'Completeness': [0-9]{1,2}.[0-9]{1,2}.{0,}'Contamination': [0-9]{1,2}.[0-9]{1,2}"
  done < ~/binning/checkm/${id}/concoct/storage/bin_stats_ext.tsv
done

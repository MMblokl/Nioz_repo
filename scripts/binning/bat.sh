#!bin/bash/
for d in ~/binning/filtered_bins/*/metabinner/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  echo $id
  CAT bins -b $d -d ~/CAT_database_15-11-2023/CAT_database.2023-11-15 -t ~/CAT_database_15-11-2023/CAT_taxonomy.2023-11-15 -n 16 -o ${d}/out.BAT -s .fna -n 16
done

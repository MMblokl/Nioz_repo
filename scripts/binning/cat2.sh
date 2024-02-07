#!bin/bash/
for d in ~/binning/*/mapping
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  cd ${id}
  #CAT contigs -c ~/binning/${id}/mapping/${id}_1000bp.fasta -d ~/CAT_database_15-11-2023/CAT_database.2023-11-15 -t ~/CAT_database_15-11-2023/CAT_taxonomy.2023-11-15 -n 16
  CAT add_names -i ~/binning/${id}/out.CAT.contig2classification.txt -o ~/binning/${id}/CATnames.txt -t ~/CAT_database_15-11-2023/CAT_taxonomy.2023-11-15 --only_official --exclude_scores
  cd ..
done

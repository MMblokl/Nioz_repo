#!bin/bash/
for dir in */*/;
do
  sample=$(echo $dir | awk -F "/" '{print $2}')
  echo "Tool,Genome_fraction,Duplication_ratio,Misasseblies,mismatch_per_100kb,NGA50" > quast_evals/${sample}_ref.csv
  for toolpath in ${dir}*/quast_outp/summary/TSV;
  do
    toolname=$(echo ${toolpath} | awk -F "/" '{print $3}')
    gen=$(cat ${toolpath}/Genome_fraction.tsv | awk 'NR>1{print $2}' | awk '{s+=$1}END{print s/NR}')
    dup=$(cat ${toolpath}/Duplication_ratio.tsv | awk 'NR>1{print $2}' | awk '{s+=$1}END{print s/NR}')
    mis=$(cat ${toolpath}/num_misassemblies.tsv | awk 'NR>1{print $2}' | awk '{s+=$1}END{print s/NR}')
    mism=$(cat ${toolpath}/num_mismatches_per_100_kbp.tsv | awk 'NR>1{print $2}' | awk '{s+=$1}END{print s/NR}')
    nga=$(cat ${toolpath}/NGA50.tsv | awk 'NR>1{print $2}' | awk '{s+=$1}END{print s/NR}')
    printf ${toolname},${gen},${dup},${mis},${mism},${nga}"\n" >> quast_evals/${sample}_ref.csv
  done
done

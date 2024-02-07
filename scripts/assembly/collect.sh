#!bin/bash/
for d in simulation_short_read/*/;
do
  cat ${d}spades/quast_outp/summary/TSV/Genome_fraction.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> spades_Genome_fraction.txt
  cat ${d}spades/quast_outp/summary/TSV/num_mismatches_per_100_kbp.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> spades_mismatch_100kbp.txt
  cat ${d}spades/quast_outp/summary/TSV/Duplication_ratio.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> spades_Duplication_ratio.txt
  cat ${d}spades/quast_outp/summary/TSV/NGA50.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> spades_NGA50.txt
  cat ${d}spades/quast_outp/summary/TSV/num_misassemblies.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> spades_misassemblies.txt
done

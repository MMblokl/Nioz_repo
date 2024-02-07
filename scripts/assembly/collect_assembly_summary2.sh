#!bin/bash/
for d in */;
do
  cat ${d}/idba/quast_outp_noref/summary/TSV/Genome_fraction.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> idba_Genome_fraction.txt
  cat ${d}/idba/quast_outp_noref/summary/TSV/num_mismatches_per_100_kbp.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> idba_mismatch_100kbp.txt
  cat ${d}/idba/quast_outp_noref/summary/TSV/Duplication_ratio.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> idba_Duplication_ratio.txt
  cat ${d}/idba/quast_outp_noref/summary/TSV/NGA50.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> idba_NGA50.txt
  cat ${d}/idba/quast_outp_noref/summary/TSV/num_misassemblies.tsv | awk 'NR>1{print $2}' | awk -v d=${d} '{s+=$1}END{print d,s/NR}' >> idba_misassemblies.txt
done

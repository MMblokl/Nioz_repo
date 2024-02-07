#!bin/bash/
for x in gtdbtk/*/*
do
  cat ${x}/gtdbtk.ar*.summary.tsv | awk -F "\t" 'NR>1{print $1"\t"$2"\t"$3}' > ${x}/bintax.tsv
  cat ${x}/gtdbtk.bac*.summary.tsv | awk -F "\t" 'NR>1{print $1"\t"$2"\t"$3}' >> ${x}/bintax.tsv
done

#!bin/bash/
#This script counts the amount of read in each reference genome, and adds the respective name to a file.
#This file can be used to calculate the original abundances.
for d in ~/assembly/cami/*/reads/*.tsv
do
  name=$(echo $d | awk -F "/" '{print $(NF-2)}')
  awk FNR-1 ${d} | awk -F "\t" '{print $2}' | sort | uniq -c > ${name}.tsv
  touch ${name}_readcounts.tsv
  while read line;
    do
      otu=$(echo $line | awk -F " " '{print $2}')
      otu=$(echo $otu | sed "s/\./\\\./")
      genome=$(cat ~/assembly/cami/genome_to_id.tsv | egrep "${otu}[[:space:]]" | awk -F "/" '{print $NF}')
      printf "${line}\t${genome}\n" >> ${name}_readcounts.tsv
    done < "${name}.tsv"
done

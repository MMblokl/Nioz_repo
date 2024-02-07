#!bin/bash/

#This scripts gets the number of reads mapped to each contig.
#The number should be divided by 2 because the reads are paired end and both reads
#Get aligned to the same contig usually.

#The -F flag is in order to filter out any non-primary alignment, supplementary
# alignments, and unmapped reads from the results.

for d in ~/binning/*/mapping
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  samtools view -F 0x904 -f 0x02 ${d}/sorted_${id}.bam | cut -f 1-4 | awk -F "\t" '{print $3}' | uniq -c > ${id}_readmapping.txt
done

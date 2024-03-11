#!bin/bash/

for d in ~/binning/*/mapping
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  mkdir -p ${id}/salmon_quant/index
  module load salmon/1.10.1
  salmon index -p 16 -t ${d}/${id}_1000bp.fasta -i ${id}/salmon_quant/index/
  salmon quant -i ${id}/salmon_quant/index/ --libType IU -1 ~/assembly/reads/${id}/${id}_1.fastq -2 ~/assembly/reads/${id}/${id}_2.fastq -o ${id}/salmon_quant/readbased_quant --meta -p 16
  salmon quant -p 16 --libType IU --output ${id}/salmon_quant/alignment_quant -a ~/binning/${id}/mapping/sorted_*.bam -t ~/binning/${id}/mapping/${id}_1000bp.fasta
done

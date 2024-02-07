#!bin/bash/

#for d in ~/assembly/cami/*/
#do
#  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
#  mkdir -p ~/binning/${id}
#  mkdir -p ~/binning/${id}/mapping/
#  cp ${d}spades/contigs.fasta ~/binning/${id}/mapping/
#  seqtk seq -L 1000 ~/binning/${id}/mapping/contigs.fasta > ~/binning/${id}/mapping/{id}_1000bp.fasta
#  for d2 in ~/assembly/cami/*/
#  do
#    id2=$(echo $d2 | awk -F "/" '{print $(NF-1)}')
#    bbmap.sh ref=~/binning/${id}/mapping/${id}_1000bp.fasta in=~/assembly/cami/${id2}/reads/anonymous_reads.fastq out=~/binning/${id}/mapping/mapped_${id2}.sam -threads=16
#    samtools view -b ~/binning/${id}/mapping/mapped_${id2}.sam -o ~/binning/${id}/mapping/rawbam_${id2}.bam
#    rm -f ~/binning/${id}/mapping/mapped_${id2}.sam
#    samtools sort ~/binning/${id}/mapping/rawbam_${id2}.bam -o ~/binning/${id}/mapping/sorted_${id2}.bam
#    rm -f ~/binning/${id}/mapping/rawbam_${id2}.bam
#    samtools index -b -@ 16 ~/binning/${id}/mapping/sorted_${id2}.bam ~/binning/${id}/mapping/sorted_${id2}.bam.bai
#  done
#done

for d in ~/assembly/cellmock/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  mkdir -p ~/binning/${id}
  mkdir -p ~/binning/${id}/mapping/
#  cp ${d}spades/contigs.fasta ~/binning/${id}/mapping/
#  seqtk seq -L 1000 ~/binning/${id}/mapping/contigs.fasta > ~/binning/${id}/mapping/${id}_1000bp.fasta
  for d2 in ~/assembly/cellmock/*/
  do
    id2=$(echo $d2 | awk -F "/" '{print $(NF-1)}')
    bbmap.sh ref=~/binning/${id}/mapping/${id}_1000bp.fasta in=~/assembly/cellmock/${id2}/${id2}_1.fastq in2=~/assembly/cellmock/${id2}/${id2}_2.fastq out=~/binning/${id}/mapping/mapped_${id2}.sam -threads=16
    samtools view -b ~/binning/${id}/mapping/mapped_${id2}.sam -o ~/binning/${id}/mapping/rawbam_${id2}.bam
    rm -f ~/binning/${id}/mapping/mapped_${id2}.sam
    samtools sort ~/binning/${id}/mapping/rawbam_${id2}.bam -o ~/binning/${id}/mapping/sorted_${id2}.bam
    rm -f ~/binning/${id}/mapping/rawbam_${id2}.bam
    samtools index -b -@ 16 ~/binning/${id}/mapping/sorted_${id2}.bam ~/binning/${id}/mapping/sorted_${id2}.bam.bai
  done
done

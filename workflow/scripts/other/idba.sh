#!bin/bash
echo "Usage: idba.sh fw_reads.fastq rv_reads.fasta output_directory"

mkdir -p $3 #create the output dir if doesn't exist
fq2fa --merge $1 $2 $3/fastareads.fa #merge the paired end fastq files into one fasta file

idba_ud -r $3/fastareads.fa -o $3/ --mink 80 --maxk 80 --num_threads 16 #run idba
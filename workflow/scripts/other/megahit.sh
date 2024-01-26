#!bin/bash/
echo "Usage: megahit.sh fw_reads.fastq rv_reads.fastq output_dir"

megahit -1 $1 -2 $2 -o $3 -t 16

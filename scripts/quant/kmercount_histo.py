import glob
import os
import sys


#Usage: kmercount_histo.py sampleid outdir binreads_dir

#jellyfish count -m mer_size -t 16 -s 16G -C -o outp fw_reads.fq rv_reads.fq

sampleid = sys.argv[1]
outdir = sys.argv[2]
readir = sys.argv[3]

for file in glob.glob(f"{readir}/*_fw.fastq"):
  bin = file.split("/")[-1].split("_fw")[0]
  print(bin)
  os.system(f"jellyfish count -m 20 -t 16 -s 5M -C -o {outdir}/{bin}.sf {sampleid}/reads/{bin}_fw.fastq {sampleid}/reads/{bin}_rv.fastq")
  os.system(f"jellyfish histo -o {outdir}/{bin}.histo {outdir}/{bin}.sf")

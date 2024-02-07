import glob
import os
import sys

#jellyfish count -m mer_size -t 16 -s 16G -C -o outp fw_reads.fq rv_reads.fq

sampleid = sys.argv[1]
outdir = sys.argv[2]
binfile = sys.argv[3]

for file in glob.glob(f"{binfile}/*"):
  bin = file.split("/")[-1]
  print(bin)
  os.system(f"jellyfish count -m 20 -t 16 -s 5M -C -o {outdir}/{bin}.sf {sampleid}/reads/{bin}_fw.fastq {sampleid}/reads/{bin}_rv.fastq")
  os.system(f"jellyfish histo -o {outdir}/{bin}.histo {outdir}/{bin}.sf")

import glob
import os
import sys
#This script creates a .histo file for a specific sample, which is used in jellyfish
# to estimate the genomesize of the bins in the sample.


#Usage: kmercount_histo.py sampleid outdir binreads_dir

#jellyfish count -m mer_size -t 16 -s 16G -C -o outp fw_reads.fq rv_reads.fq

sampleid = sys.argv[1] #The id or name of the sample
outdir = sys.argv[2] #The directory to output the .histo files in
readir = sys.argv[3] #The directory containing the forward and reverse reads, seperated by bin. 
            #These files can be generated by the "seperate_binreads.py" script.

if len(sys.argv) < 4:
  print("Usage: python3 kmercount_histo.py SAMPLE_ID_IN_PLAINTEXT /output/directory/ /dir/with/seperated/reads/")
  exit()

for file in glob.glob(f"{readir}/*_fw.fastq"):
  if "unbinned" not in file: #make sure the unbinned reads are not counted as this would take quite a long time and will not be used anyways.
    bin = file.split("/")[-1].split("_fw")[0]
    print(bin)
    os.system(f"jellyfish count -m 20 -t 16 -s 5M -C -o {outdir}/{bin}.sf {readir}/{bin}_fw.fastq {readir}/{bin}_rv.fastq")
    os.system(f"jellyfish histo -o {outdir}/{bin}.histo {outdir}/{bin}.sf")
  else:
    continue

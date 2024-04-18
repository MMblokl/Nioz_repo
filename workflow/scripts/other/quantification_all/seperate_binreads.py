import glob
import os
import sys

#This script seperates the reads based on what bin they align to.
# This is mainly done with samtools, and will take quite a while.

#USAGE
# python3 seperate_binreads.py sampleid bamfile.BAM path/to/final_bins/ read/output/location/

#The arguments given to the script must be:
# 1: sampleid
# 2: bamfile
# 3: bin file directory
# 4: the output location for where to place the fasta files
# 5: the location of the unbinned.txt file made by the find_residuals.py script
# 6: The location of the contig depth file

sampleid = sys.argv[1]
bamfile = sys.argv[2]
bins_dir = sys.argv[3]
output_dir = sys.argv[4]
unbinned_filelocation = sys.argv[5]
contig_depthfile = sys.argv[6]


#Get the contigdepth for the sample and match to each contig, then split.
with open(f"{contig_depthfile}", "r") as f:
  depths = {}
  f.readline()
  line = f.readline()
  while line != '':
    t = line.strip().split(" ")
    contig = t[0].strip('"')
    depths[contig] = t[1]
    line = f.readline()
    

#Make a dict with bin names as the key and a list of contig ids that are in the bin
bincontigs = {}
for bin in glob.glob(f"{bins_dir}/*.fna"):
  print(bin)
  os.system("rm -f temp.txt")
  os.system("""cat %s | egrep ">" | awk -v bin="%s" '{print $1,bin}' >> temp.txt""" % (bin,bin))
  bin = bin.split("/")[-1]
  with open("temp.txt", "r") as f, open(f"{output_dir}/depths/{bin}.txt", "w") as o:
    line = f.readline()
    while line != "":
      line = line.split(" ")
      bin = line[1].strip()
      contig = line[0][1:]
      o.write(f"{contig}\t{depths[contig]}\n")
      try:
        bincontigs[bin].append(contig)
      except KeyError:
        bincontigs[bin] = [contig]
      line = f.readline()


#Add the contigs in given unbinned_file into the bincontigs dict to seperate
#These as well so that they can be used later as well.
# This file is made using the "find_residuals.sh" script
bincontigs["unbinned"] = []
with open(unbinned_filelocation, "r") as f:
  line = f.readline()
  while line != "":
    line = line[1:].strip()
    bincontigs["unbinned"].append(line)
    line = f.readline()


#Put the reads into their own files to match them to the bins.
for bin in bincontigs.keys():
  outfile = f"{output_dir}/reads/{bin.split('/')[-1]}"
  os.system(f"touch {outfile}_fw.fastq")
  os.system(f"touch {outfile}_rv.fastq")
  for contig in bincontigs[bin]:
    os.system("""samtools view -G 0x904 -f 0x42 %s %s | sort -V -k1 | awk -F "\t" '{print "@"$1"\\n" $10"\\n+\\n" $11}' >> %s_fw.fastq""" % (bamfile, contig, outfile))
    os.system("""samtools view -G 0x904 -f 0x82 %s %s | sort -V -k1 | awk -F "\t" '{print "@"$1"\\n" $10"\\n+\\n" $11}' >> %s_rv.fastq""" % (bamfile, contig, outfile))


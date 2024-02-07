import glob
import os
import sys

#The arguments given to the script must be:
# 1: sampleid
# 2: bamfile
# 3: bin file directory 

sampleid = sys.argv[1]
bamfile = sys.argv[2]
bins_dir = sys.argv[3]


#Make a dict with bin names as the key and a list of contig ids that are in the bin
bincontigs = {}
for bin in glob.glob(f"{bins_dir}/*"):
  print(bin)
  os.system("rm -f temp.txt")
  os.system("""cat %s | egrep ">" | awk -v bin="%s" '{print $1,bin}' >> temp.txt""" % (bin,bin))
  with open("temp.txt", "r") as f:
    line = f.readline()
    while line != "":
      line = line.split(" ")
      bin = line[1].strip()
      try:
        bincontigs[bin].append(line[0][1:])
      except KeyError:
        bincontigs[bin] = [line[0][1:]]
      line = f.readline()

#Put the reads into their own files to match them to the bins.
for bin in bincontigs.keys():
  outfile = f"{sampleid}/reads/{bin.split('/')[-1]}"
  os.system(f"touch {outfile}_fw.fastq")
  os.system(f"touch {outfile}_rv.fastq")
  for contig in bincontigs[bin]:
    os.system("""samtools view -G 0x904 -f 0x42 %s %s | sort -V -k1 | awk -F "\t" '{print "@"$1"\\n" $10"\\n+\\n" $11}' >> %s_fw.fastq""" % (bamfile, contig, outfile))
    os.system("""samtools view -G 0x904 -f 0x82 %s %s | sort -V -k1 | awk -F "\t" '{print "@"$1"\\n" $10"\\n+\\n" $11}' >> %s_rv.fastq""" % (bamfile, contig, outfile))


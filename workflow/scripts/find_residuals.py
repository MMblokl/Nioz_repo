import os
import glob
import sys

#This script finds all the residual contigs that are not included in any of
#the final bins and puts the ids in a file.
#This can then be used to make sure the quantification of the final bins don't
# get inflated due to the reads mapped to these contigs not being accounted for.

#This also gets used in the seperate_binreads.py script.

#Arguments ----------
sampleid = sys.argv[1] #The id of the sample
contigs = sys.argv[2] #The file containing the contigs used in the binning process.
bins_dir = sys.argv[3] #The path to the >>> FILTERED <<< bins.
sampleid = sys.argv[4]
output_file = sys.argv[5] #The output file for the _unbinned.txt file.

if len(sys.argv) < 6:
  print("Usage: python3 find_residuals.py SAMPLE_ID_IN_PLAINTEXT contigs.fasta /path/to/bin/dir/ output_file")
  exit()


os.system("rm -f %s_unbinned_temp.txt" % (sampleid))
os.system("""cat %s | egrep ">" > %s_unbinned_temp.txt""" % (contigs, sampleid)) #We get every contig from the original list.
for bin in glob.glob(f"{bins_dir}/*.fna"): #We loop through each bin file in the directorty
  os.system("""cat %s | egrep ">" >> %s_unbinned_temp.txt""" % (bin, sampleid)) #Each final bin is looked through and then we write each contig ID into the temp.txt file.
    
#All the unique contig ids are written to the output file. Since a contigid
#Should appear twice if it exists in both the final bins and the originals,
# a contig that only appears once only exists in the original contigs.
#As such all unique contig headers are unbinned since they do not appear in any of the bins.
os.system(f"cat {sampleid}_unbinned_temp.txt | sort | uniq -u > {output_file}")

#Removing the file once it is no longer needed.
os.system(f"rm -f {sampleid}_unbinned_temp.txt")

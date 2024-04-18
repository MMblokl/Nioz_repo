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
output_file = sys.argv[4] #The output file for the _unbinned.txt file.



os.system("rm -f temp.txt")
os.system("""cat %s | egrep ">" > temp.txt""" % (contigs)) #We get every contig from the original list.
for bin in glob.glob(f"{bins_dir}/*.fna"): #We loop through each bin file in the directorty
  os.system(f"""cat {bin} | egrep ">" >> temp.txt""") #Each final bin is looked through and then we write each contig ID into the temp.txt file.
    
  #After we add the original contig IDs together into one file with the contig IDs in the final bins, each contig ID
  # that does NOT appear more than once would not be binned, so it is unbinned.
os.system(f"cat temp.txt | sort | uniq -u > {output_file}")

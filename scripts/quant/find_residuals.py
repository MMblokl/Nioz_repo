import os
import glob

#This script finds all the residual contigs that are not included in any of
#the final bins and puts the ids in a file.
#This can then be used to make sure the quantification of the final bins don't
# get inflated due to the reads mapped to these contigs not being accounted for.

for file in glob.glob("/export/lv6/user/mblokland/binning/*/mapping"):
  id = file.split("/")[-2]
  os.system("rm -f temp.txt")
  os.system("""cat /export/lv6/user/mblokland/binning/%s/mapping/%s_1000bp.fasta | egrep ">" > temp.txt""" % (id, id))
  for bin in glob.glob(f"/export/lv6/user/mblokland/binning/filtered_bins/{id}/metabinner/*.fna"):
    os.system(f"""cat {bin} | egrep ">" >> temp.txt""")
  os.system(f"cat temp.txt | sort | uniq -u > {id}_unbinned.txt")

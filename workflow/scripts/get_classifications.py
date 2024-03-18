import sys
import glob

#This script reads the classifications by gtdbtk in the "gtdbtk_dir" dir.
#These are then placed in a single human-readable file as the "outfile" argument.



#arguments:
outfile = sys.argv[1]
gtdb_dir = sys.argv[2]

classfiles = glob.glob(f"{gtdb_dir}/gtdbtk.*.summary.tsv")



classifications = {}
for file in classfiles:
  with open(f"{file}", "r") as f:
    f.readline()
    line = f.readline()
    while line != "":
      t = line.split("\t")
      bin = t[0]
      
      classification = t[1].split(";") #We split the classifications by their seperator.
      classification = [x[3:] for x in classification] #Here, the s__, g__, etc. headers are removed as these are useless to us
      
      #We need to remove the _A/_B/_E parts from the species classification as this is not that usefull for us
      species = classification[-1].split(" ")[-1].split("_")[0] #The final part of the species classification
      genus = classification[-2].split("_")[0]
      
      #Here, the species classification is replaced with "NA" if it is empty, meaning there was no species specific classification by gtdbtk
      if species == "":
        classification[-1] = "NA"
      else:
        classification[-1] = " ".join([genus,species])
      classification[-2] = genus
      
      classifications[bin] = classification
      line = f.readline()

#Writing the classifications into a more human readable and convenient format.
with open(f"{outfile}", "w") as o:
  o.write("Bin/genome\tsuperkingdom\tphylum\tclass\torder\tfamily\tgenus\tspecies\n")
  for c in classifications.keys():
    trailing = "\t".join(classifications[c])
    o.write(f"{c}\t{trailing}\n")





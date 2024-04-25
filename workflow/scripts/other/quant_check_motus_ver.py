import sys
import os
#import numpy

#This script is an altered version of the quant_check.py script to work with only
# the mOTUs output.


#Arguments
motus_prof_dir = sys.argv[1] #The location containing all three types of mOTU profile.
true_quants = sys.argv[2] #File that contains true sample abundance
sampleid = sys.argv[3]
outdir = sys.argv[4]

if len(sys.argv) < 5:
  print("Usage: python3 quant_check_motus_ver.py /motus_profile_directory/ /path/to/true_abundance.csv ID_IN_PLAINTEXT /output/directory/")
  exit()


def get_deviation(file, outfile, genus=False):
  #This does the whole reads the given file, and matches it to the true.
  # genus tells the function whether the given file is genus classification
  #values = []
  with open(f"{file}", "r") as f, open(f"{outfile}", 'w') as o:
    f.readline()
    line = f.readline()
    while line != "":
      #Split the classification from the estimation.
      t = line.strip().split("\t")
      
      #The estimated abundance, converted to complete percentages
      abundance = float(t[1]) * 100
      
      if genus:
        #This line only works for the genus specific classification due to
        # text formatting.
        classification = t[0].split("|")[-1][3:].strip()
      else:
        #For some reason, ncbi likes to put brackets around the genus name in the species classifications
        # from time to time. This is just to remove it.
        sep = t[0].split("|")[-1].split("s__")[1].split(" ")[:-1]
        sep = [x.strip("[]") for x in sep]
        classification = "_".join(sep)
        
      #Match the classification with the true value using egrep
      os.system("""cat %s | egrep %s > temp.txt""" % (true_quants, classification))
      
      with open("temp.txt", 'r') as f2:
        #This is the sum of all true abundances that match with the species name.
        true_sum = 0
        line2 = f2.readline()
        while line2 != "":
          #Split the line on the comma
          t2 = line2.strip().split(",")
          #Add the true abundance to the sum.
          true_sum += float(t2[1])
          line2 = f2.readline()
      
      #Save the deviation into the output dict.
      #The if is to make sure that the non-matched species do not get mixed up into
      # the deviation file.
      if true_sum > 0:
        deviation = abs(abundance - true_sum)
        o.write(f"{classification}\t{deviation}\n")
        #values.append(deviation)

      #Next estimation
      line = f.readline()
    #o.write(f"{sampleid}\t{numpy.average(values)}\n")


deviation_species = get_deviation(f"{motus_prof_dir}/motu_species.txt", f"{outdir}/motu_species_acc.txt")
deviation_genus = get_deviation(f"{motus_prof_dir}/motu_genus.txt", f"{outdir}/motu_genus_acc.txt", True)

  
  

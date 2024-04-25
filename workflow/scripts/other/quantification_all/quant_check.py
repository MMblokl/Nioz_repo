import sys
import numpy


#Arguments
quant_file = sys.argv[1] #File with estimated quantifications
true_quants = sys.argv[2] #File that contains true sample abundance
classification_file = sys.argv[3] #File that contains the bin classifications
outdir = sys.argv[4]



classifications = {}
#Read the classifications of genus and species level into a dict to be used for matching the true and estimated classifications
with open(f"{classification_file}", "r") as f:
	f.readline()
	line = f.readline()
	while line != "":
		t = line.strip().split("\t")
		species = t[-1].replace(" ", "_")
		genus = t[-2]
		bin = t[0]
		classifications[bin] = (genus, species)
		line = f.readline()

#Read the true abundances into a dict.
#The keys are the names of the species, and the values are the true abundance of this species.
true_abundances = {}
with open(f"{true_quants}", "r") as f:
  f.readline()
  line = f.readline()
  while line != "":
    t = line.strip().split(",")
    true_abundances[t[0].strip('"')] = float(t[1])
    line = f.readline()


#Read the quantifications into a dict.
#The keys are bin names, Each value is a dictionary with the specific quantification
# method number as the key, and the quantification of this method as the value.ication
quantifications = {}
with open(f"{quant_file}", "r") as f:
  line = f.readline()
  #Read the first line headers
  headers = [x for x in line.strip().split("\t")[1:]]
  line = f.readline()
  while line != '':
    t = line.strip().split("\t")
    bin = t[0]
    t = t[1:]
    quantifications[bin] = {}
    for index in range(0,len(headers)):
      quantifications[bin].update({headers[index]: t[index]})
    line = f.readline()


#Get the true abundance for species and genus from the classification names and
# get the absolute difference in percentage. This absolute value is then averaged over the entire sample.

#Two dictionaries to save each quantification result for each bin.
# The keys are the specific quantification method numbers, where the
# quantification of each bin from this method is saved into a list as the value.
enum_quants_spe = {k: [] for k in headers}
enum_quants_gen = {k: [] for k in headers} 

with open(f"{outdir}/species_acc.txt", "w") as spo, open(f"{outdir}/genus_acc.txt", "w") as geo, \
open(f"{outdir}/matched_genus.txt", 'w') as genus_matched, open(f"{outdir}/matched_species.txt", 'w') as species_matched:
  spo.write("\t".join(headers))
  spo.write("\n")
  geo.write("\t".join(headers))
  geo.write("\n")
  for bin in quantifications.keys():
    #We do not want to have the unbinned bin quantification in the final results as this will muddy the accuracy
    if bin == "unbinned":
      continue
    classification = classifications[bin]
    #The gtdbtk classification on genus level
    genus = classification[0]
    #The gtdbtk classification on species level.
    species = classification[1]
    #The quantifications of the specific bin from all methods.
    bin_quantifications = quantifications[bin]
    
    #Two dictionaries are created which will contain all true abundances of
    # the species that match with the classification from gtdbtk.
    matched_genus = {}
    matched_species = {}
    
    #We get the true abundances here. Name refers to the species name.
    for name in true_abundances.keys():
      #If the genus if found in the name of the true abundance, it is saved to
      # the matched genus dict to indicate that this abundance is linked to the
      # gtdb-tk classification.
      if genus in name:
        matched_genus[name] = true_abundances[name]
        #We write the matched genus into a file in order to see which species from the true
        # were matched. This is mainly for checking errors.
        genus_matched.write(f"{name}\t{bin}\n")

    for name in matched_genus.keys():
      if species in name:
        matched_species[name] = matched_genus[name]
        #The true abundance species matched to a specific bin is printed to a check file just like the genus.
        species_matched.write(f"{name}\t{bin}\n")
    
    #The true abundances are summed into one value, this is then used to calculate
    # the deviation of the quantification from the true abundance.
    genus_sum = sum(matched_genus.values())
    species_sum = sum(matched_species.values())
    
    for method in bin_quantifications.keys():
      quant = float(bin_quantifications[method])
      diff_genus = quant - genus_sum
      diff_species = quant - species_sum
      
      #We add the quantification difference and use the abs() function to make it absolute, as we want
      #to use this result to see which method has the least variation
      enum_quants_spe[method].append(abs(diff_species))
      enum_quants_gen[method].append(abs(diff_genus))
      
  #We take the average of the difference for each method to create an output here
  out_spe = [str(numpy.average(x)) for x in enum_quants_spe.values()]
  out_gen = [str(numpy.average(x)) for x in enum_quants_gen.values()]
    
  #We write the output
  geo.write("\t".join(out_gen))
  geo.write("\n")
  spo.write("\t".join(out_spe))
  spo.write("\n")
  




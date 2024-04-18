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

#Read the true abundances into a dict, very original :)
true_abundances = {}
with open(f"{true_quants}", "r") as f:
  f.readline()
  line = f.readline()
  while line != "":
    t = line.strip().split(",")
    true_abundances[t[0].strip('"')] = float(t[1])
    line = f.readline()


#Read the quantifications into a dict, bins are the keys where the values are bins with the keys, the specific approach, and the values the quantification
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

enum_quants_spe = {k: [] for k in headers}
enum_quants_gen = {k: [] for k in headers} #Just create a copy variant of the dict as you can't easily copy a dict in python.
with open(f"{outdir}/species_acc.txt", "w") as spo, open(f"{outdir}/genus_acc.txt", "w") as geo:
  spo.write("\t".join(headers))
  spo.write("\n")
  geo.write("\t".join(headers))
  geo.write("\n")
  for bin in quantifications.keys():
    #We do not want to have the unbinned bin quantification in the final results as this will muddy the accuracy
    if bin == "unbinned":
      continue
    classification = classifications[bin]
    genus = classification[0]
    species = classification[1]
    bin_quantifications = quantifications[bin]
    
    matched_genus = {}
    matched_species = {}
    
    #We get the true abundances here
    for name in true_abundances.keys():
      if genus in name:
        matched_genus[name] = true_abundances[name]
    
    for name in matched_genus.keys():
      if species in name:
        matched_species[name] = matched_genus[name]
    
    #Create a "sum" of the true quantifications of the genus and species so that we can calulate the difference
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
  




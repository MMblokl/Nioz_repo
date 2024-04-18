import sys

#Arguments
quant_file = sys.argv[1]
true_quants = sys.argv[2]
classification_file = sys.argv[3]
outdir = sys.argv[4]



#DIT ZIJN DE VERDOMDE BAT NAMES VERVANG HET MET ANDER DING
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


#Read the quantifications into a dict, bins are the keys where the values are more bins with the keys the specific approach, and the values the quantification
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

with open(f"{outdir}/species_acc.txt", "w") as spo, open(f"{outdir}/genus_acc.txt", "w") as geo:
  spo.write("Bin\t")
  spo.write("\t".join(headers))
  spo.write("\n")
  geo.write("Bin\t")
  geo.write("\t".join(headers))
  geo.write("\n")
  for bin in quantifications.keys():
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
    
    genus_sum = sum(matched_genus.values())
    species_sum = sum(matched_species.values())
    
    outline_gen = [bin]
    outline_spe = [bin]
    
    for method in bin_quantifications.keys():
      quant = float(bin_quantifications[method])
      diff_genus = quant - genus_sum
      diff_species = quant - species_sum
      outline_gen.append(str(diff_genus))
      outline_spe.append(str(diff_species))
    
    geo.write("\t".join(outline_gen))
    geo.write("\n")
    spo.write("\t".join(outline_spe))
    spo.write("\n")
  



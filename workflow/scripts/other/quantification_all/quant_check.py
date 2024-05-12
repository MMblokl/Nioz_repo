import sys
import numpy
import pandas as pd


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


def rmsd(estimations, true_list):
  #Calculate the RMSD using a list of estimations and a list of true values,
  # both of same size.
  rmsd = numpy.sqrt(((numpy.array(estimations) - numpy.array(true_list)) ** 2).mean())
  return rmsd


bin_list = list(quantifications.keys())
bin_list.remove("unbinned")


#Get the true abundance for species and genus from the classification names and
# get the absolute difference in percentage. This absolute value is then averaged over the entire sample.

#Two dictionaries to save each quantification result for each bin.
# The keys are the specific quantification method numbers, where the
# quantification of each bin from this method is saved into a list as the value.
enum_quants_spe = {k: [] for k in headers}
enum_quants_gen = {k: [] for k in headers} 

with open(f"{outdir}/species_acc.txt", "w") as species_abs_out, open(f"{outdir}/genus_acc.txt", "w") as genus_abs_out, \
open(f"{outdir}/matched_genus.txt", 'w') as genus_matched, open(f"{outdir}/matched_species.txt", 'w') as species_matched, \
open(f"{outdir}/RMSD_genus.txt", 'w') as genus_rmsd_out, open(f"{outdir}/RMSD_species.txt", 'w') as species_rmsd_out:
  
  #List to calculate the root mean square deviation RMSD between these lists, once per sample.
  #This is then used instead of the average of the absolute difference.
  sample_quants = [] # A list contain the dicts of all method quantifications.
  true_gen = []
  true_spe = []
  
  #Header line
  headers = "\t".join(headers)
  species_abs_out.write(f"{headers}\n")
  genus_abs_out.write(f"{headers}\n")
  species_rmsd_out.write(f"{headers}\n")
  genus_rmsd_out.write(f"{headers}\n")
  
  for bin in bin_list:
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
    
    
    #This is a list of the true species and genus values to be used in the RMSD
    #Including a list of all bin_quantification dicts from all bins, which
    #contain the estimations of each method.
    true_gen.append(genus_sum)
    true_spe.append(species_sum)
    sample_quants.append(bin_quantifications)

    for method in bin_quantifications.keys():
      quant = float(bin_quantifications[method])
      #The difference in genus and species is calculated here, which is used for the absolute next.
      diff_genus = quant - genus_sum
      diff_species = quant - species_sum
      
      #We add the quantification difference and use the abs() function to make it absolute, as we want
      #to use this result to see which method has the least variation
      enum_quants_spe[method].append(abs(diff_species))
      enum_quants_gen[method].append(abs(diff_genus))
  
  rmsd_genus = []
  rmsd_species = []
  #We put the estimations into a list in order to generate the RMSD deviation.
  #This is done via pandas and numpy
  sample_quants = pd.DataFrame(sample_quants)
  for mtd in sample_quants.keys():
    #A list of all estimations from one specific method
    estimations = sample_quants[mtd].tolist()
    estimations = [float(x) for x in estimations] # Create the list as floats and not strings.
    
    #We calculate the RMSD using the rmsd() function
    rmsd_species.append(str(rmsd(estimations, true_spe)))
    rmsd_genus.append(str(rmsd(estimations, true_gen)))
  
  #The RMSD output
  species_rmsd_out.write("\t".join(rmsd_species))
  species_rmsd_out.write("\n")
  genus_rmsd_out.write("\t".join(rmsd_genus))
  genus_rmsd_out.write("\n")
  
  #A pandas dataframe is created in order to match which species were matched to which
  # bins, which is then output to a file.
  genus_dev = pd.DataFrame.from_dict(enum_quants_gen)
  genus_dev.index = bin_list
  species_dev = pd.DataFrame.from_dict(enum_quants_spe)
  species_dev.index = bin_list
  #Write to txt file in csv format.
  genus_dev.to_csv(f"{outdir}/genus_acc_bins.txt", sep="\t")
  genus_dev.to_csv(f"{outdir}/species_acc_bins.txt", sep="\t")
  
  #This is the output for the absolute differences
  out_spe = [str(numpy.average(x)) for x in enum_quants_spe.values()]
  out_gen = [str(numpy.average(x)) for x in enum_quants_gen.values()]
  genus_abs_out.write("\t".join(out_gen))
  genus_abs_out.write("\n")
  species_abs_out.write("\t".join(out_spe))
  species_abs_out.write("\n")
  

  




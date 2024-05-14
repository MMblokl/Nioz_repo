import sys
import numpy
import os

###############
#ARGUMENTS
###############
bins_dir = sys.argv[1] #The path to the dir containing all bins to be quantified.
unbinned_contigs = sys.argv[2] #The file location of the unbinned contigs file generated by find_residuals.py
salmon_quant = sys.argv[3] #The quant.sf file generated by using salmon quant generated by the salmon_quant.sh script.
readmapping = sys.argv[4] #The file showing the amount of unique mapping reads for each contig in the sample generated by get_read_mapping.sh.
sampleid = sys.argv[5]
outfile = sys.argv[6]


###################
#This script estimates the abundance based on two methods.
#These were originally methods #2 and #13 in the full list.

#Sum of read coverages in all contigs in a bin, divided by the total sum of
# all read coverages over the entire sample.
# This coverage is a value taken from the contig header, generated by metaSPAdes.
# bincoverage / total coverage

#The weighted average TPM from salmon is taken from all contigs in a bin.
# The weights are the lengths of the contigs. This is then divided by the total 
# weighted average.
#
# Weighted average TPM in bin / total weighted average TPM

contigdata = {}
bindata = {}

#Reads all the unbinned ids into a list
with open(f"{unbinned_contigs}", "r") as f:
  unbinned_ids = [x.strip(">").strip() for x in f.readlines()]


#Read the amount of reads mapped to a contig and the contiglength for each contig in the assembly.
with open(f"{readmapping}", "r") as f:
  line = f.readline()
  while line != "":
    line = line.split(" ")
    contigname = line[-1].strip()
    sub = contigname.split("_")
    contiglen = int(sub[3])
    contigcov = float(sub[-1])
    contigdata[contigname] = {'Length': contiglen, 'Mappedreads': int(line[-2]), 'Coverage': contigcov}
    line = f.readline()


#This reads the tpm of each contig from the salmon output and saves it to the correct contig in the "contigdata" dict.
with open(f"{salmon_quant}", "r") as f:
  f.readline()
  line = f.readline()
  while line != '':
    t = line.split("\t")
    contig = t[0]
    tpm = t[3]
    contigdata[contig]["tpm"] = float(tpm)
    line = f.readline()


#Put all the contigs in all bins into a temporary file that shows what bin a contig belongs to.
os.system("rm -f %s_quantify_temp.txt" % (sampleid))
os.system("""for bin in %s/*.fna; do cat $bin | egrep ">" | awk -v bin="$bin" '{print $1,bin}' >> %s_quantify_temp.txt; done""" % (bins_dir, sampleid))
with open(f"{sampleid}_quantify_temp.txt", "r") as f:
  line = f.readline()
  while line != "":
    line = line.split()
    contigname = line[0][1:]
    bin = line[-1].split("/")[-1].split(".")[0]
    try:
      bindata[bin].update({contigname: contigdata[contigname]})
    except KeyError:
      bindata[bin] = {contigname: contigdata[contigname]}
    line = f.readline()
os.system(f"rm -f {sampleid}_quantify_temp.txt")


#Here, the unbinned contigs get put into a "bin" to quantify this residual
#bin together with the rest.
bindata["unbinned"] = {}
unbinned_size = 0
for contigid in unbinned_ids:
  unbinned_cdat = contigdata[contigid]
  unbinned_size += unbinned_cdat["Length"]
  bindata["unbinned"].update({contigid: unbinned_cdat})


#Summing up totals and calculating ratios for the quantification.
bin_quantdata = {}
with open(f"{outfile}", "w") as o:
  o.write("bin\t")
  o.write("\t".join(["kmercov_weighted", "TPM_salm_weighted"]))
  o.write("\n")

  ########
  #Creating integers for the sum values used in each method.
  ###############################################################
  #The total reads in the sample
  total_reads = 0

  #Contig read coverage from metaSPAdes
  total_coverage = 0 #The total sum of all contig coverages in a sample, for method #2.
  
  tpm_weight_avg_total = 0 #The total sum of all weighted average TPMs of all bins, for method #13.
  ################################################################
  
  
  #Here, the bindata dict is looped through, which contains a dict for every contig in the bin,
  # with each datapoint saved per contig.
  for bin in bindata.keys():
    
    #########
    #Creating lists for summing up totals per bin and weights
    ###########################################
    #Getting the correct bin values.
    dat = bindata[bin]
    #A list that will contain all contig coverages for the current bin.
    bin_cov_contiglist = []
    #A list to contain all contig lengths in order to be used as weights.
    bin_contig_lengths = []
    #A list to contain all TPM values of all contigs in the bin.
    tpm_contig_list = []
    ###########################################
    
    ###########################################
    #Loop through all contigs in bin to sum and collect values per bin
    ###########################################
    for contig in dat.keys():
      contigdata = dat[contig] #The data of the current contig
      #Add the coverage to the bin coverage list.
      bin_cov_contiglist.append(contigdata["Coverage"])
      #Add the length to the bin contig lengths list.
      bin_contig_lengths.append(contigdata["Length"])
      #Add the contig TPM to the bin TPM list.
      tpm_contig_list.append(contigdata["tpm"])
    ###########################################

    #Coverage calculations
    bin_coverage = numpy.average(bin_cov_contiglist, weights=bin_contig_lengths) #The coverage of a bin calculated as the average of all contig coverages weighted by the contig length
    total_coverage += bin_coverage
    
    #tpm calculations
    tpm_avg_weighted = numpy.average(tpm_contig_list, weights=bin_contig_lengths)
    tpm_weight_avg_total += tpm_avg_weighted

    #Each calculated value is saved into a dict called "bin_quantdata" for dividing with the sample totals later.
    bin_quantdata[bin] = {"tpm_weighted": tpm_avg_weighted, \
    "bin_coverage": bin_coverage}
    

  #Final calculation of full percentages of each bin.
  for bin in bin_quantdata.keys():
    bindata = bin_quantdata[bin]
    
    #Weighted kmer coverage quant.
    coverage_percentage = (bindata["bin_coverage"]/total_coverage)*100
    
    #Weighted TPM quant.
    tpm_weighted_percentage = (bindata["tpm_weighted"]/tpm_weight_avg_total)*100
    
    o.write(f"{bin}\t{coverage_percentage}\t{tpm_weighted_percentage}\n")


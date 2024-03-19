#Complete script that makes a bunch of quantification estimates using different methods
import os
import glob
import numpy
import ast



for dir in glob.glob("./*/"):
  contigdata = {}
  bindata = {}
  id = dir.split("/")[1]

  #Reads all the unbinned ids into a list
  with open(f"{id}_unbinned.txt", "r") as f:
    unbinned_ids = [x.strip(">").strip() for x in f.readlines()]

  #This reads the amount of reads mapped to a contig and the contiglength for each contig in the assembly.
  with open(f"{id}_readmapping.txt", "r") as f:
    line = f.readline()
    while line != "":
      line = line.split(" ")
      contigname = line[-1].strip()
      sub = contigname.split("_")
      contiglen = int(sub[3])
      contigcov = float(sub[-1])
      contigdata[contigname] = {'Length': contiglen, 'Mappedreads': int(line[-2]), 'Coverage': contigcov}
      line = f.readline()

  
  #This reads the contig read depth for each contig
  with open(f"{id}/contig_depth.txt", "r") as f:
    line = f.readline()
    line = f.readline()
    while line != '':
      t = line.split(" ")
      depth = t[1].strip()
      contig = t[0].strip('"')
      contigdata[contig]["Depth"] = float(depth)
      line = f.readline()


  #This reads the tpm of each contig from the salmon output
  with open(f"{id}/salmon_quant/readbased_quant/quant.sf", "r") as f:
    f.readline()
    line = f.readline()
    while line != '':
      t = line.split("\t")
      contig = t[0]
      tpm = t[3]
      contigdata[contig]["tpm"] = float(tpm)
      line = f.readline()


  #Put all the contigs in all bins into a temporary file that shows what bin a contig belongs to.
  os.system("rm -f temp.txt")
  os.system("""for bin in ../binning/filtered_bins/%s/metabinner/*.fna; do cat $bin | egrep ">" | awk -v bin="$bin" '{print $1,bin}' >> temp.txt; done""" % id)
  with open("temp.txt", "r") as f:
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


  #Here, the unbinned contigs get put into a "bin" to quantify this residual
  #bin together with the rest.
  bindata["unbinned"] = {}
  unbinned_size = 0
  for contigid in unbinned_ids:
    unbinned_cdat = contigdata[contigid]
    unbinned_size += unbinned_cdat["Length"]
    bindata["unbinned"].update({contigid: unbinned_cdat})


  #Reads the estimated genomesize from the genomesizes.tab file generated
  # by the calc_genomesize.R script.
  genomesizes = {}
  with open(f"{id}/genomesize/genomesizes.tab", "r") as f:
    line = f.readline()
    while line != "":
      t = line.split(" ")
      bin = t[0].split("/")[-1].split(".")[0]
      size = float(t[-1].strip())
      genomesizes[bin] = size
      line = f.readline()
  genomesizes["unbinned"] = unbinned_size #This is a "genomesize" generated for the unbinned contigs, by taking their length and summing it up. This way the percentages of the bins don't get inflated by comparison.

  #Summing up totals and calculating ratios for the quantification.
  bin_quantdata = {}
  os.system(f"mkdir -p {id}/quantification_runs/")
  with open(f"{id}/quantification_runs/quant_table.tsv", "w") as o:
    o.write("bin\tTotal reads in bin/Total reads in sample\tWeighted average bin coverage/total bin coverage\tBin depth/total bin depth(avg)\tBin depth/Total bin depth(median)\tAdjusted reads/total adjusted reads(depth)(avg)\tAdjusted reads/total adjusted reads(depth)(med)\tAdjusted reads/Total adjusted reads(median)\tAdjusted reads/Total adjusted reads(average)\tAdjusted reads/Total adjusted reads(median)(inverse)\tAdjusted reads/Total adjusted reads(average)(inverse)\tTPM percentage(avg)\tTPM percentage(median)\tTPM percentage(weighted avg)\n")
    total_reads = 0 #The total reads in the sample
    
    gs_adjusted_total_med = 0 #The total amount of adjusted reads based on the ratio of reads mapped to each contig basepair.
    gs_adjusted_total_avg = 0 #The total reads adjusted avg.
    
    gs_i_adjusted_total_med = 0 #The same as the other reads adjusted by genomesize, although here we use the inverse of the genomesize, so division.
    gs_i_adjusted_total_avg = 0
    
    bd_avg_total = 0 #The sum of the averages of the contig depths in all bins.
    bd_med_total = 0 #The sum of the medians of the contig depths in all bins.
    
    bd_adj_total_avg = 0 #The sum of total adjusted reads based on the average depth of all contigs in bin.
    bd_adj_total_med = 0 #sum of adjusted reads based on depth median.
    
    total_coverage = 0 #The total coverage of all bins/MAGs
    
    tpm_avg_total = 0 #the total sum of all bin averages
    tpm_med_total = 0 #the total sum of all bin medians
    tpm_weight_avg_total = 0
    
    for bin in bindata.keys():
      binreads = 0 #The amount of mapped reads in the bin
      dat = bindata[bin] #A dict containing the data of all contigs in a bin
      rpbp_contiglist = []
      depth_pb = []
      
      bin_cov_contiglist = [] #A list containing all coverages of all contigs in the bin
      
      bin_contig_lengths = [] #A list to contain the lengths of each contig to use as weights
      
      tpm_contig_list = [] #A list filled with all tpm values of all contigs in the bin
      
      #Loop through all contigs in bin to sum and collect values per bin
      for contig in dat.keys():
        contigdata = dat[contig] #The data of the current contig
        binreads += contigdata["Mappedreads"]
        depth_pb.append(contigdata["Depth"]) #Append the contig depth to a list
        
        bin_cov_contiglist.append(contigdata["Coverage"])
        bin_contig_lengths.append(contigdata["Length"])
        
        #Rpbp: total mapped Reads Per contig Base Pair ratio
        contig_rpbp = contigdata["Mappedreads"]/contigdata["Length"] #The ratio of number of reads per basepair in the contig, can be seen as the number of reads mapped to the contig adjusted by the contiglength
        rpbp_contiglist.append(contig_rpbp) #The reads per contig basepair is put into a list, either the median or the average is used
        
        tpm_contig_list.append(contigdata["tpm"])
        
      
      #Calculations for read amount per basepair ratios
      contig_rpbp_avg = numpy.average(rpbp_contiglist) #The average of contig reads per basepair ratios
      contig_rpbp_med = numpy.median(rpbp_contiglist) #The median of contig reads per basepair ratios
      
      #Depth calculations
      contigdepth_avg = numpy.average(depth_pb)
      bd_avg_total += contigdepth_avg
      contigdepth_med = numpy.median(depth_pb)
      bd_med_total += contigdepth_med
      
      #Depth adjusted reads
      dep_adj_readamt_avg = binreads*contigdepth_avg
      bd_adj_total_avg += dep_adj_readamt_avg
      dep_adj_readamt_med = binreads*contigdepth_med
      bd_adj_total_med += dep_adj_readamt_med
      
      #Coverage calculations
      bin_coverage = numpy.average(bin_cov_contiglist, weights=bin_contig_lengths) #The coverage of a bin calculated as the average of all contig coverages weighted by the contig length
      total_coverage += bin_coverage
      
      #tpm calculations
      tpm_med = numpy.median(tpm_contig_list)
      tpm_med_total += tpm_med
      tpm_avg = numpy.average(tpm_contig_list)
      tpm_avg_total += tpm_avg
      tpm_avg_weighted = numpy.average(tpm_contig_list, weights=bin_contig_lengths)
      tpm_weight_avg_total += tpm_avg_weighted
      
      #Adjusted reads
      #Adjusted reads are the amount of mapped reads in the bin adjusted by the genomesize. The two versions are the median and average of the read to basepair ratio in the binned contigs.
      #The adjusted amount of reads based on the genomesize. If the median amount of reads mapped to eacj basepair in a contig is 2, then the adjusted reads is twice the number of basepairs in the genomesize.
      adjusted_reads_med = contig_rpbp_med*genomesizes[bin]
      gs_adjusted_total_med += adjusted_reads_med
      #The inverse
      adjusted_reads_med_i = contig_rpbp_med/genomesizes[bin]
      gs_i_adjusted_total_med += adjusted_reads_med_i
      
      #Avg version of adjusted reads
      adjusted_reads_avg = contig_rpbp_avg*genomesizes[bin]
      gs_adjusted_total_avg += adjusted_reads_avg
      #The inverse
      adjusted_reads_avg_i = contig_rpbp_avg/genomesizes[bin]
      gs_i_adjusted_total_avg += adjusted_reads_avg_i

      
      #Collecting each value calculated in a dict to match it to the correct bin
      bin_quantdata[bin] = {"bin_reads": binreads, \
      "bin_depth_avg": contigdepth_avg, \
      "bin_depth_med": contigdepth_med, \
      "adj_reads_dep_avg": dep_adj_readamt_avg, \
      "adj_reads_dep_med": dep_adj_readamt_med, \
      "tpm_med": tpm_med, \
      "tpm_avg": tpm_avg, \
      "tpm_weighted": tpm_avg_weighted, \
      "bin_coverage": bin_coverage, \
      "genomesize": genomesizes[bin], \
      "rpbp_ratio_avg": contig_rpbp_avg, \
      "rpbp_ratio_med": contig_rpbp_med, \
      "adjusted_read_amt_med": adjusted_reads_med, \
      "adjusted_read_amt_avg": adjusted_reads_avg, \
      "adjusted_read_amt_med_i": adjusted_reads_med_i, \
      "adjusted_read_amt_avg_i": adjusted_reads_avg_i}
      
     
      
      total_reads += binreads

      #Instead of just counting up the toal rpbp ratio, you use that ratio in comparison to the total reads in a bin
      # to see how much weight each contig should have. In this way, you could be able to estimate percentages of the contigs
      # instead of the total bins.
      
    #Final calculation of full percentages of each bin.
    for bin in bin_quantdata.keys():
      bindata = bin_quantdata[bin]
      
      #The bin_readratio, which is the amount of reads mapped divided by the total, as basic as it can get.
      bin_readratio = (bindata['bin_reads']/total_reads)*100
      
      #The bin_depthratio, which is basically the same but it uses the bin depth, which is basically read coverage.
      bin_depthratio_avg = (bindata["bin_depth_avg"]/bd_avg_total)*100
      bin_depthratio_med = (bindata["bin_depth_med"]/bd_med_total)*100
      
      #Adjusted readratios based on depths.
      depth_adjusted_readratio_avg = (bindata["adj_reads_dep_avg"]/bd_adj_total_avg)*100
      depth_adjusted_readratio_med = (bindata["adj_reads_dep_med"]/bd_adj_total_med)*100
      
      #Adjusted readratios, which is the percentage caculated with the adjusted read value instead.
      adjusted_readratio_med = (bindata["adjusted_read_amt_med"]/gs_adjusted_total_med)*100
      adjusted_readratio_avg = (bindata["adjusted_read_amt_avg"]/gs_adjusted_total_avg)*100
      
      #Adjusted readratios, with inversed genomesize instead.
      adjusted_readratio_med_i = (bindata["adjusted_read_amt_med_i"]/gs_i_adjusted_total_med)*100
      adjusted_readratio_avg_i = (bindata["adjusted_read_amt_med_i"]/gs_i_adjusted_total_avg)*100
      
      #Bin coverage divided by the sum of all bin coverages in the sample.
      coverage_percentage = (bindata["bin_coverage"]/total_coverage)*100
      
      #Tpm calculations
      tpm_med_percentage = (bindata["tpm_med"]/tpm_med_total)*100
      tpm_avg_percentage = (bindata["tpm_avg"]/tpm_avg_total)*100
      tpm_weighted_percentage = (bindata["tpm_weighted"]/tpm_weight_avg_total)*100
      
      o.write(f"{bin}\t{bin_readratio}\t{coverage_percentage}\t{bin_depthratio_avg}\t{bin_depthratio_med}\t{depth_adjusted_readratio_avg}\t{depth_adjusted_readratio_med}\t{adjusted_readratio_med}\t{adjusted_readratio_avg}\t{adjusted_readratio_med_i}\t{adjusted_readratio_avg_i}\t{tpm_avg_percentage}\t{tpm_med_percentage}\t{tpm_weighted_percentage}\n")
    




#the coverage for each MAG was calculated as the average of all contig coverages, weighted by their length. The relative abundance of MAGs in each metagenomic dataset was calculated as its coverage divided by the total coverage of all genomes 




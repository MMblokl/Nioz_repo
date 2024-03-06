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
      contiglen = int(contigname.split("_")[3])
      contigdata[contigname] = {'Length': contiglen, 'Mappedreads': int(line[-2])}
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
    o.write("bin\tTotal reads in bin/Total reads in sample\tTotal depth in bin/Total depth in sample\tAdjusted reads/Total adjusted reads(median)\tAdjusted reads/Total adjusted reads(average)\n")
    total_reads = 0 #The total reads in the sample
    total_depth = 0
    
    gs_adjusted_total_med = 0 #The total amount of adjusted reads based on the ratio of reads mapped to each contig basepair.
    gs_adjusted_total_avg = 0 #The total reads adjusted avg.
    
    for bin in bindata.keys():
      binreads = 0 #The amount of mapped reads in the bin
      bindepth = 0 #The total contig depth in the bin\
      dat = bindata[bin]
      rpbp_contiglist = []
      
      for contig in dat.keys():
        binreads += dat[contig]["Mappedreads"]
        bindepth += dat[contig]["Depth"]
        contig_rpbp = dat[contig]["Mappedreads"]/dat[contig]["Length"] #The ratio of number of reads per basepair in the contig
        rpbp_contiglist.append(contig_rpbp) #The reads per contig basepair is put into a list, either the median or the average is used
        
      
      #Calculations for read amount per basepair ratios
      contig_rpbp_avg = numpy.average(rpbp_contiglist) #The average of contig reads per basepair ratios
      contig_rpbp_med = numpy.median(rpbp_contiglist) #The median of contig reads per basepair ratios
      
      
      
      bin_quantdata[bin] = {"bin_reads": binreads, \
      "bin_depth": bindepth, \
      "genomesize": genomesizes[bin], \
      "rpbp_ratio_avg": contig_rpbp_avg, \
      "rpbp_ratio_med": contig_rpbp_med}
      
      #Adjusted reads are the amount of mapped reads in the bin adjusted by the genomesize. The two versions are the median and average of the read to basepair ratio in the binned contigs.
      #The adjusted amount of reads based on the genomesize. If the median amount of reads mapped to eacj basepair in a contig is 2, then the adjusted reads is twice the number of basepairs in the genomesize.
      adjusted_reads_med = contig_rpbp_med*bin_quantdata[bin]["genomesize"]
      gs_adjusted_total_med += adjusted_reads_med
      
      #Avg version of adjusted reads
      adjusted_reads_avg = contig_rpbp_avg*bin_quantdata[bin]["genomesize"]
      gs_adjusted_total_avg += adjusted_reads_avg
      
      bin_quantdata[bin]["adjusted_read_amt_med"] = adjusted_reads_med
      bin_quantdata[bin]["adjusted_read_amt_avg"] = adjusted_reads_avg
      
      total_reads += binreads
      total_depth += bindepth

      #Instead of just counting up the toal rpbp ratio, you use that ratio in comparison to the total reads in a bin
      # to see how much weight each contig should have. In this way, you could be able to estimate percentages of the contigs
      # instead of the total bins.
      
    #Final calculation of full percentages of each bin.
    for bin in bin_quantdata.keys():
      #The bin_readratio, which is the amount of reads mapped divided by the total, as basic as it can get.
      bin_readratio = (bin_quantdata[bin]['bin_reads']/total_reads)*100
      
      
      #The bin_depthratio, which is basically the same but it uses the bin depth, which is basically read coverage.
      bin_depthratio = (bin_quantdata[bin]["bin_depth"]/total_depth)*100
      
      #Adjusted readratios, which is the percentage caculated with the adjusted read value instead.
      adjusted_readratio_med = (bin_quantdata[bin]["adjusted_read_amt_med"]/gs_adjusted_total_med)*100
      adjusted_readratio_avg = (bin_quantdata[bin]["adjusted_read_amt_avg"]/gs_adjusted_total_avg)*100
      
      #Read coverage depth use
      
      o.write(f"{bin}\t{bin_readratio}\t{bin_depthratio}\t{adjusted_readratio_med}\t{adjusted_readratio_avg}\n")
    
    

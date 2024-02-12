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
  for contigid in unbinned_ids:
    bindata["unbinned"].update({contigid: contigdata[contigid]})


  genomesizes = {}
  #Reads the estimated genomesize from the genomesizes.tab file generated
  #by the calc_genomesize.R script.
  with open(f"{id}/genomesize/genomesizes.tab", "r") as f:
    line = f.readline()
    while line != "":
      t = line.split(" ")
      bin = t[0].split("/")[-1].split(".")[0]
      size = float(t[-1].strip())
      genomesizes[bin] = size
      line = f.readline()


  #Summing up totals and calculating ratios for the quantification.
  bin_quantdata = {}
  os.system(f"mkdir -p {id}/quantification_runs/")
  with open(f"{id}/quantification_runs/quant_table.tsv", "w") as o:
    o.write("bin\tTotal reads in bin/Total reads in sample\t\n")
    total_reads = 0 #The total reads in the sample
    
    for bin in bindata.keys():
      binreads = 0 #The amount of mapped reads in the bin
      dat = bindata[bin]
      rpbp_contiglist = []
      
      for contig in dat.keys():
        binreads += dat[contig]["Mappedreads"]
        contig_rpbp = dat[contig]["Mappedreads"]/dat[contig]["Length"] #The ratio of reads per basepair in the contig
        rpbp_contiglist.append(contig_rpbp) #The reads per contig basepair is put into a list, either the median or the average is used
      
      #Calculations for reads per basepair
      contig_rpbp_avg = numpy.average(rpbp_contiglist) #The average of contig reads per basepair ratios
      contig_rpbp_med = numpy.median(rpbp_contiglist) #The median of contig reads per basepair ratios
      
      bin_quantdata[bin] = {"bin_reads": binreads, \
      "genomesize": genomesizes[bin], \
      "rpbp_ratio_avg": contig_rpbp_avg, \
      "rpbp_ratio_med": contig_rpbp_med}

      total_reads += binreads

      #Instead of just counting up the toal rpbp ratio, you use that ratio in comparison to the total reads in a bin
      # to see how much weight each contig should have. In this way, you could be able to estimate percentages of the contigs
      # instead of the total bins.
      
    #Calculation
    for bin in bin_quantdata.keys():
      bin_readratio = (bin_quantdata[bin]['bin_reads']/total_reads)*100 #The percentage of mapped reads to a bin, divided by the total reads in the sample.
      
      #STILL NEED TO BE DIVIDED OR MULTIPLIED BY SOMETHING?
      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      rpbp_avg = (bin_quantdata[bin]["rpbp_ratio_avg"])
      rpbp_med = (bin_quantdata[bin]["rpbp_ratio_med"])
      
      trpbpt = (bin_quantdata[bin]['rpbp']/total_rpbp_ratio)*100
      
      o.write(f"{bin}\t{bin_readratio}\t{}\n")
    
    

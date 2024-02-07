#Complete script that makes a bunch of quantification estimates using different methods
import os
import glob
import numpy
import ast



for dir in glob.glob("./*/"):
  contigdata = {}
  bindata = {}
  id = dir.split("/")[1]
  
  
  #THIS NEEDS TO BE REPLACED WITH A GENOME SIZE ESTIMATOR
  #os.system(f"cat ~/binning/checkm/{id}/metabinner/storage/bin_stats.analyze.tsv > temp.txt")
  ##This part reads the genome size of a bin based on a report of checkm
  #with open(f"temp.txt", "r") as f:
  #  for line in f.readlines():
  #    genomesize = ast.literal_eval(line.split("\t")[-1].strip())['Genome size']
  #    bindata[line.split("\t")[0]] = {"Genome size": genomesize}
  
  
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
  

  #The quantification
  bin_quantdata = {}
  os.system(f"mkdir -p {id}/quantification_runs/")
  with open(f"{id}/quantification_runs/quant_table.tsv", "w") as o:
    o.write("bin\tTotal reads in bin/Total reads in sample\tAverage reads per basepair in a bin/Average reads per basepair in sample\n")
    total_reads = 0
    total_rpbp_ratio = 0
    
    for bin in bindata.keys():
      binreads = 0
      reads_per_basepair = 0 #The sum of the read to bp ratio of every contig, divided by the amount of contigs
      dat = bindata[bin]
      
      for contig in dat.keys():
        binreads += dat[contig]["Mappedreads"]
        reads_per_basepair += dat[contig]["Mappedreads"]/dat[contig]["Length"] #The ratio of reads per basepair in the contig
      rpbp = reads_per_basepair/len(dat.keys())
      bin_quantdata[bin] = {"bin_reads": binreads, "rpbp": rpbp}
      
      total_reads += binreads
      total_rpbp_ratio += rpbp
      
      
    
    #Calculation
    for bin in bin_quantdata.keys():
      o.write(f"{bin}\t{(bin_quantdata[bin]['bin_reads']/total_reads)*100}\t{(bin_quantdata[bin]['rpbp']/total_rpbp_ratio)*100}\n")
    
  #DATA IS HERE NOW WE JUST DO CALCULATIONS YES YES YES
    

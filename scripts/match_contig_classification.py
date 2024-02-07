import os
import re
import glob

ranks = ['Superkingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']


for dir in glob.glob("filtered_bins/*/*"): #Get directories here
  break
  os.system("rm temp.txt")
  os.system("""for bin in %s/*.f*; do cat $bin | egrep ">" | awk -v bin="$bin" '{print $1,bin}' >> temp.txt; done""" % dir) #Reads all contig ids from the bins and puts them in a file together with the name of the bin they came from
  contigdata = {}
  with open("temp.txt", 'r') as f:
    for d in f.readlines():
      dat = d.split(" ")
      contigdata[dat[0][1:]] = dat[1].split("/")[-1].strip() #Seperate the ">" from the contig ID
  with open(f"{dir.split('/')[1]}/CATnames.txt") as f, open(f"{dir}/bintaxdata.tsv", 'w') as o:
    o.write("ContigID\tbinname\tContig taxonomy\n") #Header
    for line in f.readlines()[1:]:
      linedat = line.split("\t")
      try:
        binid = linedat[0]
        binname = contigdata[binid]
        o.write(f'{binid}\t{binname}\t{";".join(linedat[5:]).strip()}\n')
      except:
        pass

for file in glob.glob("filtered_bins/*/*"):
  bindata = {}
  taxpercentages = {}
  with open(f"{file}/bintaxdata.tsv", "r") as f:
    for line in f.readlines()[1:]:
      line = line.strip().split("\t")
      if len(line) == 2:
        line.append("NA") #Sets the tax as "NA" if there was no found classification
      try:
        bindata[line[1]].append(line[2])
      except:
        bindata[line[1]] = [line[2]]
  for bin in bindata.keys():
    for tax in set(bindata[bin]):
      t = tax.split(";")
      t = list(filter(lambda a: a != "no support", t)) #Filters all occurances of "no support" from the tax
      savename = ";".join(t)
      if savename == '':
        savename = "NA"
      amt = bindata[bin].count(tax)
      try:
        taxpercentages[bin][savename] = amt
      except:
        taxpercentages[bin] = {savename: amt}
  for bin in taxpercentages.keys():
    total = sum(taxpercentages[bin].values())
    taxdict = {}
    for rank in ranks:
      ind = ranks.index(rank) #The index defining what taxonomic level the loop is at
      #Make a dict in which we take each value that is up to the current rank, this gets puts into that level in the dict,
      #with a value that indicates how many times this value is found in all of the keys in that bin.
      taxdict[rank] = {}
      for tax in taxpercentages[bin].keys():
        try:
          val = tax.split(";")[ind]
          try:
            taxdict[rank][val] += taxpercentages[bin][tax]
          except:
            taxdict[rank][val] = taxpercentages[bin][tax]
        except:
          pass
    with open(f"{file}/abundance.{bin}.tsv", "w") as o:
      o.write("Taxonomic Rank\tTaxonomy\tPercentage\n")
      for rank in taxdict.keys():
        for tax in taxdict[rank].keys():
          percentage = taxdict[rank][tax] / total
          o.write(f"{rank}\t{tax}\t{percentage}\n")
        remainder = 1 - sum(taxdict[rank].values()) / total #Calculates the remainder of the 100%
        o.write(f"{rank}\t(Remainder not classified up to this level)\t {remainder}\n")

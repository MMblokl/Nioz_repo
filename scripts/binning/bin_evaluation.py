import glob
import os

for x in glob.glob("filtered_bins/*/*"):
  data = x.split("/")
  bins = [x.split("/")[-1].strip(".fna") for x in glob.glob(f"{x}/*")]
  #os.system("bash bin_evaluation.sh")
  with open(f"gtdbtk/{data[1]}/{data[2]}/bintax.tsv", "r") as f, open(f"gtdbtk/{data[1]}/{data[2]}/final_tax.tsv", "w") as o:
    o.write("BinID\tClassification\tLevel\n")
    taxbins = []
    for l in f.readlines():
      splitline = l.split("\t")
      taxbins.append(splitline[0])
      taxonomy = splitline[1].split(";")[-1].strip()
      for tax in splitline[1].split(";")[::-1]:
        if len(tax.strip()) != 3:
          taxonomy = tax.strip()
          break
      #o.write(f"{splitline[0]}\t{taxonomy}\t{taxonomy[0]}\n")
    not_identified = [x for x in bins if x not in taxbins]
    print(not_identified)
    #for bin in not_identified:
    #  o.write(f"{bin}\tNA\tNA\n")
  

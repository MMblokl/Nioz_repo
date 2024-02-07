import glob
import os
import re


mockids = ["SRR17380113", "SRR17380114", "SRR17380115", "SRR17380116", "SRR17380117", "SRR17380118", "SRR17380119", "SRR17380120", "SRR17380121", "SRR17380122"]
summaries = glob.glob("gtdbtk/*/*")


stats = {}

for s in summaries:
  print(s)
  for id in mockids:
    if id in s:
      refset = "~/mock_references/"
      break
    else:
      refset = "~/cami_marine/genomes/"
  bins_unspecific = 0 #bins too unspecific to be used
  bins_found_genus = 0 #bins that were found in the reference list
  bins_found_species = 0
  bins_nofound = 0 #bins NOT found in the reference list
  with open(f"{s}/final_tax.tsv", "r") as f:
    info = f.readlines()[1:]
    for dat in info:
      dat = dat.split("\t")
      if "_" in dat[1]:
        dat[1] = re.sub("_[A-Z]{1,1}", "", dat[1]) #Remove useless appendixes from the species name
      if " sp" in dat[1]:
        dat[1] = re.sub("sp[0-9]{0,}", "", dat[1])
        dat[2] = "g"
      if dat[2].strip() not in ["s", "g"]:
        bins_unspecific += 1
      else:
        dat[1] = dat[1].replace(" ", ".")
        os.system(f"ls {refset} | egrep {dat[1]} > result")
        with open("result", "r") as g:
          output = g.readlines()
          if not bool(output):
            if dat[2].strip() == "g":
              bins_nofound += 1
            else:
              dat[1] = re.sub("\.[A-z]{0,}", "", dat[1])
              os.system(f"ls {refset} | egrep {dat[1]} > result")
              with open("result", "r") as q:
                out2 = q.readlines()
                if bool(out2):
                  bins_found_genus += 1
          elif dat[2].strip() == "s":
            bins_found_species += 1
          else:
            bins_found_genus += 1
  stats[s] = [bins_found_species, bins_found_genus, bins_nofound, bins_unspecific]
with open("bin_stats2.tsv", "w") as f:
  f.write("Sample\tTool\tSpecies found in reference\tGenus found in reference\tNothing found in reference\tBin too unspecific\n")
  for tool in stats.keys():
    data = stats[tool]
    f.write(f"{tool.split('/')[1]}\t{tool.split('/')[2]}\t{data[0]}\t{data[1]}\t{data[2]}\t{data[3]}\n") #Terrible line

#for x in [x for x in mock if "plasmid" not in x]:
#  x = x.split("/")[-1].split("_")[0:-1]
#  x = ' '.join(x)

  

import glob
import ast
import os
import sys

#Arguments:

checkm_file = sys.argv[1] #The input file
cutoff_comp = sys.argv[2] #Cutoff for completeness
cutoff_cont = sys.argv[3] #Cutoff for contamination
bin_dir = sys.argv[4] #Dir with orginal bins
filt_bin_dir = sys.argv[5] #Dir with the final filtered bins which passed the cutoff

#The bin stats are written into a file that both shows the bin stats
# in the way it was used in the report. The file also acts as a flag
# to signal the end of the filter process each sample.
with open(checkm_file, "r") as f, open(f"{filt_bin_dir}/bin_stats.tsv", "w") as o:
  prefilt_binamt = 0
  unfilt_binamt = 0
  total_comp = 0.0
  total_cont = 0.0
  line = f.readline()
  while line != '':
    t = line.split("\t")
    bindata = ast.literal_eval(t[1]) #Puts the checkm data into a dict
    completeness = bindata["Completeness"]
    contamination = bindata["Contamination"]
    prefilt_binamt += 1
    #This triggers if the bin does not reach the cutoff AND is the contamination is not 0.0.
    # If the contamination reaches 0.0 in checkM the completeness is also 0.0.
    # This would otherwise pass the contamination filter which would mean that
    # bin does not get filtered out, which would not be good.
    if completeness > float(cutoff_comp) or (contamination < float(cutoff_cont) and contamination != 0.0):
      unfilt_binamt += 1
      total_comp += completeness
      total_cont += contamination
      #The bin file is copied to a filtered bin directory so that the original bins are still there and not moved.
      os.system(f"cp -n {bin_dir}/{t[0]}.fna {filt_bin_dir}")
    line = f.readline()
  o.write("Bin amount\tBin amount after filtering\tAvarage completeness\tAvarage contamination\n")
  o.write(f"{prefilt_binamt}\t{unfilt_binamt}\t{total_comp/unfilt_binamt}\t{total_cont/unfilt_binamt}")




#Old code \/

#for f in files:
#  dirs = f.split("/")
#  #os.system(f"mkdir -p filtered_bins/{dirs[1]}/{dirs[2]}")
#  with open(f, "r") as t:
#    prefilter_binamt = 0
#    unfiltered_binamt = 0
#    total_comp = 0.0
#    total_cont = 0.0
#    for line in t.readlines():
#      prefilter_binamt += 1
#      t2 = line.split("\t")
#      data = ast.literal_eval(t2[1])
#      if data["Completeness"] > 20.0 or (data["Contamination"] < 15.0 and data["Contamination"] != 0.0):
#        unfiltered_binamt += 1
#        total_comp += data["Completeness"]
#        total_cont += data["Contamination"]
#        os.system(f"cp -n {dirs[1]}/{dirs[2]}/{bins_dir[dirs[2]]}/{t2[0]}.{bins_extension[dirs[2]]} filtered_bins/{dirs[1]}/{dirs[2]}")
#  stats[f"{dirs[1]}/{dirs[2]}"] = [prefilter_binamt, unfiltered_binamt, total_comp/unfiltered_binamt, total_cont/unfiltered_binamt, data["# markers"]]#
#####
#
#with open("bin_stats.tsv", "w") as f:
##  f.write("ID\tBinner\tBin amount\tBin amount after filtering\tAvarage completeness\tAvarage contamination\tTotal found marker sequences\n")
#  for x in stats.keys():
#    x2 = x.split("/")
#    data = stats.get(x)
#    f.write(f"{x2[0]}\t{x2[1]}\t{data[0]}\t{data[1]}\t{data[2]}\t{data[3]}\t{data[4]}\n")

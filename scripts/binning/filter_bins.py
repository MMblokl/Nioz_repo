import glob
import ast
import os

bins_dir = {'concoct': 'bins', 'metawrap': 'binsABC', 'metabinner': 'metabinner_res/ensemble_res/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ensemble_3logtrans/addrefined2and3comps/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/', "multirunset1": "bins", "multirunset2": "bins", "multirunset3": "bins"}
bins_extension = {'concoct': 'fa', "metawrap": 'fa', "metabinner": 'fna', "multirunset1": "fa", "multirunset2": "fa", "multirunset3": "fa"}


files = glob.glob("checkm/*/*/storage/bin_stats_ext.tsv")

stats = {}


for f in files:
  dirs = f.split("/")
  os.system(f"mkdir -p filtered_bins/{dirs[1]}/{dirs[2]}")
  with open(f, "r") as t:
    prefilter_binamt = 0
    unfiltered_binamt = 0
    total_comp = 0.0
    total_cont = 0.0
    for line in t.readlines():
      prefilter_binamt += 1
      t2 = line.split("\t")
      data = ast.literal_eval(t2[1])
      if data["Completeness"] > 20.0 or (data["Contamination"] < 15.0 and data["Contamination"] != 0.0):
        unfiltered_binamt += 1
        total_comp += data["Completeness"]
        total_cont += data["Contamination"]
        os.system(f"cp -n {dirs[1]}/{dirs[2]}/{bins_dir[dirs[2]]}/{t2[0]}.{bins_extension[dirs[2]]} filtered_bins/{dirs[1]}/{dirs[2]}")
  stats[f"{dirs[1]}/{dirs[2]}"] = [prefilter_binamt, unfiltered_binamt, total_comp/unfiltered_binamt, total_cont/unfiltered_binamt, data["# markers"]]


with open("bin_stats.tsv", "w") as f:
  f.write("ID\tBinner\tBin amount\tBin amount after filtering\tAvarage completeness\tAvarage contamination\tTotal found marker sequences\n")
  for x in stats.keys():
    x2 = x.split("/")
    data = stats.get(x)
    f.write(f"{x2[0]}\t{x2[1]}\t{data[0]}\t{data[1]}\t{data[2]}\t{data[3]}\t{data[4]}\n")
  


print(stats)

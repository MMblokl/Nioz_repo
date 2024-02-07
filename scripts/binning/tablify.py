import glob
import pandas

samples = glob.glob("*.tsv")
data = {}

for sample in samples:
  file = open(f"{sample}")
  data[sample] = {}
  for line in file.readlines():
    data[sample][line.strip().split("\t")[1]] = line.split(" ")[0]

data = pandas.DataFrame(data=data)
data.to_csv("CAMI_counts.csv")

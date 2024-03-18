import sys

#Arguments
quant_file = sys.argv[1]
true_quants = sys.argv[2]
classification_file = sys.argv[3]
outfile = sys.argv[4]



classifications = {}
#Read the classifications of genus and species level into a dict to be used for matching the true and estimated classifications
with open(f"{classification file}", "r") as f:
	f.readline()
	line = f.readline()
	while line != "":
		t = line.strip().split("\t")
		species = t[-1]
		genus = t[-2]
		bin = t[0][0:-4] #THIS ONE MIGHT NOT WORK
		classifications[bin] = (genus, species)
		line = f.readline()


true_quantification = {}
#Read the true percentages of the quantifications from the true_quants file
with open(f"{true_quants}", "r") as f:
	f.readline()
	line = f.readline()
	while line != "":
		t = line.strip().split(",")
		quant = float(t[-1]) #The quantification as a percentage
		genomename = t[0].strip('"')
		true_quantification[genomename] = quant
		line = f.readline()

with open(f"{quant_file}", "r") as f, open(f"{outfile}", "r") as o:
	line = f.readline()
	headers = [x for x in line.strip().split("\t")]
	line = f.readline()
	while line != "":
		t = line.strip().split("\t")
		bin = t[0]
		true_quant = true_quantification[bin]
		quants = t[1::]
		#Now we have to match the classifications with the true classifications and decide where to output them
		for quant in range(0,len(headers)): #HERE, WE LOOP TROUGH ALL THE QUANTIFICATIONSS
			pass

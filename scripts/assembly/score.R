#This script is awful, but it works, ok.
#The scores are outputted into the terminal.
scores = list(c(0,0,0,0,0), c(0,0,0,0,0), c(0,0,0,0,0))  #The list of the final scores
names(scores) = c("idba", "megahit", "spades") #Give toolnames to the scores
#The list contains three sublists for each tool, containing 5 scores belonging the evaluation metrics
#in the following order: Genome_fraction, Duplication_ratio, Misassemblies, Mismatch_per_100kb, NGA50


#Get the filenames of the files containing the evaluation metrics
files_noref <- list.files(path="assembly/quast_evals/", pattern = "*_noref.csv")
files_ref <- list.files(path="assembly/quast_evals/", pattern = "*_ref.csv")


for (f in files_noref[1:10]){
  temp <- read.csv(paste("~/assembly/quast_evals/", f, sep = ''), row.names=1)
  #Genome fraction
  tc = c(temp$Genome_fraction) #Create a temporary list for the values in the table.
  names(tc) = rownames(temp) #Give names to the values in list "tc", the names of the tools
  tc = sort(tc) # sort from highest to lowest, index 1 is the lowest and 3 the highest.
  scores[names(tc)[3]][[1]][1] = scores[names(tc)[3]][[1]][1] + 3 #Best tool gets 3 points
  scores[names(tc)[2]][[1]][1] = scores[names(tc)[2]][[1]][1] + 2 #Middle tool gets 2 points
  scores[names(tc)[1]][[1]][1] = scores[names(tc)[1]][[1]][1] + 1 #Lowest tool gets 1 point.
  #Duplication ratio
  tc = c(temp$Duplication_ratio)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][2] = scores[names(tc)[1]][[1]][2] + 3
  scores[names(tc)[2]][[1]][2] = scores[names(tc)[2]][[1]][2] + 2
  scores[names(tc)[3]][[1]][2] = scores[names(tc)[3]][[1]][2] + 1
  #Misassemblies
  tc = c(temp$Misasseblies)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][3] = scores[names(tc)[1]][[1]][3] + 3
  scores[names(tc)[2]][[1]][3] = scores[names(tc)[2]][[1]][3] + 2
  scores[names(tc)[3]][[1]][3] = scores[names(tc)[3]][[1]][3] + 1
  #Mismatch per 100 kb
  tc = c(temp$mismatch_per_100kb)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][4] = scores[names(tc)[1]][[1]][4] + 3
  scores[names(tc)[2]][[1]][4] = scores[names(tc)[2]][[1]][4] + 2
  scores[names(tc)[3]][[1]][4] = scores[names(tc)[3]][[1]][4] + 1
  #NGA50
  tc = c(temp$NGA50)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[3]][[1]][5] = scores[names(tc)[3]][[1]][5] + 3
  scores[names(tc)[2]][[1]][5] = scores[names(tc)[2]][[1]][5] + 2
  scores[names(tc)[1]][[1]][5] = scores[names(tc)[1]][[1]][5] + 1
}
print(scores) #These are the scores for the CAMI dataset with NO reference provided.

scores = list(c(0,0,0,0,0), c(0,0,0,0,0), c(0,0,0,0,0))
names(scores) = c("idba", "megahit", "spades")
for (f in files_noref[11:20]){
  temp <- read.csv(paste("~/assembly/quast_evals/", f, sep = ''), row.names=1)
  #Genome fraction
  tc = c(temp$Genome_fraction) #Create a temporary list for the values in the table.
  names(tc) = rownames(temp) #Give names to the values in list "tc", the names of the tools
  tc = sort(tc) # sort from highest to lowest, index 1 is the lowest and 3 the highest.
  scores[names(tc)[3]][[1]][1] = scores[names(tc)[3]][[1]][1] + 3 #Best tool gets 3 points
  scores[names(tc)[2]][[1]][1] = scores[names(tc)[2]][[1]][1] + 2 #Middle tool gets 2 points
  scores[names(tc)[1]][[1]][1] = scores[names(tc)[1]][[1]][1] + 1 #Lowest tool gets 1 point.
  #Duplication ratio
  tc = c(temp$Duplication_ratio)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][2] = scores[names(tc)[1]][[1]][2] + 3
  scores[names(tc)[2]][[1]][2] = scores[names(tc)[2]][[1]][2] + 2
  scores[names(tc)[3]][[1]][2] = scores[names(tc)[3]][[1]][2] + 1
  #Misassemblies
  tc = c(temp$Misasseblies)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][3] = scores[names(tc)[1]][[1]][3] + 3
  scores[names(tc)[2]][[1]][3] = scores[names(tc)[2]][[1]][3] + 2
  scores[names(tc)[3]][[1]][3] = scores[names(tc)[3]][[1]][3] + 1
  #Mismatch per 100 kb
  tc = c(temp$mismatch_per_100kb)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][4] = scores[names(tc)[1]][[1]][4] + 3
  scores[names(tc)[2]][[1]][4] = scores[names(tc)[2]][[1]][4] + 2
  scores[names(tc)[3]][[1]][4] = scores[names(tc)[3]][[1]][4] + 1
  #NGA50
  tc = c(temp$NGA50)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[3]][[1]][5] = scores[names(tc)[3]][[1]][5] + 3
  scores[names(tc)[2]][[1]][5] = scores[names(tc)[2]][[1]][5] + 2
  scores[names(tc)[1]][[1]][5] = scores[names(tc)[1]][[1]][5] + 1
}
print(scores) #These are the scores for the mock community dataset with NO reference provided.

scores = list(c(0,0,0,0,0), c(0,0,0,0,0), c(0,0,0,0,0))
names(scores) = c("idba", "megahit", "spades")
for (f in files_ref[1:10]){
  temp <- read.csv(paste("~/assembly/quast_evals/", f, sep = ''), row.names=1)
  #Genome fraction
  tc = c(temp$Genome_fraction) #Create a temporary list for the values in the table.
  names(tc) = rownames(temp) #Give names to the values in list "tc", the names of the tools
  tc = sort(tc) # sort from highest to lowest, index 1 is the lowest and 3 the highest.
  scores[names(tc)[3]][[1]][1] = scores[names(tc)[3]][[1]][1] + 3 #Best tool gets 3 points
  scores[names(tc)[2]][[1]][1] = scores[names(tc)[2]][[1]][1] + 2 #Middle tool gets 2 points
  scores[names(tc)[1]][[1]][1] = scores[names(tc)[1]][[1]][1] + 1 #Lowest tool gets 1 point.
  #Duplication ratio
  tc = c(temp$Duplication_ratio)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][2] = scores[names(tc)[1]][[1]][2] + 3
  scores[names(tc)[2]][[1]][2] = scores[names(tc)[2]][[1]][2] + 2
  scores[names(tc)[3]][[1]][2] = scores[names(tc)[3]][[1]][2] + 1
  #Misassemblies
  tc = c(temp$Misasseblies)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][3] = scores[names(tc)[1]][[1]][3] + 3
  scores[names(tc)[2]][[1]][3] = scores[names(tc)[2]][[1]][3] + 2
  scores[names(tc)[3]][[1]][3] = scores[names(tc)[3]][[1]][3] + 1
  #Mismatch per 100 kb
  tc = c(temp$mismatch_per_100kb)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][4] = scores[names(tc)[1]][[1]][4] + 3
  scores[names(tc)[2]][[1]][4] = scores[names(tc)[2]][[1]][4] + 2
  scores[names(tc)[3]][[1]][4] = scores[names(tc)[3]][[1]][4] + 1
  #NGA50
  tc = c(temp$NGA50)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[3]][[1]][5] = scores[names(tc)[3]][[1]][5] + 3
  scores[names(tc)[2]][[1]][5] = scores[names(tc)[2]][[1]][5] + 2
  scores[names(tc)[1]][[1]][5] = scores[names(tc)[1]][[1]][5] + 1
}
print(scores) #These are the scores for the CAMI dataset with reference provided.

scores = list(c(0,0,0,0,0), c(0,0,0,0,0), c(0,0,0,0,0))
names(scores) = c("idba", "megahit", "spades")
for (f in files_ref[11:20]){
  temp <- read.csv(paste("~/assembly/quast_evals/", f, sep = ''), row.names=1)
  #Genome fraction
  tc = c(temp$Genome_fraction) #Create a temporary list for the values in the table.
  names(tc) = rownames(temp) #Give names to the values in list "tc", the names of the tools
  tc = sort(tc) # sort from highest to lowest, index 1 is the lowest and 3 the highest.
  scores[names(tc)[3]][[1]][1] = scores[names(tc)[3]][[1]][1] + 3 #Best tool gets 3 points
  scores[names(tc)[2]][[1]][1] = scores[names(tc)[2]][[1]][1] + 2 #Middle tool gets 2 points
  scores[names(tc)[1]][[1]][1] = scores[names(tc)[1]][[1]][1] + 1 #Lowest tool gets 1 point.
  #Duplication ratio
  tc = c(temp$Duplication_ratio)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][2] = scores[names(tc)[1]][[1]][2] + 3
  scores[names(tc)[2]][[1]][2] = scores[names(tc)[2]][[1]][2] + 2
  scores[names(tc)[3]][[1]][2] = scores[names(tc)[3]][[1]][2] + 1
  #Misassemblies
  tc = c(temp$Misasseblies)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][3] = scores[names(tc)[1]][[1]][3] + 3
  scores[names(tc)[2]][[1]][3] = scores[names(tc)[2]][[1]][3] + 2
  scores[names(tc)[3]][[1]][3] = scores[names(tc)[3]][[1]][3] + 1
  #Mismatch per 100 kb
  tc = c(temp$mismatch_per_100kb)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[1]][[1]][4] = scores[names(tc)[1]][[1]][4] + 3
  scores[names(tc)[2]][[1]][4] = scores[names(tc)[2]][[1]][4] + 2
  scores[names(tc)[3]][[1]][4] = scores[names(tc)[3]][[1]][4] + 1
  #NGA50
  tc = c(temp$NGA50)
  names(tc) = rownames(temp)
  tc = sort(tc)
  scores[names(tc)[3]][[1]][5] = scores[names(tc)[3]][[1]][5] + 3
  scores[names(tc)[2]][[1]][5] = scores[names(tc)[2]][[1]][5] + 2
  scores[names(tc)[1]][[1]][5] = scores[names(tc)[1]][[1]][5] + 1
}
print(scores) #These are the scores for the mock community dataset with reference provided.

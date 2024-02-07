args = commandArgs(trailingOnly = TRUE)

#The script takes 2 arguments:
#1: The path to the directory containing the .histo files
#2: The name of the output file

files = list.files(path=args[1], pattern="*.histo", full.names=TRUE, recursive=FALSE)

breakpoint <- "Word" #This is a random string to act as a catch

estimates = c()

for (x in files){
  breakpoint <- "Word" #Reinstate the catch at the start of the loop
  
  t <- read.table(x)
  for (row in 1:100){
    val <- t[row, 2]
    if(t[row + 1, 2] > val) { #Check if the next value is higher than the current
      breakpoint <- row #Set the breakpoint as next row, which will omit the current value and under from the estimation
      break
    }
  }
  #If the end was reached without finding a peak this is a catch
  if(breakpoint == "Word"){
    breakpoint <- 2
  }
  temp <- t[breakpoint:nrow(t),]
  max <- temp[which.max(temp$V2),1]
  total_kmer <- sum(as.numeric(t[breakpoint:nrow(t),1]*t[breakpoint:nrow(t),2]))/max
  #This part catches any false peak. Sometimes the disctribution does not look good enough
  #and will result in it finding a false peak very far back onto the dataset.
  #This catch will make it only take out the first datapoint and estimate the genome size with that.
  if(total_kmer < 10000){
    breakpoint <- 2
    temp <- t[breakpoint:nrow(t),]
    max <- temp[which.max(temp$V2),1]
    total_kmer <- sum(as.numeric(t[breakpoint:nrow(t),1]*t[breakpoint:nrow(t),2]))/max
  }
  estimates=append(estimates, total_kmer)
}
names(estimates) = files #Add the bin file name to each estimate

write.table(estimates, file = args[2])

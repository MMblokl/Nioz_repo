#!bin/bash/

#Arguments:
#1: The sampleid
#2: the contigs used for binning
#3: The forward reads
#4: The reverse reads
#5: The ouput directory

#Load the environment. This needs to be changed to whatever you would use to use salmon on your setup.
module load salmon/1.10.1


  
mkdir -p $5/index

salmon index -p 16 -t $2 -i $5/index
salmon quant -i $5/index/ --libType IU -1 $3 -2 $4 -o $5 --meta -p 16


#This one ended up not being used
#salmon quant -p 16 --libType IU --output $5/alignment_quant -a SORTED BAM FILE -t $2

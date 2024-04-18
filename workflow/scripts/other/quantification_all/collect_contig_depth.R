args = commandArgs(trailingOnly = TRUE)

#arguments:
#1: mb2_master_depth file location for the correct sample
#2: The id of the sample, used to collect the correct contig read depth.
#3: Output file path

df = read.delim(args[1], row.names=1)

#We get the rowname that contains the sample id
col = grep(args[2], colnames(df))
name = colnames(df)[col]

depth = df[name]

write.table(depth, file=args[3])
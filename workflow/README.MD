##Config
Before running the workflow, make sure that you have the config configured
to your liking, and that all your samples are accessible in the sample
directory given in the config.

It is very important that the path to this directory is accessible from the directory where you run snakemake from.
Since some files will be read through python, a "~/directory" might not work.


##Reads
The forward and reverse reads must be ordered as such:
$SAMPLE_1.fastq for the forward facing reads.
$SAMPLE_2.fastq for the reverse facing reads.

These reads must be present in the directory "reads/", the full dirpath of which
can be changed in the config.



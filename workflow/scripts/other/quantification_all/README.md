## README for running every single quantification method.
The scripts in this directory generate the results for every quantification
method tested during the project.

## How to use
The script quant_runall.sh runs every quantification method on the results of
the snakemake workflow.
The complete output of the workflow up until the classifications.csv files from
GTDB-TK are required.

All files should be left in the same configuration as the workflow put them in.

## NOTE
It is required for the python package numpy to be available from the environment
you run the script from.


### True abundances
If you wish to also generate the absolute deviation data with true abundances,
a single line in the "quant_runall.sh" script must be altered.
On line 34, the script "quant_check.py" can be run if this line is uncommented.
Here, the part of the line "PATH_TO_ABUNDANCE_DIR_GOES_HERE/" requires one to
make a directory containing true abundance csv files which will be used to compare
the quantifications.

Making the true abundance directory.
The directory should contain one file for every ID, replicate or sample.
If the workflow was used on a dataset with 10 samples, 10 files need to be in
this true abundance directory, the filenames matching the IDs that were user-specified
in the workflow config.
For example:
[USER]$ ls PATH_TO_ABUNDANCE_DIR_GOES_HERE/
ID1.csv ID2.csv ID3.csv etc...

The files should contain comma seperated values of the organisms present in the sample,
and the true abundance of this organism is this manner:
"Rhodothermus_marinus_SG05JP17-172_genomic.fasta",0.0020723963118554
"Rhodothermus_marinus_DSM_4252_genomic.fasta",0.135690899386961
"Vibrio_nigripulchritudo_str_SFn1_genomic.fasta",0.565908359836479
"T-232_S7_contigs.fasta",0.0226942413512745
"Thermococcus_gammatolerans_EJ3_genomic.fasta",0.0332904937979786

It does not matter if you add the ".fasta" part as this is unimportant.
As long as, in the first column, the name of the species can be found like so:
"Thermococcus_gammatolerans",5

This is the bare minimum requirement for the script to match the true abundance with
the classifications from GTDBTK.

Example files will be left in the same repository directory as this README.

## Running the script.
[USER]$ bash quant_runall.sh PROJECT_LOCATION

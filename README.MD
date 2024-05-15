## Important
On certain servers, GTDB-TK might not work with more than 2 jobs runnin parralel at once.
This is because GTDB-TK loads the entire database into the working memory which can cause issues on clusters.
To avoid issues with this, make sure to not run more than two jobs.

Make sure to setup all tools by following the installation guide.
If the tools are already installed, locate the environments for said tools and add the load command into the wrapper scripts.

## Running the workflow.
snakemake --configfile=config.yaml -j 2 --cores * all


## Config
Before running the workflow, make sure that you have the config configured
to your liking, and that all your samples are accessible in the sample
directory given in the config.

It is very important that the path to this directory is accessible from the directory where you run snakemake from.
Since some files will be read through python, a "~/directory" might not work.


## Reads
The forward and reverse reads must be ordered as such:
$SAMPLE_1.fastq for the forward facing reads.
$SAMPLE_2.fastq for the reverse facing reads.

These reads must be present in the directory "reads/", the full dirpath of which
can be changed in the config.

## Programs and packages
The following is a list of programs and packages required to run the workflow.
Read the installation guide for more info.
Make sure the workflow is run in an environment with the following python packages installed:

### python modules:
  - numpy

### List of tools:
- metaSPAdes
- BBmap
- SAMtools
- MetaBinner: This tool needs to be installed in a different environment than
              the other programs due to package conflicts.
              Make sure this environment is loaded in the "mbinner.wrap" script.
              MetaBinner can be installed via conda or mamba. More information
              can be found on the MetaBinner github at: https://github.com/ziyewang/MetaBinner
- CheckM:     This program can also be used via a different environment. Just add
              line to load the environment into the "checkm.wrap" script and replace
              the old one.
- GTDB-TK:    Just like MetaBinner, GTDB-TK can most likely not be installed on the
              same environment as the rest of the programs. Make sure the environment
              GTDB-TK is installed on is loaded in the "gtdbtk.wrap" script.
- Salmon:     This tool needs to be installed into either a seperate environment or
              can be installed onto the main working environment. If the tool is installed
	            on a separate environment, make sure to add the line to load said environment in
              the "salmon.wrap" script.


Make sure that all tools, excluding GTDB-TK and MetaBinner, are accessible via
PATH so that snakemake can run them like normal.

GTDB-TK and MetaBinner use wrapper scripts to run, make sure to add the line used
for loading their respective environments into these scripts.

Again, GTDB-TK WILL crash if more than 1-2 instances are run due to how it loads the database into the memory.
If you wish to run the tool all in one go, make sure to only allow 1-2 jobs to run at a time.

If you add more jobs, the workflow will work up until the gtdb-tk classification rules.
Just re-run the workflow and it will continue from where it left off, just make sure to remove the unfunished gtdb-tk runs.

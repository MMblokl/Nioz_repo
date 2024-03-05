##Config
Before running the workflow, make sure that you have the config configured
to your liking, and that all your samples are accessible in the sample
directory given in the config.

It is very important that the path to this directory is accessible everywhere on
the system. "~/dirname" will likely not work as the files are read through python.


##Reads
The forward and reverse reads must be ordered as such:
$SAMPLE_1.fastq for the forward facing reads.
$SAMPLE_2.fastq for the reverse facing reads.

These reads must be present in the directory "reads/", the full dirpath of which
can be changed in the config.


##CAT/BAT
Contig/Bin Annotation Tool uses a database in order to classify contigs and bins.
If you already have this database prepared please create a link pointing to specific parts of that database
These should be placed in a directory named CAT_database inside the workflow folder.

  ln -d -s ~/CAT_database_15-11-2023/CAT_database.2023-11-15/ CAT_database/CAT_database
  ln -d -s ~/CAT_database_15-11-2023/CAT_taxonomy.2023-11-15/ CAT_database/CAT_taxonomy

If there is no database yet, please use the CAT prepare and link to this new database instead.

  CAT prepare --fresh -o ./CAT_database

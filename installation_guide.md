## Installation guide.

AFTER INSTALLING ALL TOOLS:
Make sure to add the environment load lines into the .wrap scripts in workflow/scripts/
The line to load the environment should be replaced by the new one.

If you want to install samtools, metaSPAdes and BBMap via apt install, make sure to add the "universe" repository to APT.
This can be line with this command: sudo add-apt-repository -r universe

If you do not have access to apt install, make sure to link the bin of these tools to PATH so that they are accessible by snakemake.
These tools are only accessible by snakemake if they are linked in the PATH.
If the tools are installed in separate conda environments, they cannot be linked like the other tools.
If they are installed in one conda environment, just simply run the workflow in that environment, given that snakemake is also installed.

## Wrapper scripts
Certain tools might need you to install them via a separate conda environment.
Make sure to add the environment load command into the wrapper scripts for the following tools.

- MetaBinner
- CheckM
- GTDB-TK

If these tools are also installed on the same environment as the others or are accessable via PATH, it should run fine given they function properly.
Just leave the environment load command space empty in the wrapper scripts. This is already the case on default.

### snakemake
The easiest way to install snakemake is via apt-install, but conda works as well.
Make sure to NOT install MetaBinner in the same directory as snakemake

### metaSPAdes.
metaSPAdes can be installed by installing the SPAdes package via apt install.
It can also be installed with the binaries through github.
Go to the github and install the binaries for SPAdes at: https://github.com/ablab/spades
Make sure to have python 3.8+ installed in your running environment.
Link the binaries to the SPAdes to your PATH using the following line. This is temporary and will revert when you exit the machine.

export PATH="$HOME/SPAdes_install_location/bin:$PATH"

metaspades will want to run python3 as just plain "python".
On a basic linux environment, you can do this by installing "pyton-is-python3" like so:

sudo apt install python-is-python3

### BBMap
Just like metaSPAdes, BBMap can be installed using apt install or through the binaries.
Install the BBMap tar from sourceforge at: https://sourceforge.net/projects/bbmap/
Link directory containing the bbmap.sh script to the PATH, this is the bin dir.

export PATH="$HOME/bbmap:$PATH"

### samtools
Install samtools via binary and add to PATH, or use apt install, whatever works.
As long as the "samtools" command is available and working from the current environment.


### MetaBinner
Install MetaBinner into a separate conda environment.
Follow the installation guide on the github: https://github.com/ziyewang/MetaBinner

If the installation from the github guide does not work, this is most likely due to package conflicts.
Try to use a blank conda installation, as this will most likely resolve most package conflicts.
A blank conda environment should work in most cases as long as the python version is 3.7.6.

If all else fails, a blank machine with only python and conda installed will work.

### checkM
Follow the installation guide on: https://github.com/Ecogenomics/CheckM/wiki/Installation#how-to-install-checkm
To run checkM, the database folder needs to downloaded and linked as well.
This is also explaned on the installation guide

Make sure to add the environment load command into the "checkm.wrap" scripts in the scripts directory.

### GTDBK-TK
Follow the guide from https://github.com/Ecogenomics/GTDBTk
Using conda is recommended as this is how the other tools are also installed.

Make sure to download and link the database as well.

Add the environment load command to the "gtdbtk.wrap" script in the workflow scripts directory.


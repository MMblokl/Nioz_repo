#!bin/bash/
for d in simulation_short_read/*/;
do
  metaquast.py ${d}idba/contig-60.fa --unique-mapping -r simulation_short_read/genomes/ -t 16 -o ${d}/idba/quast_outp_WITHref
done

#!bin/bash/
for d in simulation_short_read/*/;
do
  idba_ud -r ${d}fastareads.fa -o ${d}idba/ --mink 60 --maxk 80 --num_threads 16
done

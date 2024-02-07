#!bin/bash/
source $HOME/.bashrc.conda3 gtdbtk
for d in ~/binning/filtered_bins/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  mkdir -p ~/binning/gtdbtk/${id}/concoct/
  mkdir -p ~/binning/gtdbtk/${id}/metabinner/
  mkdir -p ~/binning/gtdbtk/${id}/metawrap/
  mkdir -p ~/binning/gtdbtk/${id}/mulitrunset1
  mkdir -p ~/binning/gtdbtk/${id}/mulitrunset2
  mkdir -p ~/binning/gtdbtk/${id}/mulitrunset3
  gtdbtk classify_wf --genome_dir ~/binning/filtered_bins/${id}/concoct/ --out_dir gtdbtk/${id}/concoct/ -x fa --cpus 16
  gtdbtk classify_wf --genome_dir ~/binning/filtered_bins/${id}/metabinner/ --out_dir gtdbtk/${id}/metabinner/ -x fna --cpus 16
  gtdbtk classify_wf --genome_dir ~/binning/filtered_bins/${id}/metawrap/ --out_dir gtdbtk/${id}/metawrap/ -x fa --cpus 16
  gtdktk classify_wf --genome_dir ~/binning/filtered_bins/${id}/multirunset1 --out_dir gtdbtk/${id}/multirunset1 -x fa --cpus 16
  gtdktk classify_wf --genome_dir ~/binning/filtered_bins/${id}/multirunset2 --out_dir gtdbtk/${id}/multirunset2 -x fa --cpus 16
  gtdktk classify_wf --genome_dir ~/binning/filtered_bins/${id}/multirunset3 --out_dir gtdbtk/${id}/multirunset3 -x fa --cpus 16
done

#!bin/bash/
source $HOME/.bashrc.conda3 checkm
for d in ~/binning/*/mapping
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  #mkdir -p ~/binning/checkm/${id}/concoct/
  #mkdir -p ~/binning/checkm/${id}/metabinner/
  #mkdir -p ~/binning/checkm/${id}/metawrap/
  mkdir -p ~/binning/checkm/${id}/multirunset1/
  mkdir -p ~/binning/checkm/${id}/multirunset2/
  mkdir -p ~/binning/checkm/${id}/multirunset3/
  #checkm lineage_wf -t 16 -x fa ~/binning/${id}/concoct/bins/ ~/binning/checkm/${id}/concoct/
  #checkm lineage_wf -t 16 -x fna ~/binning/${id}/metabinner/metabinner_res/ensemble_res/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ensemble_3logtrans/addrefined2and3comps/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ ~/binning/checkm/${id}/metabinner/
  #checkm lineage_wf -t 16 -x fa ~/binning/${id}/metawrap/binsABC/ ~/binning/checkm/${id}/metawrap/
  checkm lineage_wf -t 16 -x fa ~/binning/${id}/multirun/set1/binsABC/ ~/binning/checkm/${id}/multirunset1/
  checkm lineage_wf -t 16 -x fa ~/binning/${id}/multirun/set2/binsABC/ ~/binning/checkm/${id}/multirunset2/
  checkm lineage_wf -t 16 -x fa ~/binning/${id}/multirun/set3/binsABC/ ~/binning/checkm/${id}/multirunset3/
done

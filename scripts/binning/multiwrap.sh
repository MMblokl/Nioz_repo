#!bin/bash/
source $HOME/.bashrc.conda3 metawrap
for d in ~/binning/filtered_bins/*/
do
  id=$(echo $d | awk -F "/" '{print $(NF-1)}')
  echo $id
  mkdir -p ~/binning/${id}/multirun/set1
  mkdir -p ~/binning/${id}/multirun/set2
  mkdir -p ~/binning/${id}/multirun/set3
  metaWRAP bin_refinement -o ~/binning/${id}/multirun/set1 -t 16 -m 40 -A ~/binning/${id}/metabinner/metabinner_res/ensemble_res/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ensemble_3logtrans/addrefined2and3comps/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ -B ~/binning/${id}/metawrap/concoct_bins/ -C ~/binning/${id}/metawrap/maxbin2_bins/
  metaWRAP bin_refinement -o ~/binning/${id}/multirun/set2 -t 16 -m 40 -A ~/binning/${id}/metabinner/metabinner_res/ensemble_res/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ensemble_3logtrans/addrefined2and3comps/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ -B ~/binning/${id}/metawrap/concoct_bins/ -C ~/binning/${id}/metawrap/metabat2_bins/
  metaWRAP bin_refinement -o ~/binning/${id}/multirun/set3 -t 16 -m 40 -A ~/binning/${id}/metabinner/metabinner_res/ensemble_res/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ensemble_3logtrans/addrefined2and3comps/greedy_cont_weight_3_mincomp_50.0_maxcont_15.0_bins/ -B ~/binning/${id}/metawrap/maxbin2_bins/ -C ~/binning/${id}/metawrap/metabat2_bins/
done

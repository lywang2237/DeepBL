# DeepBL
codes for published work "Deep Learning Parameterization of Tropical Cyclone Boundary Layer"

In folder preprocess_of_LES:

Scripts run in this order
1. Use wrf_interp.ncl to interp the raw TC-LES data to the 14 specific levels in boundary layer (BL). This is a NCAR Command Language script file.
2. Use avg_resolved_var_flux.m to get resovled turbulent fluxes and resolved variables
3. Use get_sfc_flux.py to get surface fluxes
4. Use get_sgs_flux_and_add_together.m to get subgrid scale turbulent fluxes and add them to the resolved fluxes

In folder generate_data_for_NN:

Scripts run in this order:
1. Use gen_raw_data.py to generate raw data and the per-level calculated and global standard deviations and averages
2. Use gen_original_data.py to generate original data (simple normalization)
3. Use gen_nonli_trans.py to generate nonlinearly transformed data (first nonlinear transform, then calculate the stds and avgs of transformed data and normalize)

In folder training_NN:

1. 1DCNN_10l56c.py for the training of 1D-CNN on original data
2. 1DCNN_10l56c_nonli.py for the training of 1D-CNN on nonlinearly transformed data
3. FCNN_same_compute.py for the training of FC-NN-COMP
4. FCNN_same_nodes.py for the training of FC-NN-NODE

The output from gen_raw_data.py, old TC-LES and new TC-LES for test data evaluation of DeepBL and the trained model for 1D-CNN (DeepBL; on original data or nonlinearly transformed data) and FC-NNs are uploaded to Zenodo: https://zenodo.org/record/6641564

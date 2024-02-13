Connects a measurement from HEPdata to a theory provided by LHE events, for the purpose of statistical inference.
Used in a number of pheno studies.

Options are:
- plotting
- get constraints at 68% and 95% CL

Run using:
- python run.py --config-name='CMS_mtt_ALPS'

config-name options are:
- CMS_mtt_ALPS: reproduce fig. 8 of https://arxiv.org/abs/2303.17634
- ATLAS_pt_ALPS: reproduce fig. 9 of https://arxiv.org/abs/2303.17634

Requirements:
- hydra
- numpy
- seaborn
- matplotlib
- black
- scipy

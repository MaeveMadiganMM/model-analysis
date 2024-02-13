import csv
import numpy as np


def preprocess(exp):
    """
    header function, calls the functions below depending on tag
    """

    if exp.cfg.data.data_label == "CMS_mtt_1D_RunII":
        bins, data, covmat = read_CMS_mtt_1D_RunII(exp)
    if exp.cfg.data.data_label == "ATLAS_pt_1D_RunII":
        bins, data, covmat = read_ATLAS_pt_1D_RunII(exp)
    else:
        print("data label not recognised")
        print("data_label", exp.cfg.data.data_label)

    return bins, data, covmat


def csv_reader(filename):
    """Generic CSV reader"""
    output = []
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            output.append(row)
        csvfile.close()
    return output


def read_CMS_mtt_1D_RunII(exp):
    """
    Read and parse the datasets .... ref
    """
    builtdata = csv_reader(exp.cfg.data.data_path)
    cms_data = []
    bins = []
    for item in builtdata[9:24]:
        cms_data.append(float(item[3]))
        bins.append(float(item[1]))
    bins.append(float(item[2]))

    ndat = len(cms_data)
    builtcovdata = csv_reader(exp.cfg.data.covmat_path)
    cms_covmat = np.zeros(ndat * ndat).reshape(ndat, ndat)

    covmatlist = []
    count = 0
    for item in builtcovdata[9 : int(9 + ndat * ndat)]:
        covmatlist.append(float(item[6]))

    for i in range(ndat):
        for j in range(ndat):
            cms_covmat[i, j] = covmatlist[count]
            count += 1

    return (
        np.array(bins, dtype=float),
        np.array(cms_data, dtype=float),
        np.array(cms_covmat, dtype=float),
    )


def read_ATLAS_pt_1D_RunII(exp):
    """
    Read and parse the datasets .... ref
    """
    atlas_hepdata = np.genfromtxt(
        exp.cfg.data.data_path,
        dtype=float,
        usecols=(
            0,
            1,
            2,
        ),
    )
    atlas_bins = atlas_hepdata[:, 0]
    atlas_bins = np.append(atlas_bins, atlas_hepdata[-1, 1])
    atlas_data = atlas_hepdata[:, 2]

    atlas_covmat = np.genfromtxt(exp.cfg.data.covmat_path, dtype=float)

    return (
        np.array(atlas_bins, dtype=float),
        np.array(atlas_data, dtype=float),
        np.array(atlas_covmat, dtype=float),
    )

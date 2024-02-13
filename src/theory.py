import numpy as np


def signal(exp):
    """
    Signal model: assigns the function relevant to
    the model analysis of interest, and returns the signal components.

    Returns
    -------
    float
        Components of the signal model in an EFT approximation: e.g. SM, linear, quadratic

    Raises
    ------
    ValueError
        If the input modelname is unknown

    """
    if exp.modelname == "CMS_mtt_1D_RunII_ALPS":
        signal = signal_CMS_mtt_1D_RunII_ALPS(exp)
        return signal
    elif exp.modelname == "ATLAS_pt_1D_RunII_ALPS":
        signal = signal_ATLAS_pt_1D_RunII_ALPS(exp)
        return signal
    else:
        print("raise error here")  # to do


def signal_CMS_mtt_1D_RunII_ALPS(exp):
    """
    Signal model for the analysis of top ALPS using CMS ttbar data.

    Returns
    -------
    numpy.ndarray
        2D array, specifying the SM, quadratic ALP and quartic ALP contributions to
        the total theory predictions to this dataset, assuming the Wilson coefficient
        ct=1.

    """

    kfac = kfactor(exp)

    bins_width = exp.bins[1:] - exp.bins[:-1]

    sm = np.divide(
        float(exp.cfg.model.BR)
        * np.loadtxt(
            exp.cfg.model.model_path + "/" + exp.cfg.model.SM_file,
            dtype=float,
            usecols=(2,),
        ),
        bins_width,
    )
    axion_lin = np.divide(
        float(exp.cfg.model.BR)
        * np.loadtxt(
            exp.cfg.model.model_path + "/" + exp.cfg.model.model_file_lin,
            usecols=(2,),
            dtype=float,
        ),
        bins_width,
    )
    axion_quad = np.divide(
        float(exp.cfg.model.BR)
        * np.loadtxt(
            exp.cfg.model.model_path + "/" + exp.cfg.model.model_file_quad,
            usecols=(2,),
            dtype=float,
        ),
        bins_width,
    )

    axion_signal = np.c_[kfac * sm, kfac * axion_lin, kfac * axion_quad]
    return axion_signal


def signal_ATLAS_pt_1D_RunII_ALPS(exp):
    """
    Signal model for the analysis of top ALPS using CMS ttbar data.

    Returns
    -------
    numpy.ndarray
        2D array, specifying the SM, quadratic ALP and quartic ALP contributions to
        the total theory predictions to this dataset, assuming the Wilson coefficient
        ct=1.

    """

    kfac = kfactor(exp)

    bins_width = exp.bins[1:] - exp.bins[:-1]

    sm = np.divide(
        float(exp.cfg.model.BR)
        * np.loadtxt(
            exp.cfg.model.model_path + "/" + exp.cfg.model.SM_file,
            dtype=float,
            usecols=(2,),
        ),
        bins_width,
    )
    axion_lin = np.divide(
        float(exp.cfg.model.BR)
        * np.loadtxt(
            exp.cfg.model.model_path + "/" + exp.cfg.model.model_file_lin,
            usecols=(2,),
            dtype=float,
        ),
        bins_width,
    )
    axion_quad = np.divide(
        float(exp.cfg.model.BR)
        * np.loadtxt(
            exp.cfg.model.model_path + "/" + exp.cfg.model.model_file_quad,
            usecols=(2,),
            dtype=float,
        ),
        bins_width,
    )

    axion_signal = np.c_[kfac * sm, kfac * axion_lin, kfac * axion_quad]
    return axion_signal

def kfactor(exp):
    """
    QCD kfactor
    If specified in the config file, load a QCD kfactor to multiply by theory predictions.

    Returns
    -------
    numpy.ndarray
        1D array, of length equal to the number of bins, specifying the ratio of the SM predictions at NNLO in QCD
        to the predictions at NLO in QCD

    """
    if exp.cfg.model.kfactor is None:
        kfac = np.ones(len(exp.proc_data))
    else:
        kfac = np.loadtxt(
            exp.cfg.model.model_path + "/" + exp.cfg.model.kfactor,
            dtype=float,
            usecols=(0,),
        )

    return kfac

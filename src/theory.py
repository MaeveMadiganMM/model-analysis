import numpy as np


def signal(exp):
    if exp.modelname == "CMS_mtt_1D_RunII_ALPS":
        signal = signal_CMS_mtt_1D_RunII_ALPS(exp)
        return signal
    else:
        print("raise error here")


def signal_CMS_mtt_1D_RunII_ALPS(exp):
    """
    Construct model signal as a function of the model parameter of interest.
    Branch this out into a choice of models:
    if model-name = ..., call funcA() etc
    Calculate SM + C^2*sigma + C^4*sigma
    and uncertainties
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
    if exp.cfg.model.kfactor == None:
        kfac = np.ones(len(exp.proc_data))
    else:
        kfac = np.loadtxt(
            exp.cfg.model.model_path + "/" + exp.cfg.model.kfactor,
            dtype=float,
            usecols=(0,),
        )

    return kfac

import numpy as np
from src.theory import signal as model
from scipy.optimize import minimize, brentq


def chi2(ct, signal, exp):
    """
    Chi2 test-statistic as a function of the parameter of interest.
    Built from the signal predictions and data inputs.

    Returns
    -------
    float
        Value of the chi2 at the given value of ct

    """
    sm = signal[:, 0]
    quad = signal[:, 1]
    quart = signal[:, 2]
    theory = sm + quad * ct**2 + quart * ct**4
    diff = theory - exp.proc_data
    Vinv = np.linalg.inv(exp.proc_covmat)
    return ((diff).dot(Vinv)).dot(diff)


def limits(exp):
    """
    Limit-setting routine.
    Solves for the minimum chi2, and obtains the values of ct at which delta chi2 = 0.99, 3.84

    Returns
    -------
    List
        List of floats, giving the upper and lower constraints at 68 and 95% CL

    """
    cvals = np.arange(-30, 30, 1)
    exp.proc_covmat = exp.proc_covmat
    chivals = []

    # Get model predictions
    signal = model(exp)

    # minimise the chi2
    min1, min2 = (
        minimize(chi2, args=(signal, exp), x0=-100).x,
        minimize(chi2, args=(signal, exp), x0=100).x,
    )
    chi2min = chi2(min1, signal, exp)

    for ct in cvals:
        chivals.append(chi2(ct, signal, exp) - chi2min)

    def func_to_solve_68(ct):
        return chi2(ct, signal, exp) - chi2min - 0.99

    def func_to_solve_95(ct):
        return chi2(ct, signal, exp) - chi2min - 3.84

    c68a, c68b = brentq(func_to_solve_68, a=-1000, b=min1), brentq(
        func_to_solve_68, a=min2, b=1000.0
    )
    c95a, c95b = brentq(func_to_solve_95, a=-1000, b=min1), brentq(
        func_to_solve_95, a=min2, b=1000.0
    )

    return [c68a, c68b, c95a, c95b]

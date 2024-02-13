import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from src.theory import signal as model

import seaborn as sns
colors = sns.color_palette("colorblind", 8)


def plotter(exp):
    # config things
    ctvals = [0.0, 4.0, 12.0, 20.0]

    len_data = len(exp.bins) - 1

    # organise bins
    bins_centre = 0.5 * (exp.bins[:-1] + exp.bins[1:])
    bins_width = exp.bins[1:] - exp.bins[:-1]

    # Create uncertainties from covmat for plotting
    data_unc = np.sqrt(np.diag(exp.proc_covmat))

    # Create arrays for step plot
    exp.proc_data_plot = np.concatenate([exp.proc_data, [exp.proc_data[-1]]])
    data_unc_plot = np.concatenate([data_unc, [data_unc[-1]]])

    fig = plt.figure(figsize=(7, 7))
    matplotlib.rc("font", **exp.cfg.font)
    gs = fig.add_gridspec(
        2,
        1,
        height_ratios=(4, 1),
        left=0.14,
        right=0.86,
        bottom=0.1,
        top=0.9,
        wspace=0.55,
        hspace=0.25,
    )

    # Create the Axes.
    ax = fig.add_subplot(gs[0, 0])
    ax_ratio = fig.add_subplot(gs[1, 0], sharex=ax)

    # Main plot | ax
    ax.step(
        exp.bins, exp.proc_data_plot, where="post", label="CMS data", color=colors[0]
    )
    ax.fill_between(
        exp.bins,
        exp.proc_data_plot - data_unc_plot,
        exp.proc_data_plot + data_unc_plot,
        color=colors[0],
        step="post",
        alpha=0.2,
    )
    ax.set_title(exp.cfg.plottitle)
    ax.set_yscale("log")
    ax.set_xlim([355, 3500])  # change to bins min and max
    ax.set_xlabel(exp.cfg.plotxlabel)
    ax.set_ylabel(exp.cfg.plotylabel)

    # Lower plot | ax_ratio
    ax_ratio.set_xlabel(exp.cfg.plotxlabel)
    ax_ratio.set_ylabel("Ratio to data")
    ax_ratio.hlines(
        xmin=355, xmax=3500, y=1.0, color=colors[0]
    )  # change to bins min and max

    for ind in range(len(ctvals)):
        # Get model predictions
        signalComp = model(exp)

        signal = (
            signalComp[:, 0]
            + ctvals[ind] ** 2 * signalComp[:, 1]
            + ctvals[ind] ** 4 * signalComp[:, 2]
        )

        # Main plot | ax
        signal_plot = np.concatenate([signal, [signal[-1]]])
        # signal_unc_plot = np.concatenate([signal_unc, [signal_unc[-1]]])

        ax.step(
            exp.bins,
            signal_plot,
            where="post",
            label=r"SM + ALP, $c_{t}/f_a = $" + str(int(ctvals[ind])) + r" TeV$^{-1}$",
            color=colors[ind + 1],
        )

        # Lower plot | ax_ratio
        signal_ratio = np.divide(signal_plot, exp.proc_data_plot)
        data_ratio_unc = np.divide(data_unc_plot, exp.proc_data_plot)
        # signal_ratio_unc = signal_ratio * np.sqrt(
        #    data_ratio_unc**2 + np.divide(signal_unc_plot, signal_plot) ** 2
        # )

        ax_ratio.step(exp.bins, signal_ratio, where="post", color=colors[ind + 1])
    ax_ratio.fill_between(
        exp.bins,
        1 - data_ratio_unc,
        1 + data_ratio_unc,
        color=colors[0],
        step="post",
        alpha=0.4,
    )

    ax.legend()
    # plt.tight_layout()
    plt.savefig("outputs/" + exp.cfg.plotfilename)

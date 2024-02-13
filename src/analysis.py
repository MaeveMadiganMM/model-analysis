from src.data import preprocess
from src.plotter import plotter
from src.limits import limits


class Analysis:
    """
    Analysis class, bringing together the preprocessed dataset and signal
    model to produce plots and get constraints on the model parameter of interest.

    Attributes
    ----------
    cfg : omegaconf.dictconfig.DictConfig
        configuration file
    modelname : str
        unique identifier for the model analysis of interest
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.modelname = self.cfg.data.data_label + "_" + self.cfg.model.model_label

    def analyse(self):
        """Analyse function.

        Runs the full analysis, determined by settings in the config file.
        """

        self.build_data()

        if self.cfg.plot:
            self.plot()

        if self.cfg.limits:
            self.get_constraints()

    def build_data(self):
        """Build the preprocessed datasets, for use in the chi2 and plotting scripts."""
        self.dataname = self.cfg.data.data_label
        self.bins, self.proc_data, self.proc_covmat = preprocess(self)

    def plot(self):
        """Call the plotting routine"""
        plotter(self)

    def get_constraints(self):
        """Obtain contraints at 68% and 95% CL, and output"""
        constraints = limits(self)
        print("limits at 68% CL")
        print(constraints[0], constraints[1])
        print("limits at 95% CL")
        print(constraints[2], constraints[3])

from src.data import preprocess
from src.plotter import plotter
from src.limits import limits

class Experiment():

    def __init__(self,cfg):
        self.cfg = cfg
        self.modelname = self.cfg.data.data_label+'_'+self.cfg.model.model_label
        
    def analyse(self):
        self.build_data()

        if self.cfg.plot:
            self.plot()

        if self.cfg.limits:
            self.get_constraints()

    def build_data(self):
        self.dataname = self.cfg.data.data_label
        self.bins, self.proc_data, self.proc_covmat = preprocess(self)

    def plot(self):
        plotter(self)


    def get_constraints(self):
        constraints = limits(self)
        print('limits at 68% CL')
        print(constraints[0], constraints[1])
        print('limits at 95% CL')
        print(constraints[2], constraints[3])

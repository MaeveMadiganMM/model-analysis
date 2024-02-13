import hydra
from src.analysis import Analysis


@hydra.main(config_path="config", config_name="CMS_mtt_ALPS", version_base=None)
def main(cfg):
    # Create an instance of the analysis class with config details given by cfg
    exp = Analysis(cfg)

    # Run the full analysis toolchain
    exp.analyse()


if __name__ == "__main__":
    main()

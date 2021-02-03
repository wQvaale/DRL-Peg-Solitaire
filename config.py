# TODO: Use CLI-based input to toggle between various configurations
# from sys import argv
import yaml


class Config:
    def __init__(self, config_path):
        configuration = yaml.load(open(config_path, 'r'), Loader=yaml.SafeLoader)

        self.agent_config = configuration["AGENT"]
        self.initial_pi_range = self.agent_config["INITIAL_PI_RANGE"]
        self.divider = self.agent_config["DIVIDER"]
        self.learning_rate = self.agent_config["LEARNING_RATE"]
        self.discount = self.agent_config["DISCOUNT"]
        self.decay = self.agent_config["DECAY"]



# TODO: Use CLI-based input to toggle between various configurations
# from sys import argv
import yaml


class Config:
    def __init__(self, config_path):
        configuration = yaml.load(open(config_path, 'r'), Loader=yaml.Loader)

        self.agent_config = configuration["AGENT"]
        self.learning_rate = float(self.agent_config["LEARNING_RATE"])
        self.discount = float(self.agent_config["DISCOUNT"])
        self.decay = float(self.agent_config["DECAY"])



# TODO: Use CLI-based input to toggle between various configurations using `argv`
import yaml
import numpy as np
from agent import NeuralAgent, TableAgent


class Config:
    def __init__(self, config_path):
        configuration = yaml.load(open(config_path, 'r'), Loader=yaml.Loader)

        self.defaults = configuration["DEFAULT"]
        self.shape = self.defaults["SHAPE"]
        self.size = self.defaults["SIZE"]
        self.epsilon = self.defaults["EPSILON"]
        self.epsilon_dr = self.defaults["EPSILON_DR"]
        self.episodes = self.defaults["EPISODES"]
        self.delay = self.defaults["DELAY"]


        self.agent_type = self.defaults["AGENT_TYPE"].upper()
        self.agent_config = configuration[self.agent_type]
        self.learning_rate = float(self.agent_config["LEARNING_RATE"])
        self.actor_learning_rate = self.learning_rate + float(self.agent_config["ADDITIONAL_LEARNING"])
        self.discount = float(self.agent_config["DISCOUNT"])
        self.decay = float(self.agent_config["DECAY"])

        self.holes = self.set_holes(self.defaults["HOLES"])
        self.layers = self.set_layer_dimensions(list(self.agent_config["HIDDEN_LAYERS"]))

    def set_layer_dimensions(self, hidden_layers):
        if self.shape.upper() == "TRIANGLE":
            first_layer_dimensions = self.size * (self.size + 1) / 2
        elif self.shape.upper() == "DIAMOND":
            first_layer_dimensions = self.size * self.size
        else:
            raise Exception("Shape must be 'Triangle' or 'Diamond'")

        layers = np.insert(hidden_layers, 0, first_layer_dimensions)
        layers = np.append(layers, 1)
        return layers

    @staticmethod
    def set_holes(holes):
        ret = []
        for hole in holes:
            ret.append(tuple(hole))
        return ret

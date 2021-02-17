# TODO: Use CLI-based input to toggle between various configurations using `argv`
import yaml
import numpy as np

from agent import NeuralAgent, TableAgent


class Config:
    def __init__(self, config_path):
        configuration = yaml.load(open(config_path, 'r'), Loader=yaml.Loader)

        self.agent_config = configuration["NEURAL_AGENT"]
        self.learning_rate = float(self.agent_config["LEARNING_RATE"])
        self.discount = float(self.agent_config["DISCOUNT"])
        self.decay = float(self.agent_config["DECAY"])

        self.defaults = configuration["DEFAULT"]
        self.shape = self.defaults["SHAPE"]
        self.size = self.defaults["SIZE"]
        self.epsilon = self.defaults["EPSILON"]
        self.epsilon_dr = self.defaults["EPSILON_DR"]
        self.episodes = self.defaults["EPISODES"]

        self.holes = self.set_holes(self.defaults["HOLES"])
        self.agent = self.set_agent(self.defaults["AGENT_TYPE"])
        self.layers = self.set_layer_dimensions(list(self.agent_config["LAYERS"]))

    def set_agent(self, agent_string):
        if agent_string.upper() == "NEURAL":
            return NeuralAgent(self)
        elif agent_string.upper() == "TABLE":
            return TableAgent(self)
        else:
            raise Exception("Actor type must be 'NEURAL' or 'ACTOR_CRITIC'")

    def set_layer_dimensions(self, hidden_layers):
        if self.shape.upper() == "TRIANGLE":
            first_layer_dimensions = self.size * (self.size + 1) / 2
        elif self.shape.upper() == "DIAMOND":
            first_layer_dimensions = self.size * self.size
        else:
            raise Exception("Shape must be 'Triangle' or 'Diamond'")

        layers = np.insert(hidden_layers, 0, first_layer_dimensions)
        return layers

    @staticmethod
    def set_holes(holes):
        ret = []
        for hole in holes:
            ret.append(tuple(hole))
        return ret

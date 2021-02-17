import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
from scipy.interpolate import make_interp_spline

from agent import NeuralAgent, TableAgent


def smooth_curve(data):
    x = np.array(range(0, 600))
    y = np.array(data)
    x_new = np.linspace(0, x, 50)
    a_BSpline = make_interp_spline(x, y)
    y_new = a_BSpline(x_new)
    return x_new, y_new


def visualize_training_performance(remaining_pegs, epsilons, wins):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, figsize=(16, 4))
    fig.suptitle("Training performance visualized")
    fig.text(0.5, 0.01, "Episodes", ha="center")

    ax1.plot(remaining_pegs, 'b')
    ax1.set_ylabel("Remaining pegs")

    ax2.plot(epsilons, 'r')
    ax2.set_ylabel("Epsilon")

    # i, j = smooth_curve(wins)
    y = gaussian_filter1d(wins, sigma=1)
    ax3.plot(y, 'g')
    ax3.set_ylabel("# wins")

    plt.show()


def create_agent(cfg):
    if cfg.agent_type.upper() == "NEURAL":
        return NeuralAgent(cfg)
    elif cfg.agent_type.upper() == "TABLE":
        return TableAgent(cfg)
    else:
        raise Exception("Actor type must be 'NEURAL' or 'ACTOR_CRITIC'")


class PerformanceTracker:
    def __init__(self):
        self.remaining_pegs = list()
        self.epsilons = list()
        self.wins = list()

    def update(self, remaining_peg, win, epsilon):
        self.remaining_pegs.append(remaining_peg)
        self.epsilons.append(epsilon)
        self.wins.append(win)

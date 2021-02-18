import matplotlib.pyplot as plt
from agent import NeuralAgent, TableAgent


def visualize_training_performance(remaining_pegs, epsilons, wins):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, figsize=(16, 4))
    fig.suptitle("Training performance visualized")
    fig.text(0.5, 0.01, "Episodes", ha="center")

    ax1.plot(remaining_pegs, 'b')
    ax1.set_ylabel("Remaining pegs")

    ax2.plot(epsilons, 'r')
    ax2.set_ylabel("Epsilon")

    ax3.plot(wins, 'g')
    ax3.set_ylabel("# wins")

    plt.show()


def create_agent(cfg):
    if cfg.agent_type.upper() == "NEURAL":
        return NeuralAgent(cfg)
    elif cfg.agent_type.upper() == "TABLE":
        return TableAgent(cfg)
    else:
        raise Exception("Actor type must be 'NEURAL' or 'TABLE'")


class PerformanceTracker:
    def __init__(self):
        self.remaining_pegs = list()
        self.epsilons = list()
        self.wins = list()

    def update(self, remaining_peg, win, epsilon):
        self.remaining_pegs.append(remaining_peg)
        self.epsilons.append(epsilon)
        self.wins.append(win)

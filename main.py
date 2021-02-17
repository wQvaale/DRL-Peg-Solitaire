from tqdm import tqdm
from config import Config
from sim_world import SimWorld
from game import Game
from utils import visualize_training_performance, create_agent


class PerformanceTracker:
    def __init__(self):
        self.remaining_pegs = list()
        self.epsilons = list()
        self.wins = list()

    def update(self, remaining_peg, win, epsilon):
        self.remaining_pegs.append(remaining_peg)
        self.epsilons.append(epsilon)
        self.wins.append(win)


def train(cfg: Config, agent):
    agent = agent
    epsilon = cfg.epsilon
    tracker = PerformanceTracker()
    sim_world = SimWorld(cfg)

    for _ in tqdm(range(cfg.episodes)):
        epsilon *= cfg.epsilon_dr
        Game.play(sim_world, agent, epsilon, viz_toggle=False)

        tracker.update(remaining_peg=sim_world.get_remaining_pegs(),
                       epsilon=epsilon,
                       win=agent.wins)

        sim_world.reset_world()
        agent.flush()
    print(f"Agent wins during training:\t{agent.wins}")
    return agent, tracker


def test(agent, cfg: Config):
    trained_wins = agent.wins
    sim_world = SimWorld(cfg)
    Game.play(sim_world, agent, epsilon=-1, viz_toggle=True)
    result = agent.wins - trained_wins
    print("Agent won!" if result else "Agent lost...")
    agent.flush()


if __name__ == '__main__':
    cfg = Config("configs/config.yaml")

    agent = create_agent(cfg)

    trained_agent, tracker = train(cfg, agent)

    visualize_training_performance(tracker.remaining_pegs, tracker.epsilons, tracker.wins)

    test(trained_agent, cfg)

    # TODO:
    """
    1. Size 5 triangle with ActorCriticAgent (aka TableBased)
    2. Size 5 triangle with NeuralAgent
    3. Size 4 diamond with ActorCriticAgent (aka TableBased)
    4. Size 4 diamond with NeuralAgent
    5. All hyperparams MUST be configurable @wQuole
    6. Triangles from size 4 up to size 8
    7. Diamonds from size 3 up to size 6
    8. You should be able to locate the 2 holes that are doable in size 4 diamond
    9. We need to plot the convergence!
    10. Rename gamma to TD_ERROR
    11. Enable VIZ for test_triangle
    12. Generalize train_test
    13. reward = 10000, negative_reward = -1*len(remaining_pegs)
    14. Dynamic EPSILON + refactor usage of it
    15. Save a 8 diamond
    16. @tjedor check whether you approve of the ActorCriticAgent's learning_rate
    """

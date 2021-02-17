from tqdm import tqdm
from config import Config
from sim_world import SimWorld
from utils import visualize_training_performance


class PerformanceTracker:
    def __init__(self):
        self.remaining_pegs = list()
        self.epsilons = list()
        self.wins = list()

    def update(self, remaining_peg, win, epsilon):
        self.remaining_pegs.append(remaining_peg)
        self.epsilons.append(epsilon)
        self.wins.append(win)


def train(cfg: Config):
    agent = cfg.agent
    epsilon = cfg.epsilon
    tracker = PerformanceTracker()

    for _ in tqdm(range(cfg.episodes)):
        sim_world = SimWorld(cfg)
        epsilon *= cfg.epsilon_dr
        sim_world.play_RL(agent, epsilon, choose_best=False)

        tracker.update(remaining_peg=sim_world.get_remaining_pegs(),
                       epsilon=epsilon,
                       win=agent.wins)
        agent.flush()
    print(f"Agent wins during training:\t{agent.wins}")
    return agent, tracker


def test(agent, cfg: Config):
    trained_wins = agent.wins
    sim_world = SimWorld(cfg, viz_toggle=True)
    sim_world.play_RL(agent, choose_best=True)
    result = agent.wins - trained_wins
    print("Agent won!" if result else "Agent lost...")
    agent.flush()


if __name__ == '__main__':
    cfg = Config("configs/config.yaml")

    trained_agent, tracker = train(cfg)

    visualize_training_performance(tracker.remaining_pegs, tracker.epsilons, tracker.wins)

    test(trained_agent, cfg)

    # 1.
    # train_and_test_triangle(actor_critic_agent, size=5)
    # train_and_test_triangle(neural_agent, size=5)

    # 2.
    # train_and_test_diamond(actor_critic_agent, size=4)
    # train_and_test_diamond(neural_agent, size=4)

    # 3.
    # for i in range(4, 5):
    #     train_and_test_triangle(actor_critic_agent, size=i)

    # for i in range(3, 7):
    #     train_and_test_diamond(actor_critic_agent, size=i)

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

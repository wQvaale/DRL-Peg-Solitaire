from hex_grid import Triangle
from sim_world import SimWorld
from agent import *
from tqdm import tqdm
import matplotlib.pyplot as plt


def train(agent, sim_world, init_holes, shape, size, episodes):
    remaining_pegs = list()
    rewards = list()
    epsilon: float = 0.3

    for i in tqdm(range(episodes)):
        sim_world.new_game(shape, size, init_holes)
        # e = epsilon - (epsilon*i/episodes)
        epsilon *= 0.997
        if i > 490:
            sim_world.play_RL(agent, epsilon, choose_best=True)
        else:
            sim_world.play_RL(agent, epsilon, choose_best=False)
        # if i % 50 == 0:
        #     remaining_pegs.append((agent.wins - wins)/100)
        #     wins = agent.wins
        remaining_pegs.append(sim_world.get_remaining_pegs())
        rewards.append(sim_world.get_reward())
        agent.flush()
    print(agent.wins)
    return agent, remaining_pegs, rewards


def test(agent, init_holes, shape, size):
    w = agent.wins
    asd = SimWorld(shape=shape, size=size, holes=init_holes, viz_toggle=True)
    asd.play_RL(agent, choose_best=True)
    print(agent.wins - w)
    agent.flush()


if __name__ == '__main__':
    cfg = Config("configs/config.yaml")

    sim_world = SimWorld(shape="Diamond", size=4, holes=[(1, 2)])

    actor_critic_agent = ActorCriticAgent(cfg)
    neural_agent = NeuralAgent(cfg)

    trained_agent, remains, rewards = train(neural_agent, sim_world, init_holes=[(1, 2)], shape="Diamond", size=4, episodes=500)

    plt.plot(remains)
    plt.show()

    test(trained_agent, init_holes=[(1, 2)], shape="Diamond", size=4)

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
    """

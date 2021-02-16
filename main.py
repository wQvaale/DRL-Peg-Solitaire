from hex_grid import Triangle
from sim_world import SimWorld
from agent import *
from tqdm import tqdm
import matplotlib.pyplot as plt


def train_and_test_triangle(agent, size=5):
    j = 0
    for row in tqdm(range(0, 5)):
        for col in range(row + 1):
            for i in range(500):
                sim_world = SimWorld(shape="Triangle", size=size, holes=[(row, col)])
                sim_world.play_RL(agent, 0.5)
                agent.flush()
    agent_wins = agent.wins

    for row in range(0, 5):
        for col in range(row + 1):
            sim_world = SimWorld(shape="Triangle", size=size, holes=[(row, col)], viz_toggle=1)
            sim_world.play_RL(agent, greed=0, choose_best=True)
            agent.flush()

    print(agent.actor.state_action_pairs)
    print(f"Agent wins:\t{agent.wins - agent_wins}")


def train_and_test_diamond(agent, episodes=500, size=4):
    holes = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for hole in holes:
        for i in tqdm(range(episodes)):
            sim_world = SimWorld(shape="Diamond", size=size, holes=[hole])
            sim_world.play_RL(agent, 0.5)
            agent.flush()

    trained_agent_wins = agent.wins

    for hole in holes:
        sim_world = SimWorld(shape="Diamond", size=size, holes=[hole], viz_toggle=True)
        sim_world.play_RL(agent, greed=0, choose_best=True)
        agent.flush()

    print(agent.actor.state_action_pairs)
    print(f"Agent wins:\t{agent.wins - trained_agent_wins}")


def train(agent, sim_world, init_holes=[(0, 0)], shape="Diamond", size=4, episodes=100):
    remaining_pegs = list()
    epsilon: float = 0.2

    wins = 0
    for i in tqdm(range(episodes)):
        sim_world.new_game(shape, size, init_holes)
        e = epsilon - (epsilon*i/episodes)
        sim_world.play_RL(agent, epsilon_greedy=e)
        # if i % 50 == 0:
        #     remaining_pegs.append((agent.wins - wins)/100)
        #     wins = agent.wins
        remaining_pegs.append((sim_world.get_remaining_pegs()))
        agent.flush()
    print(agent.wins)
    return remaining_pegs, agent


def test(agent, init_holes=[(0, 0)], shape="Diamond", size=4):
    w = agent.wins
    asd = SimWorld(shape=shape, size=size, holes=init_holes, viz_toggle=True)
    asd.play_RL(agent, choose_best=True)
    print(agent.wins - w)
    agent.flush()


if __name__ == '__main__':
    cfg = Config("configs/config.yaml")

    sim_world = SimWorld(shape="Triangle", size=4, holes=[(1,1)])

    actor_critic_agent = ActorCriticAgent(cfg)
    neural_agent = NeuralAgent(cfg)

    remains, trained_agent = train(neural_agent, sim_world, init_holes=[(1, 2)], shape="Diamond", size=4, episodes=1000)

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

from hex_grid import Triangle
from sim_world import SimWorld
from agent import *


def triangle_example():
    size = 4
    t = Triangle(size, [(1, 0)])
    for row in t.grid:
        for cell in row:
            print(cell.getPos())


def train_and_test_triangle(agent):
    for row in range(0, 5):
        for col in range(row):
            for i in range(1000):
                if i % 100 == 0:
                    print(i)

                sim_world = SimWorld(shape="Triangle", size=4, holes=[(row, col)])
                sim_world.play_RL(agent, 0.5)
                agent.flush()
    agent_wins = agent.wins

    for row in range(0, 5):
        for col in range(row):
            sim_world = SimWorld(shape="Triangle", size=4, holes=[(row, col)])
            sim_world.play_RL(agent, greed=0, vis=True, choose_best=True)
            agent.flush()

    print(agent.actor.state_action_pairs)
    print(f"Agent wins:\t{agent.wins - agent_wins}")


def train_diamond(agent, epochs=1000):
    holes = [(1,1), (1,2), (2,1), (2,2)]
    for hole in holes:
        for i in range(epochs):
            sim_world = SimWorld(shape="Diamond", size=4, holes=[hole])
            sim_world.play_RL(agent, 0.5)
            agent.flush()

    trained_agent_wins = agent.wins

    for hole in holes:
        sim_world = SimWorld(shape="Diamond", size=4, holes=[hole], viz_toggle=True)
        sim_world.play_RL(agent, greed=0, vis=True, choose_best=True)
        agent.flush()

    print(agent.actor.state_action_pairs)
    print(f"Agent wins:\t{agent.wins - trained_agent_wins}")





if __name__ == '__main__':
    cfg = Config("configs/config.yaml")

    #sim_world = SimWorld(shape="Diamond", viz_toggle=1)
    #sim_world.play_solitaire_random_agent()

    agent = ActorCriticAgent(cfg)
    train_diamond(agent)

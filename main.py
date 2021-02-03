from hex_grid import Triangle
from sim_world import SimWorld
from agent import *


def triangle_example():
    size = 4
    t = Triangle(size, [(1, 0)])
    for row in t.grid:
        for cell in row:
            print(cell.getPos())


def train_randomly(agent, shape="Diamond"):
    for row in range(0, 5):
        for col in range(row):

            for i in range(1000):
                if i % 100 == 0:
                    print(i)

                sim_world = SimWorld(shape=shape, size=5, holes=[(row, col)])
                sim_world.play_RL(agent, 0.5)
                agent.flush()

    for i in range(10):
        x = random.randint(0, 4)
        y = random.randint(0, x)
        sim_world = SimWorld(shape=shape, size=5, holes=[(y, x)])
        sim_world.play_RL(agent, greed=0, vis=True, choose_best=True)
        agent.flush()

    agent_wins = agent.wins
    but = len(agent.actor.state_action_pairs)
    print(agent.actor.state_action_pairs)
    print(agent_wins, agent.wins - agent_wins)
    print(but, len(agent.actor.state_action_pairs))


if __name__ == '__main__':

    sim_world = SimWorld(shape="Diamond")
    agent = ActorCriticAgent
    sim_world.play_solitaire_random_agent()

    # train_randomly(agent)

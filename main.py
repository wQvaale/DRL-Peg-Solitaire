from tqdm import tqdm
from config import Config
from sim_world import SimWorld
from game import Game
from utils import visualize_training_performance, create_agent, PerformanceTracker


def train(agent, cfg: Config):
    agent = agent
    epsilon = cfg.epsilon
    tracker = PerformanceTracker()
    sim_world = SimWorld(cfg)

    for _ in tqdm(range(cfg.episodes)):
        epsilon *= cfg.epsilon_dr
        Game.play(sim_world=sim_world,
                  agent=agent,
                  epsilon=epsilon,
                  delay=cfg.delay,
                  viz_toggle=False)

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

    Game.play(sim_world=sim_world,
              agent=agent,
              epsilon=0,
              delay=cfg.delay,
              viz_toggle=True)

    result = agent.wins - trained_wins
    print("Agent won!" if result else "Agent lost...")
    agent.flush()


if __name__ == '__main__':
    cfg = Config("configs/config.yaml")

    agent = create_agent(cfg)

    trained_agent, tracker = train(agent, cfg)
    visualize_training_performance(tracker.remaining_pegs, tracker.epsilons, tracker.wins)

    test(trained_agent, cfg)


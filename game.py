from viz import Viz


class Game:

    @staticmethod
    def play(sim_world, agent, epsilon, viz_toggle=False):
        if viz_toggle: visualizer = Viz(sim_world.board)

        while sim_world.get_all_legal_moves():
            prev_state = sim_world.board.stringify()
            action = agent.get_move(state=prev_state, e_greedy=epsilon, moves=sim_world.get_all_legal_moves())

            if viz_toggle: visualizer.step(sim_world.board, action)
            sim_world.solitaire_jump(action)
            if viz_toggle: visualizer.step(sim_world.board, None)

            reward = sim_world.get_reward()
            agent.update(prev_state, action, reward, sim_world.board.stringify())

            if sim_world.is_victory():
                agent.wins += 1
                if viz_toggle:
                    visualizer.viz()
                break
            elif sim_world.is_loss():
                if viz_toggle:
                    visualizer.viz()
                break

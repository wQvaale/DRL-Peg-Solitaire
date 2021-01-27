
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()

G = nx.complete_graph(4)
pos = nx.spring_layout(G, iterations=100)

def update(i):
    col = ['grey', 'grey', 'grey', 'grey']
    if i == 1:
        col = ['grey', 'grey', 'grey', 'black']
    if i == 0:
        col = ['grey', 'grey', 'black', 'black']
    if i == 3:
        col = ['grey', 'black', 'black', 'black']
    if i == 4:
        col = ['black', 'black', 'black', 'black']
    return nx.draw(G, pos=pos, node_color=col)

animation = FuncAnimation(fig, func=update, frames=5, interval=1000)
plt.show()


import numpy as np
import argparse
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(time, trace_data, n_nodes):

    x = trace_data[time*n_nodes:(time+1)*n_nodes,2] #trace_data[(time+1)*n_nodes:(time+2)*n_nodes,2] - trace_data[time*n_nodes:(time+1)*n_nodes,2] 

    y = trace_data[time*n_nodes:(time+1)*n_nodes,3] #trace_data[(time+1)*n_nodes:(time+2)*n_nodes,3] - trace_data[time*n_nodes:(time+1)*n_nodes,3] 

    scatter.set_offsets(np.c_[x, y])

    return scatter,


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, help='data path')
    parser.add_argument('--n_nodes', type=int, help='number of ndoes')
    parser.add_argument('--range', type=int, help='range of time')
    args = parser.parse_args()

    if not (args.data_path or args.n_nodes or args.range):
        exit()

    trace_data = np.loadtxt(args.data_path)

    plt.style.use('seaborn-pastel')

    fig = plt.figure()

    ax = plt.axes(xlim=(0, 30000), ylim=(0, 30000))

    scatter = ax.scatter(trace_data[0:args.n_nodes,2], trace_data[0:args.n_nodes,3], c = np.random.rand(args.n_nodes), s=100)

    anim = FuncAnimation(fig, animate, frames=1800, interval=1, fargs=(trace_data, args.n_nodes))
    #anim.save('../plot_results/animation.gif', writer='pillow')
    plt.show()

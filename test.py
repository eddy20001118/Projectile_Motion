from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
fig, ax = plt.subplots()

x = range(100)
y = range(100)
line, = ax.plot(x, y)


def animate(i):
    line.set_xdata(x[:i])
    line.set_ydata(y[:i])
    return line,


def init():
    return line,


ani = animation.FuncAnimation(fig=fig,
                              func=animate,
                              frames=100,
                              init_func=init,
                              interval=50,
                              blit=True,
                              repeat = False)

plt.show()
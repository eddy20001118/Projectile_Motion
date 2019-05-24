matplotlib_exist = False

try:
    from matplotlib import animation
    from matplotlib import pyplot as plt
    import numpy as np
    matplotlib_exist = True
except:
    pass

class mpt_animation:
    def __init__(self, projectile):
        name = projectile.name
        cal_res = projectile.cal_res
        self.dis_x_arr = cal_res["dis_x_arr"]
        self.dis_y_arr = cal_res["dis_y_arr"]
        self.time_step = cal_res["time_step"] * 1000
        self.length = cal_res["length"]
        self.line, = plt.plot(self.dis_x_arr, self.dis_y_arr,ls='--',label=name)
        self.dot, = plt.plot([],[],"ro")
        self.ani = animation.FuncAnimation(fig=plt.figure(1),
                                frames=self.length,
                                func=self.animate,
                                init_func=self.init,
                                interval=self.time_step,
                                blit=False,
                                repeat=False)

    def init(self):
        return self.line, self.dot,

    def animate(self, i):
        self.line.set_data(self.dis_x_arr[:i],self.dis_y_arr[:i])
        self.dot.set_data(self.dis_x_arr[i],self.dis_y_arr[i])
        return self.line, self.dot,

def run_animation_2d():
    plt.legend(loc='upper right')
    plt.grid()
    plt.xlabel("displacement x (m)")
    plt.ylabel("displacement y (m)")
    plt.title("Projectile Motion Simulator")
    plt.show()
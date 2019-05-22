from matplotlib import animation
from matplotlib import pyplot as plt
from vpython import *


class animation_3d:
    scene = None
    color_list = [vector(1, 0.85, 0.73), vector(
        1, 0.96, 0.56), vector(1, 0.27, 0)]
    color_count = 0
    total_count = 0

    @classmethod
    def count(cls):
        if cls.color_count < 3:
            cls.color_count += 1
        else:
            cls.color_count = 1
        cls.total_count += 1

    @classmethod
    def create_scene(cls):
        cls.scene = canvas(width=1440, height=900, background=color.white)

    @classmethod
    def exit_animation(cls):
        if cls.scene.waitfor("keydown"):
            cls.scene.delete()
            cls.scene = None
            cls.total_count = 0
            cls.color_count = 0

    def __init__(self, cal_res):
        if self.scene is None:
            self.create_scene()

        self.count()
        self.cal_res = cal_res
        init_dis_x = self.cal_res['dis_x_arr'][0] / 10
        init_dis_y = self.cal_res['dis_y_arr'][0] / 10

        self.ground = box(pos=vector(0, 0, 0), size=vector(
            20, 0.1, 8), color=color.green)
        self.ball = sphere(pos=vector(init_dis_x, init_dis_y, self.total_count - 1),
                           radius=0.2, color=self.color_list[self.color_count - 1], make_trail=True)

    def run_animation(self):
        delay_rate = 1 / self.cal_res['time_step']
        dis_x_arr = self.cal_res['dis_x_arr']
        dis_y_arr = self.cal_res['dis_y_arr']
        i = 0
        if self.scene.waitfor("keydown"):
            while i < len(dis_x_arr):
                rate(delay_rate)
                dis_x = dis_x_arr[i] / 10
                dis_y = dis_y_arr[i] / 10
                pos = vector(dis_x, dis_y, self.ball.pos.z)
                self.ball.pos = pos
                i += 1


class mpt_animation:
    def __init__(self, projectile):
        name = projectile.name
        cal_res = projectile.cal_res
        self.dis_x_arr = cal_res["dis_x_arr"]
        self.dis_y_arr = cal_res["dis_y_arr"]
        self.time_step = cal_res["time_step"] * 1000
        self.length = cal_res["length"]
        self.line, = plt.plot(self.dis_x_arr, self.dis_y_arr,label=name)
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

    @classmethod
    def run_animation(cls):
        plt.legend(loc='upper right')
        plt.show()
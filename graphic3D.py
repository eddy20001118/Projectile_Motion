from vpython import *
class animation_3d:
    scene = None
    color_list = [vector(1,0.85,0.73), vector(1,0.96,0.56), vector(1,0.27,0)]
    color_count = 0
    total_count = 0

    @classmethod
    def count(cls):
        if cls.color_count < 3:
            cls.color_count += 1
        else:
            cls.color_count = 0
        cls.total_count += 1

    @classmethod
    def create_scene(cls):
        cls.scene = canvas(width=1440,height=900)

    @classmethod
    def exit_animation(cls):
        if cls.scene.waitfor("keydown"):
            cls.scene.delete()
            cls.scene = None

    def __init__(self, cal_res):
        if self.scene is None:
            self.create_scene()

        self.count()
        self.cal_res = cal_res
        init_dis_x = self.cal_res['dis_x_arr'][0] / 10
        init_dis_y = self.cal_res['dis_y_arr'][0] / 10
        
        self.ground = box(pos=vector(0,0,0), size=vector(20,0.1,8), color=color.green)
        self.ball = sphere(pos=vector(init_dis_x,init_dis_y,self.total_count - 1), radius=0.2, color=self.color_list[self.color_count - 1], make_trail=True)

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
                pos = vector(dis_x,dis_y,self.ball.pos.z)
                self.ball.pos = pos
                i += 1

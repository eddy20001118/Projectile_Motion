from vpython import *
class animation_3d:
    cal_res = {}

    def __init__(self, cal_res):
        self.cal_res = cal_res
        init_dis_x = self.cal_res['dis_x_arr'][0] / 10
        init_dis_y = self.cal_res['dis_y_arr'][0] / 10
        scene = canvas(width=1440,height=900)
        scene.caption = "Projectile Motion Simulator"

        self.scene = scene
        self.ground = box(pos=vector(0,0,0), size=vector(20,0.2,1), color=color.green)
        self.ball = sphere(pos=vector(init_dis_x,init_dis_y,0), radius=0.2, color=vector(72/255,61/255,139/255), make_trail=True)

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
                pos = vector(dis_x,dis_y,0)
                self.ball.pos = pos
                i += 1
            print("Animation finished, press any key to exit")
        
        if self.scene.waitfor("keydown"):
            self.scene.delete()


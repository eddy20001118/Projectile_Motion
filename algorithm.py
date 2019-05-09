import numpy as np

class algo:
    grav = float(0.0)
    mass = float(0.0)
    ang = float(0.0)
    vel = float(0.0)
    dis_x = float(0.0)
    dis_y = float(0.0)
    drag_coef = float(0.0)
    time_step = float(0.0)
    total_time = float(0.0)
    
    def get_angle(self,x,y):
        if x == 0:
            return np.copysign(90, y)
        else:
            return np.degrees(np.arctan(y/x))

    def __init__(self, sys_params):
        self.grav = sys_params['grav']
        self.mass = sys_params['mass']
        self.ang = sys_params['ang']
        self.vel = sys_params['vel']
        self.dis_x = sys_params['dis_x']
        self.dis_y = sys_params['dis_y']
        self.drag_coef = sys_params['drag_coef']
        self.time_step = sys_params['time_step']
        self.total_time = sys_params['total_time']

    def execute(self):
        f_v = lambda self,t,a,v0: v0 + a*t
        f_d = lambda self,t,a,v0,d0: v0 * t + 0.5*a*(t**2) + d0

        grav = self.grav
        mass = self.mass
        drag_coef = self.drag_coef
        time_step = self.time_step
        total_time = self.total_time
        arr_length = int(total_time / time_step)

        ang = self.ang
        accel_x = 0
        accel_y = -grav
        vel_x = init_vel_x = np.cos(np.radians(ang)) * self.vel
        vel_y = init_vel_y = np.sin(np.radians(ang)) * self.vel
        dis_x = init_dis_x = self.dis_x
        dis_y = init_dis_y = self.dis_y

        time_arr = np.arange(0,total_time,time_step)
        accel_x_arr = np.zeros(arr_length)
        accel_y_arr = np.zeros(arr_length)
        vel_x_arr = np.zeros(arr_length)
        vel_y_arr = np.zeros(arr_length)
        dis_x_arr = np.zeros(arr_length)
        dis_y_arr = np.zeros(arr_length)
        ang_arr = np.zeros(arr_length)

        accel_x_arr[0] = accel_x
        accel_y_arr[0] = accel_y
        vel_x_arr[0] = vel_x
        vel_y_arr[0] = vel_y
        dis_x_arr[0] = dis_x
        dis_y_arr[0] = dis_y
        ang_arr[0] = ang

        contact_time = -1
        current_time = float(0.0)
        i = int(1)

        while i < len(time_arr):
            current_time = time_arr[i]

            drag_a_x = -(vel_x * np.abs(vel_x) * drag_coef) / mass
            drag_a_y = -(vel_x * np.abs(vel_x) * drag_coef) / mass

            accel_x = drag_a_x
            accel_y = - grav + drag_a_y
            vel_x = f_v(current_time,accel_x,init_vel_x)
            vel_y = f_v(current_time,accel_y,init_vel_y)
            dis_x = f_d(current_time,accel_x,init_vel_x,init_dis_x)
            dis_y = f_d(current_time,accel_y,init_vel_x,init_dis_y)
            ang = self.get_angle(vel_x,vel_y)

            if dis_y_arr[i-1] > 0 and dis_y < 0:
                contact_time = current_time
            
            accel_x_arr[i] = accel_x
            accel_y_arr[i] = accel_y
            vel_x_arr[i] = vel_x
            vel_y_arr[i] = vel_y
            dis_x_arr[i] = dis_x
            dis_y_arr[i] = dis_y
            ang_arr[i] = ang

            i += 1

        accel_x_arr = np.around(accel_x_arr,decimals=4)
        accel_y_arr = np.around(accel_y_arr,decimals=4)
        vel_x_arr = np.around(vel_x_arr,decimals=4)
        vel_y_arr = np.around(vel_y_arr,decimals=4)
        dis_x_arr = np.around(dis_x_arr,decimals=4)
        dis_y_arr = np.around(dis_y_arr,decimals=4)
        ang_arr = np.around(ang_arr,decimals=4)
        time_arr = np.around(time_arr,decimals=2)

        # Summarise key information
        max_height = np.max(dis_y_arr)
        min_height = np.min(dis_y_arr)
        max_dis_x = np.max(dis_x_arr)
        min_dis_x = np.min(dis_x_arr)
        length = time_arr.size

        cal_res = {
            "accel_y_arr": list(accel_y_arr),
            "accel_x_arr": list(accel_x_arr),
            "vel_y_arr": list(vel_y_arr),
            "vel_x_arr": list(vel_x_arr),
            "dis_y_arr": list(dis_y_arr),
            "dis_x_arr": list(dis_x_arr),
            "ang_arr": list(ang_arr),
            "time_arr": list(time_arr),
            "length": length,
            "max_height": max_height,
            "min_height": min_height,
            "max_dis_x": max_dis_x,
            "min_dis_x": min_dis_x,
            "contact_time": contact_time,
            "time_step": time_step,
            "is_calculated": True
        }
        return cal_res

def main():
    input_params = {
        "grav" : 9.81,
        "mass" : 1,
        "ang" : 60,
        "vel" : 10,
        "dis_x" : 0,
        "dis_y" : 20,
        "drag_coef" : 0.0,
        "time_step" : 0.001,
        "total_time" : 5
    }
    al = algo(input_params)
    cal_res = al.execute()

if __name__ == "__main__":
    main()
import numpy as np

class algorithm:
    grav = float(0.0)
    mass = float(0.0)
    ang = float(0.0)
    vel = float(0.0)
    dis_x = float(0.0)
    dis_y = float(0.0)
    drag_coef = float(0.0)
    time_step = float(0.0)
    total_time = float(0.0)

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
        grav = self.grav
        mass = self.mass
        drag_coef = self.drag_coef
        time_step = self.time_step
        total_time = self.total_time
        time_arr = np.arange(0,total_time,time_step)
        arr_length = time_arr.size
        f_drag = lambda vel : -((vel * np.abs(vel) * drag_coef) / mass)
        f_ang = lambda x,y : np.degrees(np.arctan(y/x)) if x != 0 else np.copysign(90, y)

        ang = self.ang
        accel_x = 0
        accel_y = -grav
        vel_x = np.around( np.cos(np.radians(ang)) * self.vel, decimals=4)
        vel_y = np.around( np.sin(np.radians(ang)) * self.vel, decimals=4)
        dis_x = self.dis_x
        dis_y = self.dis_y

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

        while i < arr_length:
            current_time = time_arr[i]

            drag_a_x = f_drag(vel_x)
            drag_a_y = f_drag(vel_y)

            accel_x = drag_a_x
            accel_y = - grav + drag_a_y

            vel_x += time_step * accel_x
            vel_y += time_step * accel_y
            dis_x += time_step * vel_x
            dis_y += time_step * vel_y
            ang = f_ang(vel_x,vel_y)

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

        # Summarise key information
        max_height = np.max(dis_y_arr)
        min_height = np.min(dis_y_arr)
        max_dis_x = np.max(dis_x_arr)
        min_dis_x = np.min(dis_x_arr)

        cal_res = {
            "accel_y_arr": np.around(accel_y_arr, decimals=4),
            "accel_x_arr": np.around(accel_x_arr, decimals=4),
            "vel_y_arr": np.around(vel_y_arr, decimals=4),
            "vel_x_arr": np.around(vel_x_arr, decimals=4),
            "dis_y_arr": np.around(dis_y_arr, decimals=4),
            "dis_x_arr": np.around(dis_x_arr, decimals=4),
            "ang_arr": np.around(ang_arr, decimals=4),
            "time_arr": np.around(time_arr, decimals=2),
            "length": arr_length,
            "max_height": max_height,
            "min_height": min_height,
            "max_dis_x": max_dis_x,
            "min_dis_x": min_dis_x,
            "contact_time": contact_time,
            "time_step": time_step,
            "is_calculated": True
        }
        return cal_res
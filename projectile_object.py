import traceback
import os
run_programme = False


try:
    import numpy as np
    import matplotlib.pyplot as plt

    from matplotlib import animation
    from prettytable import PrettyTable
    run_programme = True
except ModuleNotFoundError:
    print(traceback.format_exc())
    input("Press any key to continue")


class projectile_object:
    object_list = []
    params_prompt_list = ["Mass", "Angle", "Velocity", "Initial displacement x",
                          "Initial displacement y", "Drag coef", "Enable ground [T/F]",
                          "Restitution coef", "Time step", "Total time"]

    params_key_list = ["mass", "ang", "vel", "dis_x", "dis_y", "drag_coef",
                       "en_g", "rst_coef", "time_step", "total_time"]

    file_save_path = "./results/"

    @classmethod
    def add_to_list(cls, this):
        cls.object_list.append(this)

    @classmethod
    def remove_from_list(cls, this):
        cls.object_list.remove(this)

    @classmethod
    def remove_all(cls):
        cls.object_list = []

    def __init__(self, name, head_menu_callback):
        self.name = name
        self.sys_params = {
            "grav": float(9.81),
            "mass": float(1.0),
            "ang": float(60.0),
            "vel": float(10.0),
            "dis_x": float(0.0),
            "dis_y": float(2.0),
            "drag_coef": float(0.0025),
            "en_g": True,
            "rst_coef": float(0.85),
            "time_step": float(0.02),
            "total_time": float(12.0)
        }
        self.cal_res = {  # Output result variable
            "is_calculated": False
        }
        self.add_to_list(self)
        self.print_head_menu = head_menu_callback

    def __repr__(self):
        return "{:s} : {:s}".format("Object", self.name)

    def print_param_menu(self):
        # This function is to print the parameter menu in the console
        self.print_head_menu()
        print("+----------------------------------------------------------+")
        print("|{:^58s}|".format("Parameters Info"))
        print("+----------------------------------------------------------+")
        print("| 1. Mass: {:<47s} |".format(
            str(self.sys_params["mass"])+" (kg)"))
        print("| 2. Angle: {:<46s} |".format(
            str(self.sys_params["ang"])+" (deg)"))
        print("| 3. Velocity: {:<43s} |".format(
            str(self.sys_params["vel"])+" (m/s)"))
        print("| 4. Initial displacement x: {:<29s} |".format(
            str(self.sys_params["dis_x"])+" (m)"))
        print("| 5. Initial displacement y: {:<29s} |".format(
            str(self.sys_params["dis_y"])+" (m)"))
        print("| 6. Drag coef: {:<42s} |".format(
            str(self.sys_params["drag_coef"])))
        print("| 7. Enable ground: {:<38s} |".format(
            str(self.sys_params["en_g"])))
        print("| 8. Restitution coef: {:<35s} |".format(
            str(self.sys_params["rst_coef"])))
        print("| 9. Time step: {:<42s} |".format(
            str(self.sys_params["time_step"])+" (s)"))
        print("| 10. Total time: {:<40s} |".format(
            str(self.sys_params["total_time"])+" (s)"))
        print("| Quit -- q {:<46s} |".format(""))
        print("+----------------------------------------------------------+\n")

    def set_single_param(self, prompt, key):
        # This function is for setting the parameters
        # inputs:	hint 	        (string)		        the hint for the input
        #           default 	    (float)		            default value
        #           index           (int)                   index of options
        #
        # outputs:  exit_code       (string)                exit code of the function

        res = float(0)
        sys_params = self.sys_params
        default = sys_params[key]

        try:
            param_input = input(prompt)
            if param_input is "q":
                self.sys_params = sys_params
                return "interrupt"

            elif param_input is "":
                sys_params[key] = default

            elif param_input is not "":

                if key is "en_g":
                    if param_input is "T" or param_input is "t":
                        res = True
                    elif param_input is "F" or param_input is "f":
                        res = False
                    else:
                        raise ValueError()
                else:
                    res = float(param_input)
                    if (key is "mass" or key is "time_step" or key is "total_time") and res == 0:
                        raise ValueError()

                sys_params[key] = res
                self.cal_res["is_calculated"] = False

            # Refresh the parameter menu every time when a parameter is set.
            self.sys_params = sys_params
            self.print_param_menu()
            return "normal-quit"

        except ValueError:
            print("Invalid input, try again")
            time.sleep(1)
            self.print_param_menu()
            # Internal call for inputting one more time
            self.set_single_param(prompt, key)

    def set_params(self):
        exit_code = ""
        i = 0
        self.print_param_menu()

        while i < len(self.params_key_list) and exit_code is not "interrupt":
            prompt = "Option[{:d}] - {:s}: ".format(
                i+1, self.params_prompt_list[i])
            exit_code = self.set_single_param(
                prompt, self.params_key_list[i])
            i += 1
        
        if exit_code is not "interrupt":
            input("Parameters set, press any key to continue")

    def calculate(self):
        grav = self.sys_params["grav"]
        mass = self.sys_params["mass"]
        ang = self.sys_params["ang"]
        vel = self.sys_params["vel"]
        drag_coef = self.sys_params["drag_coef"]
        enable_ground = self.sys_params["en_g"]
        rst_coef = self.sys_params["rst_coef"]
        time_step = self.sys_params["time_step"]
        total_time = self.sys_params["total_time"]
        time_arr = np.arange(0, total_time, time_step)
        arr_length = time_arr.size
        accel_x = 0
        accel_y = -grav
        vel_x = np.around(np.cos(np.radians(ang)) * vel, decimals=4)
        vel_y = np.around(np.sin(np.radians(ang)) * vel, decimals=4)
        dis_x = self.sys_params["dis_x"]
        dis_y = self.sys_params["dis_y"]
        bouncing_finish = False

        def f_drag(vel): return -((vel * np.abs(vel) * drag_coef) / mass)

        def f_ang(x, y): return np.degrees(
            np.arctan(y/x)) if x != 0 else np.copysign(90, y)

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
            accel_x = drag_a_x
            vel_x += time_step * accel_x
            dis_x += time_step * vel_x

            if not bouncing_finish:
                drag_a_y = f_drag(vel_y)
                accel_y = - grav + drag_a_y
                vel_y += time_step * accel_y
                dis_y += time_step * vel_y
                ang = f_ang(vel_x, vel_y)
            else:
                vel_y = 0
                dis_y = 0
                ang = 0

            if dis_y_arr[i-1] > 0 and dis_y < 0:
                if contact_time == -1:
                    contact_time = current_time  # first time contacting the ground

                if enable_ground:
                    dis_y = 0
                    vel_y = -vel_y * rst_coef
                    if -0.5 < vel_y < 0.5:
                        bouncing_finish = True

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

        self.cal_res = {
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

    def print_res_table(self):
        cal_res = self.cal_res

        # Preview table
        table = PrettyTable()
        table.add_column("Time", cal_res["time_arr"][:20])
        table.add_column("Accel_X", cal_res["accel_x_arr"][:20])
        table.add_column("Accel_Y", cal_res["accel_y_arr"][:20])
        table.add_column("Vel_X", cal_res["vel_x_arr"][:20])
        table.add_column("Vel_Y", cal_res["vel_y_arr"][:20])
        table.add_column("Dis_X", cal_res["dis_x_arr"][:20])
        table.add_column("Dis_Y", cal_res["dis_y_arr"][:20])
        table.add_column("Angle", cal_res["ang_arr"][:20])
        list_len = len(cal_res["time_arr"][:20])

        print(table)
        print("First {:d} result points printed\n".format(list_len))
        input("Press any key to continue")

    def print_summary(self):
        cal_res = self.cal_res

        # Summary block
        max_height = cal_res["max_height"]
        min_height = cal_res["min_height"]
        max_dis_x = cal_res["max_dis_x"]
        min_dis_x = cal_res["min_dis_x"]
        data_points = cal_res["length"]
        contact_time = cal_res["contact_time"]
        if contact_time == -1:
            contact_time = "Not contact"

        print("+----------------------------------------------------------+")
        print("|{:^58s}|".format("Summary of object "+self.name))
        print("+----------------------------------------------------------+")
        print("| 1. Maximum height: {:<38.2f}|".format(max_height))
        print("| 2. Minimum height: {:<38.2f}|".format(min_height))
        print(
            "| 3. Maximum horizontal displacement: {:<21.2f}|".format(max_dis_x))
        print(
            "| 4. Minimum horizontal displacement: {:<21.2f}|".format(min_dis_x))
        print("| 5. Number of data points: {:<31.2f}|".format(data_points))
        print("| 6. Contact ground time: {:<33s}|".format(str(contact_time)))
        print("+----------------------------------------------------------+\n")
        input("Press any key to continue")

    def save_to_csv(self):
        user_option = ""
        full_path = self.file_save_path + self.name + ".csv"
        if self.cal_res["is_calculated"]:
            if not os.path.isdir(self.file_save_path):
                os.makedirs(self.file_save_path)

            if os.path.isfile(full_path):
                user_option = input(
                    "{:s}.csv already exists, do you wish to overwrite it ? [Y/N]: ".format(self.name))

            if (user_option == "y" or user_option == "Y") or not os.path.isfile(full_path):
                cal_res = self.cal_res
                # open a file with "write" mode
                f = open(full_path, "w")

                # write the head
                f.write("time,accel_x,accel_y,vel_x,vel_y,dis_x,dis_y,ang\n")

                # unpack the result package
                time_arr = cal_res["time_arr"]
                accel_x_arr = cal_res["accel_x_arr"]
                accel_y_arr = cal_res["accel_y_arr"]
                vel_x_arr = cal_res["vel_x_arr"]
                vel_y_arr = cal_res["vel_y_arr"]
                dis_x_arr = cal_res["dis_x_arr"]
                dis_y_arr = cal_res["dis_y_arr"]
                ang_arr = cal_res["ang_arr"]

                i = 0

                # write all results
                while i < len(time_arr):
                    csv_format = "{:.2f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}\n"
                    next_line = csv_format.format(time_arr[i], accel_x_arr[i], accel_y_arr[i],
                                                  vel_x_arr[i], vel_y_arr[i], dis_x_arr[i], dis_y_arr[i], ang_arr[i])
                    f.write(next_line)
                    i += 1

                # close the file after finished
                f.close()
            else:
                print("{:s}.csv was not saved.".format(self.name))

    def add_animation(self):
        def init():
            return line, dot,

        def animate(i):
            line.set_data(dis_x_arr[:i], dis_y_arr[:i])
            dot.set_data(dis_x_arr[i], dis_y_arr[i])
            return line, dot,

        name = self.name
        cal_res = self.cal_res
        dis_x_arr = cal_res["dis_x_arr"]
        dis_y_arr = cal_res["dis_y_arr"]
        time_step = cal_res["time_step"] * 1000
        length = cal_res["length"]
        line, = plt.plot(dis_x_arr, dis_y_arr, ls='--', label=name)
        dot, = plt.plot([], [], "ro")
        self.ani = animation.FuncAnimation(fig=plt.figure(1),
                                           frames=length,
                                           func=animate,
                                           init_func=init,
                                           interval=time_step,
                                           blit=False,
                                           repeat=False)

    @classmethod
    def run_animation(cls):
        try:
            for ob in cls.object_list:
                ob.add_animation()

            plt.legend(loc='upper right')
            plt.grid()
            plt.xlabel("displacement x (m)")
            plt.ylabel("displacement y (m)")
            plt.title("Projectile Motion Simulator")
            plt.show()
        except:
            pass

    @classmethod
    def plot_single_graph(cls, title, x_label, y_label, x_key, y_key):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()

        for ob in cls.object_list:

            cal_res = ob.cal_res
            is_calculated = cal_res["is_calculated"]

            if is_calculated:
                x_data = cal_res[x_key]
                y_data = cal_res[y_key]
                plt.plot(x_data, y_data, label=ob.name)

                # Plot the maximum point
                if y_key is "dis_y_arr":
                    max_y = np.max(y_data)
                    index_y = list(y_data).index(max_y)
                    max_x = x_data[index_y]
                    plt.plot(max_x, max_y, 'ro')
                    plt.text(max_x, max_y, "Highest Point")
                plt.legend(loc='upper right')

    @classmethod
    def plot_graphs(cls, index):
        if index is "1":
            cls.plot_single_graph("Acceleration x", "time (s)",
                                  "acceleration (m/s^2)", "time_arr", "accel_x_arr")
        elif index is "2":
            cls.plot_single_graph("Acceleration y", "time (s)",
                                  "acceleration (m/s^2)", "time_arr", "accel_y_arr")
        elif index is "3":
            cls.plot_single_graph("Velocity x", "time (s)",
                                  "velocity (m/s)", "time_arr", "vel_x_arr")
        elif index is "4":
            cls.plot_single_graph("Velocity y", "time (s)",
                                  "velocity (m/s)", "time_arr", "vel_y_arr")
        elif index is "5":
            cls.plot_single_graph("Displacement x", "time (s)",
                                  "displacement (m)", "time_arr", "dis_x_arr")
        elif index is "6":
            cls.plot_single_graph("Displacement y", "time (s)",
                                  "displacement (m)", "time_arr", "dis_y_arr")
        elif index is "7":
            cls.plot_single_graph("Displacement", "displacement x (m)",
                                  "displacement x (m)", "dis_x_arr", "dis_y_arr")
        elif index is "8":
            cls.plot_single_graph("Angle", "time (s)",
                                  "angle (deg)", "time_arr", "ang_arr")
        elif index is "9":
            plt.suptitle("Projectile Motion Simulator", fontsize=16)
            plt.subplot(2, 2, 1)
            cls.plot_single_graph("Velocity x", "time (s)",
                                  "velocity (m/s)", "time_arr", "vel_x_arr")

            plt.subplot(2, 2, 2)
            cls.plot_single_graph("Velocity y", "time (s)",
                                  "velocity (m/s)", "time_arr", "vel_y_arr")

            plt.subplot(2, 2, 3)
            cls.plot_single_graph("Displacement", "displacement x (m)",
                                  "displacement y (m)", "dis_x_arr", "dis_y_arr")

            plt.subplot(2, 2, 4)
            cls.plot_single_graph("Angle", "time (s)",
                                  "angle (deg)", "time_arr", "ang_arr")

            plt.subplots_adjust(wspace=0.5, hspace=0.5)

        elif index is "q":
            return

        plt.show()

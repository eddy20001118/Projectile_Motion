from graphic import animation_3d, mpt_animation
from prettytable import PrettyTable

import matplotlib.pyplot as plt
import numpy as np
import os
import time


class projectile_object:
    object_list = []
    params_prompt_list = ["Mass", "Angle", "Velocity", "Initial displacement x",
                          "Initial displacement y", "Drag coef", "Time step", "Total time"]
    params_key_list = ["mass", "ang", "vel", "dis_x",
                       "dis_y", "drag_coef", "time_step", "total_time"]
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
            "dis_y": float(30.0),
            "drag_coef": float(0.0025),
            "time_step": float(0.02),
            "total_time": float(3.0)
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
        print("| 1. Mass: {:<47s} |".format(str(self.sys_params["mass"])+" (kg)"))
        print("| 2. Angle: {:<46s} |".format(str(self.sys_params["ang"])+" (deg)"))
        print("| 3. Velocity: {:<43s} |".format(str(self.sys_params["vel"])+" (m/s)"))
        print("| 4. Initial displacement x: {:<29s} |".format(str(self.sys_params["dis_x"])+" (m)"))
        print("| 5. Initial displacement y: {:<29s} |".format(str(self.sys_params["dis_y"])+" (m)"))
        print("| 6. Drag coef: {:<42s} |".format(str(self.sys_params["drag_coef"])))
        print("| 7. Time step: {:<42s} |".format(str(self.sys_params["time_step"])+" (s)"))
        print("| 8. Total time: {:<41s} |".format(str(self.sys_params["total_time"])+" (s)"))
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
                res = float(param_input)

                if (key == "mass" or key == "time_step" or key == "total_time") and res == 0:
                    raise ValueError()

                if sys_params["ang"] != 0 and sys_params["vel"] == 0:
                    print(
                        "\nWarning: Velocity is set to 0, angle in any value would not take effects\n")
                    input("Press any key to continue")

                sys_params[key] = res
                self.cal_res["is_calculated"] = False

            # Refresh the parameter menu every time when a parameter is set.
            self.sys_params = sys_params
            self.print_param_menu()
            return "normal-quit"

        except ValueError:
            print("Invalid input, try again")
            time.sleep(1)
            self.print_param_menu(sys_params)
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

    def calculate(self):
        f_drag = lambda vel : -((vel * np.abs(vel) * drag_coef) / mass)
        f_ang = lambda x,y : np.degrees(np.arctan(y/x)) if x != 0 else np.copysign(90, y)

        grav = self.sys_params["grav"]
        mass = self.sys_params["mass"]
        ang = self.sys_params["ang"]
        vel = self.sys_params["vel"]
        drag_coef = self.sys_params["drag_coef"]
        time_step = self.sys_params["time_step"]
        total_time = self.sys_params["total_time"]
        time_arr = np.arange(0,total_time,time_step)
        arr_length = time_arr.size
        accel_x = 0
        accel_y = -grav
        vel_x = np.around( np.cos(np.radians(ang)) * vel, decimals=4)
        vel_y = np.around( np.sin(np.radians(ang)) * vel, decimals=4)
        dis_x = self.sys_params["dis_x"]
        dis_y = self.sys_params["dis_y"]

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
        self.cal_res = cal_res

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
                self.is_saved = True

    @classmethod
    def run_animation(cls):
        for ob in cls.object_list:
            ob.animation = mpt_animation(ob)
        mpt_animation.run_animation()
        
    @classmethod
    def plot_single_graph(cls, title, x_label, y_label, x_key, y_key):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)

        for ob in cls.object_list:

            cal_res = ob.cal_res
            is_calculated = cal_res["is_calculated"]

            if is_calculated:
                x_data = cal_res[x_key]
                y_data = cal_res[y_key]
                plt.plot(x_data, y_data, label=ob.name)
                plt.legend(loc='upper right')

    @classmethod
    def plot_graphs(cls, index):
        if index is "1":
            cls.plot_single_graph("Acceleration x", "time (s)",
                                  "accel (m/s^2)", "time_arr", "accel_x_arr")
        elif index is "2":
            cls.plot_single_graph("Acceleration y", "time (s)",
                                  "accel (m/s^2)", "time_arr", "accel_y_arr")
        elif index is "3":
            cls.plot_single_graph("Velocity x", "time (s)",
                                  "vel (m/s)", "time_arr", "vel_x_arr")
        elif index is "4":
            cls.plot_single_graph("Velocity y", "time (s)",
                                  "vel (m/s)", "time_arr", "vel_y_arr")
        elif index is "5":
            cls.plot_single_graph("Displacement x", "time (s)",
                                  "dis (m)", "time_arr", "dis_x_arr")
        elif index is "6":
            cls.plot_single_graph("Displacement y", "time (s)",
                                  "dis (m)", "time_arr", "dis_y_arr")
        elif index is "7":
            cls.plot_single_graph("Displacement", "dis x (m)",
                                  "dis x (m)", "dis_x_arr", "dis_y_arr")
        elif index is "8":
            cls.plot_single_graph("Angle", "time (s)",
                                  "ang (deg)", "time_arr", "ang_arr")
        elif index is "9":
            plt.suptitle("Pendulum Simulator", fontsize=16)
            plt.subplot(2, 2, 1)
            cls.plot_single_graph("Velocity x", "time (s)",
                                  "vel (m/s)", "time_arr", "vel_x_arr")

            plt.subplot(2, 2, 2)
            cls.plot_single_graph("Velocity y", "time (s)",
                                  "vel (m/s)", "time_arr", "vel_y_arr")

            plt.subplot(2, 2, 3)
            cls.plot_single_graph("Displacement", "dis x (m)",
                                  "dis y (m)", "dis_x_arr", "dis_y_arr")

            plt.subplot(2, 2, 4)
            cls.plot_single_graph("Angle", "time (s)",
                                  "ang (deg)", "time_arr", "ang_arr")

            plt.subplots_adjust(wspace=0.5, hspace=0.5)

        elif index is "q":
            return

        plt.show()

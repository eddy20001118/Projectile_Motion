from algorithm import algorithm
from graphic3D import animation_3d
from prettytable import PrettyTable
from vpython import *

import matplotlib.pyplot as plt
import os
import time


class projectile_object:
    object_list = []
    params_prompt_list = ["Mass", "Angle", "Velocity", "Initial displacement x",
                            "Initial displacement y", "Drag coef", "Time step", "Total time"]
    params_key_list = ["mass", "ang", "vel", "dis_x",
                        "dis_y", "drag_coef", "time_step", "total_time"]

    cal_res = {  # Output result variable
        "is_calculated": False
    }

    name = ""
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

    def __init__(self, name):
        self.name = name
        sys_params = {
            "grav": float(9.81),
            "mass": float(1.0),
            "ang": float(60.0),
            "vel": float(10.0),
            "dis_x": float(0.0),
            "dis_y": float(30.0),
            "drag_coef": float(0.0),
            "time_step": float(0.02),
            "total_time": float(3.0)
        }
        self.sys_params = sys_params
        self.add_to_list(self)

    def __repr__(self):
        return "{:s} : {:s}".format("Object", self.name)

    def set_single_param(self,prompt,key,refresh_menu_callback):
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
                        "\nWarning: Velocity is set to 0, angle in any value would not take effect\n")
                    input("Press any key to continue")

                sys_params[key] = res
                self.cal_res["is_calculated"] = False

            # Refresh the parameter menu every time when a parameter is set.
            refresh_menu_callback(sys_params)
            self.sys_params = sys_params
            return "normal-quit"

        except ValueError:
            print("Invaild input, try again")
            time.sleep(1)
            refresh_menu_callback(sys_params)
            # Internal call for inputting one more time
            self.set_single_param(prompt, key, refresh_menu_callback)

    def set_params(self, refresh_menu_callback):
        exit_code = ""
        i = 0
        refresh_menu_callback(self.sys_params)

        while i < len(self.params_key_list) and exit_code is not "interrupt":
            prompt = "Option[{:d}] - {:s}: ".format(i+1, self.params_prompt_list[i])
            exit_code = self.set_single_param(prompt, self.params_key_list[i], refresh_menu_callback)
            i += 1

    def calculate(self):
        algo = algorithm(self.sys_params)
        cal_res = algo.execute()
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

    def save_to_csv(self, path, name):
        user_option = ""
        full_path = path + name + ".csv"

        if not os.path.isdir(path):
            os.makedirs(path)
            
        if os.path.isfile(full_path):
            user_option = input("File already exists, do you wish to overwrite it ? [Y/N]: ")

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
            input("Saving complete, press any key to continue")

    @classmethod
    def run_animation(cls):
        for ob in cls.object_list:
            cal_res = ob.cal_res
            ob.animation = animation_3d(cal_res)
        
        for ob in cls.object_list:
            ob.animation.run_animation()

        animation_3d.exit_animation()


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

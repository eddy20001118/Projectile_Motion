# DUISC Advanced Physics Project
# Projectile Motion Simulator
# Yuhao Li 2019
import os
import traceback
import platform
import math
from graphic3D import animation_3d
from algorithm import algo
run_programme = True


try:
    import matplotlib.pyplot as plt
    from prettytable import PrettyTable
    from graphics import *
except ModuleNotFoundError:
    print(traceback.format_exc())
    input("Press any key to continue")
    run_programme = False

# Check platform
sys_info = platform.system()

# console clear command
if sys_info is "Windows":
    sys_clear = "CLS"
else:
    sys_clear = "clear"

# Initialise global prompts
title = "DUISC Advanced Physics Project"
author_copyright = "Yuhao Li 2019"
name = "Projectile Motion Simulator"

# Default input parameters
sys_params = {
    "grav": float(9.81),
    "mass": float(1.0),
    "ang": float(60.0),
    "vel": float(10.0),
    "dis_x": float(0.0),
    "dis_y": float(20.0),
    "drag_coef": float(0.001),
    "time_step": float(0.02),
    "total_time": float(5.0)
}


def print_head_title():
    os.system(sys_clear)
    print(title)
    print(author_copyright)
    print(name+"\n")


def print_main_menu():
    # This function is to print the main menu in the console

    print_head_title()
    print("+-------------------------------------------+")
    print("|{:^43s}|".format("Main menu"))
    print("+-------------------------------------------+")
    print("| {:<42s}|".format("1. Edit params"))
    print("| {:<42s}|".format("2. Calculate"))
    print("| {:<42s}|".format("3. Plot data"))
    print("| {:<42s}|".format("4. Save to CSV"))
    print("| {:<42s}|".format("5. Open 2-D simulator"))
    print("| {:<42s}|".format("Quit -- q"))
    print("+-------------------------------------------+\n")


def print_param_menu(sys_params):
    # This function is to print the parameter menu in the console

    print_head_title()
    print("+----------------------------------------------------------+")
    print("|{:^58s}|".format("Parameters Info"))
    print("+----------------------------------------------------------+")
    print("| 1. Mass: {:<47s} |".format(str(sys_params["mass"])+" (kg)"))
    print("| 2. Angle: {:<46s} |".format(str(sys_params["ang"])+" (deg)"))
    print("| 3. Velocity: {:<43s} |".format(str(sys_params["vel"])+" (m/s)"))
    print("| 4. Initial displacement x: {:<29s} |".format(str(sys_params["dis_x"])+" (m)"))
    print("| 5. Initial displacement y: {:<29s} |".format(str(sys_params["dis_y"])+" (m)"))
    print("| 6. Drag coef: {:<42s} |".format(str(sys_params["drag_coef"])))
    print("| 7. Time step: {:<42s} |".format(str(sys_params["time_step"])+" (s)"))
    print("| 8. Total time: {:<41s} |".format(str(sys_params["total_time"])+" (s)"))
    print("| Quit -- q {:<46s} |".format(""))
    print("+----------------------------------------------------------+\n")


def print_plot_menu():
    # This function is to print ploting option menu in the console

    print_head_title()
    print("+----------------------------------------------------------+")
    print("|{:^58s}|".format("Plot options"))
    print("+----------------------------------------------------------+")
    print("| {:<56s} |".format("1. Print acceleration x"))
    print("| {:<56s} |".format("2. Print acceleration y"))
    print("| {:<56s} |".format("3. Print velocity x"))
    print("| {:<56s} |".format("4. Print velocity y"))
    print("| {:<56s} |".format("5. Print displacement x"))
    print("| {:<56s} |".format("6. Print displacement y"))
    print("| {:<56s} |".format("7. Print resultant displacement"))
    print("| {:<56s} |".format("8. Print angle"))
    print("| {:<56s} |".format("9. Print four summative graphs"))
    print("| {:<56s} |".format("Quit -- q"))
    print("+----------------------------------------------------------+\n")


def print_res_table(cal_res):
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
    print(table)

    list_len = len(cal_res["time_arr"][:20])
    return list_len


def set_param(hint, key, sys_params):
    # This function is for setting the parameters
    # inputs:	hint 	        (string)		        the hint for the input
    #           default 	    (float)		            default value
    #           index           (int)                   index of options
    #
    # outputs:  exit_code       (string)                exit code of the function

    res = float(0)
    local_sys_params = sys_params
    default = local_sys_params[key]
    exit_code = ""
    try:
        param_input = input(hint)
        if param_input is "q":
            exit_code = "interrupt"
            return exit_code, local_sys_params

        elif param_input is "":
            local_sys_params[key] = default

        elif param_input is not "":
            res = float(param_input)

            if (key == "mass" or key == "time_step" or key == "total_time") and res == 0:
                raise ValueError()

            if local_sys_params["ang"] != 0 and local_sys_params["vel"] == 0:
                print(
                    "\nWarning: Velocity is set to 0, angle in any value would not take effect\n")
                input("Press any key to continue")

            local_sys_params[key] = res

        # Refresh the parameter menu every time when a parameter is set.
        print_param_menu(sys_params)
        exit_code = "normal-quit"
        return exit_code, local_sys_params

    except ValueError:
        print("Invaild input, try again")
        time.sleep(1)
        os.system(sys_clear)
        print_param_menu(sys_params)
        # Internal call for inputting one more time
        set_param(hint, key, sys_params)


def accurate_calculation(sys_params):
    algorithm = algo(sys_params)
    cal_res = algorithm.execute()
    return cal_res


def plot_single_graph(title, x_label, y_label, x_data, y_data):
    # This function is for plotting a single graph using matplotlib
    # inputs:	title 	        (string)		        title of the graph
    #           x_label 	    (string)		        x label of the graph
    #           y_label         (string)                y label of the graph
    #           x_data          (list)                  data-list for x-axis
    #           y_data          (list)                  data-list for y-axis
    #
    # outputs:  res             (float)                 result value after value-check

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.plot(x_data, y_data)


def plot_data(cal_res, index):
    # This function is for plotting a selected graph using matplotlib
    # inputs:   cal_res         (object)                key-value set of the result
    #           index           (int)                   option for selecting a graph

    if index is 1:
        x_data = cal_res["time_arr"]
        y_data = cal_res["accel_x_arr"]
        plot_single_graph("Acceleration x", "time (s)",
                          "accel (m/s^2)", x_data, y_data)

    elif index is 2:
        x_data = cal_res["time_arr"]
        y_data = cal_res["accel_y_arr"]
        plot_single_graph("Acceleration y", "time (s)",
                          "accel (m/s^2)", x_data, y_data)

    elif index is 3:
        x_data = cal_res["time_arr"]
        y_data = cal_res["vel_x_arr"]
        plot_single_graph("Velocity x", "time (s)",
                          "vel (m/s)", x_data, y_data)

    elif index is 4:
        x_data = cal_res["time_arr"]
        y_data = cal_res["vel_y_arr"]
        plot_single_graph("Velocity y", "time (s)",
                          "vel (m/s)", x_data, y_data)

    elif index is 5:
        x_data = cal_res["time_arr"]
        y_data = cal_res["dis_x_arr"]
        plot_single_graph("Displacement x", "time (s)",
                          "dis (m)", x_data, y_data)

    elif index is 6:
        x_data = cal_res["time_arr"]
        y_data = cal_res["dis_y_arr"]
        plot_single_graph("Displacement y", "time (s)",
                          "dis (y)", x_data, y_data)

    elif index is 7:
        x_data = cal_res["dis_x_arr"]
        y_data = cal_res["dis_y_arr"]
        plot_single_graph("Displacement", "dis x (m)",
                          "dis y (m)", x_data, y_data)

    elif index is 8:
        x_data = cal_res["time_arr"]
        y_data = cal_res["ang_arr"]
        plot_single_graph("Angle", "time (s)", "ang (deg)", x_data, y_data)

    elif index is 9:
        plt.suptitle("Pendulum Simulator", fontsize=16)
        plt.subplot(2, 2, 1)
        x_data = cal_res["time_arr"]
        y_data = cal_res["vel_x_arr"]
        plot_single_graph("Velocity x", "time (s)",
                          "vel (m/s)", x_data, y_data)

        plt.subplot(2, 2, 2)
        x_data = cal_res["time_arr"]
        y_data = cal_res["vel_y_arr"]
        plot_single_graph("Velocity y", "time (s)",
                          "vel (m/s)", x_data, y_data)

        plt.subplot(2, 2, 3)
        x_data = cal_res["dis_x_arr"]
        y_data = cal_res["dis_y_arr"]
        plot_single_graph("Displacement", "dis x (m)",
                          "dis y (m)", x_data, y_data)

        plt.subplot(2, 2, 4)
        x_data = cal_res["time_arr"]
        y_data = cal_res["ang_arr"]
        plot_single_graph("Angle", "time (s)", "ang (deg)", x_data, y_data)

        plt.subplots_adjust(wspace=0.5, hspace=0.5)

    plt.ion()
    plt.show()


def print_res(cal_res):
    # This function is for previewing all the result in the terminal. It will print a
    # summary block and a table containing first 20 data points.
    # inputs:	cal_res	    (dictionary)        a dictionary that hold the all the result lists

    print_head_title()

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
    print("|{:^58s}|".format("Summary"))
    print("+----------------------------------------------------------+")
    print("| 1. Maximum height: {:<38.2f}|".format(max_height))
    print("| 2. Minimum height: {:<38.2f}|".format(min_height))
    print("| 3. Maximum horizontal displacement: {:<21.2f}|".format(max_dis_x))
    print("| 4. Minimum horizontal displacement: {:<21.2f}|".format(min_dis_x))
    print("| 5. Number of data points: {:<31.2f}|".format(data_points))
    print("| 6. Contact ground time: {:<33s}|".format(str(contact_time)))
    print("+----------------------------------------------------------+\n")

    list_len = print_res_table(cal_res)
    print("First {:d} result points printed\n".format(list_len))
    input("Press any key to continue")


def save_to_csv(cal_res):
    # This function is for saving all the result to a csv file.
    #
    # inputs:	cal_res         (object)                key-value set of the result

    print_head_title()
    print_res_table(cal_res)

    # open a file with "write" mode
    f = open("res.csv", "w")

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
    input("Press any key to continue")


def run_animation3D(cal_res):
    # animation_3d.clear_screen()
    test = animation_3d(cal_res)
    test.run_animation()


def main():
    input_options = ""  # Input option variable
    cal_res = {  # Output result variable
        "is_calculated": False
    }

    # Main loop starts
    while input_options is not "q":
        try:
            print_main_menu()
            input_options = input("Options: ")

            if input_options is "1":
                params_prompt_list = ["Mass", "Angle", "Velocity", "Initial displacement x",
                                      "Initial displacement y", "Drag coef", "Time step", "Total time"]
                params_key_list = ["mass", "ang", "vel", "dis_x",
                                   "dis_y", "drag_coef", "time_step", "total_time"]
                exit_code = ""
                i = 0
                print_param_menu(sys_params)
                while i < len(params_key_list) and exit_code is not "interrupt":
                    prompt = "Option[{:d}] - {:s}: ".format(
                        i+1, params_prompt_list[i])
                    exit_code = set_param(
                        prompt, params_key_list[i], sys_params)
                    i += 1
                cal_res["is_calculated"] = False

            elif input_options is "2":
                cal_res = accurate_calculation(sys_params)
                print_res(cal_res)

            elif input_options is "3":
                if not cal_res["is_calculated"]:
                    raise CalculationError()
                else:
                    while True:
                        try:
                            print_plot_menu()
                            sub_menu_input = input("Options: ")

                            if sub_menu_input == "":
                                pass
                            elif sub_menu_input == "q":
                                break
                            elif 1 <= int(sub_menu_input) <= 9:
                                plot_data(cal_res, int(sub_menu_input))
                            else:
                                raise ValueError()

                        except ValueError:
                            input("Invaild input, press any key to continue")

                        except Exception:
                            print(traceback.format_exc())
                            input("\n Press any key to continue")

            elif input_options is "4":
                if not cal_res["is_calculated"]:
                    raise CalculationError()
                else:
                    save_to_csv(cal_res)

            elif input_options is "5":
                if not cal_res["is_calculated"]:
                    raise CalculationError()
                else:
                    run_animation3D(cal_res)

            elif input_options is "q":
                pass
            elif input_options == "":
                pass
            else:
                raise ValueError()

        except ValueError:
            print(traceback.format_exc())
            input("Invaild input, press any key to continue")

        except CalculationError:
            input("Calculate first, press any key to continue")

        except Exception:
            print(traceback.format_exc())
            input("\n Press any key to continue")
        print("Exit the programme...")


class CalculationError(Exception):
    # Author-defined exception class
    pass


if __name__ == "__main__" and run_programme:
    main()

# DUISC Advanced Physics Project
# Projectile Motion Simulator
# Yuhao Li 2019
import os
import traceback
import platform
import math
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

# System constants
g_grav = 9.81  # gravitational acceleration

# Default input parameters
g_mass = float(1.0)  # mass (kg)
g_ang = float(60.0)  # initial angel to the horizontal CCW (deg)
g_height = float(20.0)
g_vel = float(10.0)
g_drag_coef = float(0.001)  # coefficient of drag force (5cm diameter sphere)
g_time_step = float(0.02)  # time step size (s)
g_total_time = float(5.0)  # total time for the simulation


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


def print_param_menu():
    # This function is to print the parameter menu in the console

    global g_mass, g_ang, g_height, g_vel, g_drag_coef, g_time_step, g_total_time
    print_head_title()
    print("+----------------------------------------------------------+")
    print("|{:^58s}|".format("Parameters Info"))
    print("+----------------------------------------------------------+")
    print("| 1. Mass: {:<47s} |".format(str(g_mass)+" (kg)"))
    print("| 2. Angle: {:<46s} |".format(str(g_ang)+" (deg)"))
    print("| 3. Height: {:<45s} |".format(str(g_height)+" (m)"))
    print("| 4. Velocity: {:<43s} |".format(str(g_vel)+" (m/s)"))
    print("| 5. Drag coef: {:<42s} |".format(str(g_drag_coef)))
    print("| 6. Time step: {:<42s} |".format(str(g_time_step)+" (s)"))
    print("| 7. Total time: {:<41s} |".format(str(g_total_time)+" (s)"))
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
    print("| {:<56s} |".format("9. Print four useful graphs"))
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


def set_param(hint, default, index):
    # This function is for setting the parameters
    # inputs:	hint 	        (string)		        the hint for the input
    #           default 	    (float)		            default value
    #           index           (int)                   index of options
    #
    # outputs:  exit_code       (string)                exit code of the function

    res = float(0)
    exit_code = ""
    try:
        param_input = input(hint)
        if param_input is "q":
            exit_code = "interrupt"
            return exit_code
        elif param_input is not "":
            res = float(param_input)

            # for the 1st,6th,7th option, the input value cannot be zero
            if (index is 1 or index is 6 or index is 7) and res == 0:
                raise ValueError()
        else:
            res = default

        global g_mass, g_ang, g_height, g_vel, g_drag_coef, g_time_step, g_total_time

        if index is 1:
            g_mass = res
        elif index is 2:
            if g_vel == 0:
                print(
                    "\nWarning: Velocity is set to 0, angle in any value would not take effect\n")
                input("Press any key to continue")
            g_ang = res
        elif index is 3:
            g_height = res
        elif index is 4:
            if g_ang != 0 and res == 0:
                print(
                    "\nWarning: Velocity is set to 0, angle in any value would not take effect\n")
                input("Press any key to continue")
            g_vel = res
        elif index is 5:
            g_drag_coef = res
        elif index is 6:
            g_time_step = res
        elif index is 7:
            g_total_time = res
        else:
            res = default

        # Refresh the parameter menu every time when a parameter is set.
        print_param_menu()
        exit_code = "normal-quit"
        return exit_code

    except ValueError as v:
        print("Invaild input, try again")
        time.sleep(1)
        os.system(sys_clear)
        print_param_menu()

        # Internal call for inputting one more time
        set_param(hint, default, index)


def execute(mass, ang, vel, height, drag_coef, time_step, total_time):
    # This function is for the main calculation
    # inputs:	mass 	        (float)		        Mass
    #           ang 	        (float)		        Angle for the ejection
    #           vel             (float)             Velocity
    #           height          (float)             Initial height
    #           drag_coef       (float)             Drag coefficient
    #           time_step       (float)             Time step
    #           total_time      (float)             Total time for the simulation
    #
    # outputs:  cal_res         (Object)            The key-value set that holds all the result lists

    init_ang = 0 if vel == 0 else ang
    # Resolving velocity vector
    vel_x = math.cos(math.radians(ang)) * vel
    vel_y = math.sin(math.radians(ang)) * vel

    # Initialise result-lists
    accel_x_arr = []
    accel_y_arr = []
    vel_y_arr = []
    vel_x_arr = []
    dis_y_arr = []
    dis_x_arr = []
    ang_arr = []
    time_arr = []

    # Append starting point
    accel_y_arr.append(float("%.4f" % -g_grav))
    accel_x_arr.append(float("%.4f" % 0.0))
    vel_y_arr.append(float("%.4f" % vel_y))
    vel_x_arr.append(float("%.4f" % vel_x))
    dis_y_arr.append(float("%.4f" % height))
    dis_x_arr.append(float("%.4f" % 0.0))
    ang_arr.append(float("%.4f" % init_ang))
    time_arr.append(float("%.2f" % 0.02))

    # Initial loop variables
    contact_time = "Not contact"
    time = float(0.0)
    index = int(0)

    while time < total_time:
        # Instant variables
        drag_accel_y = -(
            vel_y_arr[index] * math.fabs(vel_y_arr[index]) * drag_coef) / mass
        drag_accel_x = -(
            vel_x_arr[index] * math.fabs(vel_x_arr[index]) * drag_coef) / mass

        accel_y = - g_grav + drag_accel_y
        accel_x = drag_accel_x

        # variables for step i+1
        vel_y = vel_y_arr[index] + (accel_y * time_step)
        vel_x = vel_x_arr[index] + (accel_x * time_step)
        dis_y = dis_y_arr[index] + (vel_y * time_step)
        dis_x = dis_x_arr[index] + (vel_x * time_step)
        ang = 0.0
        if -0.00001 < vel_x < 0.00001:
            ang = math.copysign(90, vel_y)
        else:
            ang = math.degrees(math.atan(vel_y / vel_x))
        time = time_arr[index] + time_step

        if dis_y < 0 < dis_y_arr[index]:
            contact_time = time

        # append i+1 to lists
        accel_y_arr.append(float("%.4f" % accel_y))
        accel_x_arr.append(float("%.4f" % accel_x))
        vel_y_arr.append(float("%.4f" % vel_y))
        vel_x_arr.append(float("%.4f" % vel_x))
        dis_y_arr.append(float("%.4f" % dis_y))
        dis_x_arr.append(float("%.4f" % dis_x))
        ang_arr.append(float("%.4f" % ang))
        time_arr.append(float("%.2f" % time))

        index += 1

    # Summarise key information
    max_height = max(dis_y_arr)
    min_height = min(dis_y_arr)
    max_dis_x = max(dis_x_arr)
    min_dis_x = min(dis_x_arr)

    cal_res = {
        "accel_y_arr": accel_y_arr,
        "accel_x_arr": accel_x_arr,
        "vel_y_arr": vel_y_arr,
        "vel_x_arr": vel_x_arr,
        "dis_y_arr": dis_y_arr,
        "dis_x_arr": dis_x_arr,
        "ang_arr": ang_arr,
        "time_arr": time_arr,
        "max_height": max_height,
        "min_height": min_height,
        "max_dis_x": max_dis_x,
        "min_dis_x": min_dis_x,
        "contact_time": contact_time,
        "time_step": time_step,
        "is_calculated": True
    }

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

        plt.subplots_adjust(wspace=0.37, hspace=0.27)

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
    data_points = len(cal_res["time_arr"])
    contact_time = cal_res["contact_time"]

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


def run_animation(cal_res):
    # This function is for creating an animation GUI winodow for visualising the motion.
    # inputs:	cal_res	    (dictionary)        a dictionary that hold the all the result lists
    time_step = cal_res["time_step"]

    # Delay constants
    real_time_delay = 1
    other_msg_delay = 10

    # Loop counter for the delay
    real_time_loop_counter = 0
    other_msg_loop_counter = 0

    # System variables
    width = 800
    height = 600

    # Zero point
    zero_x = 100
    zero_y = height/2
    zero_point = Point(zero_x, zero_y)

    dis_x = cal_res["dis_x_arr"][0]
    dis_y = cal_res["dis_y_arr"][0]

    max_height = math.fabs(cal_res["max_height"])
    min_height = math.fabs(cal_res["min_height"])
    max_dis_x = math.fabs(cal_res["max_dis_x"])

    denominter_y = max_height if max_height > min_height else min_height

    x_scale_factor = float(0.0)
    if max_dis_x < (width-200) / 10:
        x_scale_factor = 4
    elif max_dis_x > (width-200):
        x_scale_factor = ((width - 200) / 2) / max_dis_x
    else:
        x_scale_factor = 1.0

    y_scale_factor = ((height/2)-100) / denominter_y

    # Initial object coordinate
    dx = zero_x + (dis_x * x_scale_factor)
    dy = zero_y - (dis_y * y_scale_factor)

    # Create a window
    win = GraphWin("ProjectileSIm", width, height)

    # Create object
    curve_point = Point(dx,dy)
    ball_object = Circle(curve_point, 10)
    ball_object.setFill(color_rgb(255, 230, 204))
    ball_object.setOutline(color_rgb(215, 155, 0))

    # Create axis
    x_axis = Line(zero_point, Point(width-zero_x, zero_y))
    y_axis = Line(Point(zero_x, 100), Point(zero_x, height-100))
    x_interval_line = Line(Point(x_scale_factor*10+zero_x,
                                 zero_y-10), Point(x_scale_factor*10+zero_x, zero_y))
    y_interval_line = Line(Point(
        zero_x+10, zero_y-y_scale_factor*10), Point(zero_x, zero_y-y_scale_factor*10))

    # Initialise on-screen messages
    title_msg = Text(Point(width/2, 60), name)
    author_msg = Text(Point(width/2, 80), author_copyright)
    press_continue_msg = Text(Point(width/2, 500), "Press any key to start!")
    ang_msg = Text(Point(720, 60), "ang : 0 deg")
    vel_msg = Text(Point(720, 80), "vel : 0 m/s")
    accel_msg = Text(Point(720, 100), "accel : 0 m/s^2")
    dis_msg = Text(Point(dx, dy+20), "(%.2f,%.2f)" % (dis_x, dis_y))
    sim_time_msg = Text(Point(720, 140), "sim time : 0 s")
    rt_time_msg = Text(Point(720, 160), "real time : 0 s")

    # Set font size
    title_msg.setSize(20)
    author_msg.setSize(16)

    # Draw elements
    x_axis.draw(win)
    y_axis.draw(win)
    x_interval_line.draw(win)
    y_interval_line.draw(win)
    ball_object.draw(win)
    title_msg.draw(win)
    author_msg.draw(win)
    press_continue_msg.draw(win)
    ang_msg.draw(win)
    vel_msg.draw(win)
    accel_msg.draw(win)
    dis_msg.draw(win)
    sim_time_msg.draw(win)
    rt_time_msg.draw(win)

    win.getKey()    # Start after a key press
    title_msg.undraw()
    author_msg.undraw()
    press_continue_msg.undraw()
    t_start = time.time()
    i = 0
    check_key = ""

    while(i < len(cal_res["time_arr"]) and check_key == ""):
        check_key = win.checkKey()

        if other_msg_loop_counter >= other_msg_delay:
            ang = cal_res["ang_arr"][i]
            accel_x = cal_res["accel_x_arr"][i]
            accel_y = cal_res["accel_y_arr"][i]
            vel_x = cal_res["vel_x_arr"][i]
            vel_y = cal_res["vel_y_arr"][i]
            vel_resultant = math.sqrt(vel_x*vel_x + vel_y*vel_y)
            accel_resultant = math.sqrt(accel_x*accel_x+accel_y*accel_y)

            ang_msg.setText("ang : %.4f deg" % ang)
            vel_msg.setText("vel : %.4f m/s" % vel_resultant)
            accel_msg.setText("accel : %.4f m/s^2" % accel_resultant)

            other_msg_loop_counter = 0

        if real_time_loop_counter >= real_time_delay:
            dis_x = cal_res["dis_x_arr"][i]
            dis_y = cal_res["dis_y_arr"][i]
            dx = zero_x + (dis_x * x_scale_factor)
            dy = zero_y - (dis_y * y_scale_factor)

            new_object = Circle(Point(dx, dy), 10)
            new_object.setFill(color_rgb(255, 230, 204))
            new_object.setOutline(color_rgb(215, 155, 0))
            new_dis_msg = Text(
                Point(dx, dy+20), "(%.2f,%.2f)" % (dis_x, dis_y))
            new_curve_point = Point(dx, dy)
            curve_line = Line(curve_point,new_curve_point)
            
            new_object.draw(win)
            new_dis_msg.draw(win)
            curve_line.draw(win)

            ball_object.undraw()
            dis_msg.undraw()
            ball_object = new_object
            curve_point = new_curve_point
            dis_msg = new_dis_msg

            real_time_loop_counter = 0

        t_now = time.time() - t_start
        sim_time_msg.setText("sim time : %f s" % cal_res["time_arr"][i])
        rt_time_msg.setText("real time : %f s" % t_now)

        if t_now > cal_res["time_arr"][i]:
            rt_time_msg.setTextColor("red")

        real_time_loop_counter += 1
        other_msg_loop_counter += 1
        time.sleep(time_step)
        i += 1


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
                params_prompt_list = ["Mass", "Angle", "Height",
                                      "Velocity", "Drag coef", "Time step", "Total time"]
                params_list = [g_mass, g_ang, g_height, g_vel,
                               g_drag_coef, g_time_step, g_total_time]
                exit_code = ""
                i = 0
                print_param_menu()
                while i < len(params_list) and exit_code is not "interrupt":
                    prompt = "Option[{:d}] - {:s}: ".format(
                        i+1, params_prompt_list[i])
                    exit_code = set_param(prompt, params_list[i], i+1)
                    i += 1
                cal_res["is_calculated"] = False

            elif input_options is "2":
                cal_res = execute(g_mass, g_ang, g_vel, g_height,
                                  g_drag_coef, g_time_step, g_total_time)
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
                    run_animation(cal_res)

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

# DUISC Programming Assignment 2 Part A
# Yuhao Li 2019

import math
import matplotlib.pyplot as plt
import os
import traceback
from graphics import *
from prettytable import PrettyTable

# Initialise global variables

# System contant, will not change
grav = 9.81     # gravitational coefficient
rad_deg_ratio = 57.29577951     # ratio for converting angle in radian to angle in degrees
deg_rad_ratio = 0.01745329      # ratio for converting angle in degrees to angle in radian

# Default simulation parameters, can be edited by user
mass = float(1.0)          # mass (kg)
length = float(1.0)        # length of the string (m)
drag_coef = float(0.1)     # coefficient of drag force
time_step = float(0.02)    # time step size (s)
initial_angle = float(30.0)  # initial angle (deg)
total_time = float(20.0)     # total time for the simulation (s)

def execute(mass, length, drag_coef, time_step, initial_angle, total_time):
    # This function is for the calculation
    # inputs:	mass 	        (float)		        mass of the object (kg)
    #           length          (float)             length of the string (m)
    #           drag_coef       (float)             coefficient of drag force
    #           time_step       (float)             time step size (s)
    #           initial_angle   (float)             initial angle (deg)
    #           total_time      (float)             total time for the simulation (s)
    #
    # outputs:  res             (dictionary)        a dictionary that holds all the result arrays

    # Result lists for holding the results
    ang_rad_arr = []
    ang_deg_arr = []
    vel_arr = []
    accel_arr = []
    dis_arr = []
    turn_point_arr = []
    time_arr = []

    # append the data for the starting point
    ang_deg_arr.append(initial_angle)
    # convert the initial angle to radian
    ang_rad_arr.append(initial_angle * deg_rad_ratio)
    vel_arr.append(0)
    accel_arr.append(0)
    dis_arr.append(0)
    turn_point_arr.append(True)
    time_arr.append(0.0)

    # index for the while loop
    index = 0
    time = 0.0

    while (time < total_time):
        tan_force = -1 * mass * grav * math.sin(ang_rad_arr[index])
        drag_force = vel_arr[index] * math.fabs(vel_arr[index]) * drag_coef

        # variables for step i+1
        accel = (tan_force - drag_force) / mass
        vel = vel_arr[index] + (accel * time_step)
        dis = dis_arr[index] + (vel * time_step)
        ang_rad = (dis / length) + ang_rad_arr[0]
        ang_deg = ang_rad * rad_deg_ratio
        time = time_arr[index] + time_step
        turn_point = True if vel * vel_arr[index] < 0 else False

        # append to the lists
        ang_deg_arr.append(float("%.4f" % ang_deg))
        ang_rad_arr.append(float("%.4f" % ang_rad))
        vel_arr.append(float("%.4f" % vel))
        accel_arr.append(float("%.4f" % accel))
        dis_arr.append(float("%.4f" % dis))
        turn_point_arr.append(turn_point)
        time_arr.append(float("%.4f" % time))

        index += 1

    # a dictionary that holds all the result arrays
    res = {
        'ang_deg_arr': ang_deg_arr,
        'ang_rad_arr': ang_rad_arr,
        'vel_arr': vel_arr,
        'accel_arr': accel_arr,
        'dis_arr': dis_arr,
        'turn_point_arr': turn_point_arr,
        'time_arr': time_arr
    }

    # return the dictionary
    return res


def plot_data(cal_res):
    # This function is for plottin all the results on a graph
    # inputs:	cal_res	    (dictionary)        a dictionary that hold the all the result lists

    # Plot four graphs using subplot

    # Plot angle graph at position 1
    plt.suptitle("Pendulum Simulator", fontsize=16)
    plt.subplot(2, 2, 1)
    plt.title("Angle")
    plt.plot(cal_res['time_arr'], cal_res['ang_deg_arr'])
    plt.xlabel('time(s)')
    plt.ylabel('angle(deg)')

    # Plot velocity graph at position 2
    plt.subplot(2, 2, 2)
    plt.title("Velocity")
    plt.plot(cal_res['time_arr'], cal_res['vel_arr'])
    plt.xlabel('time(s)')
    plt.ylabel('vel(m/s)')

    # Plot acceleration graph at position 3
    plt.subplot(2, 2, 3)
    plt.title("Acceleration")
    plt.plot(cal_res['time_arr'], cal_res['accel_arr'])
    plt.xlabel('time(s)')
    plt.ylabel('acc(m/s^2)')

    # Plot displacement graph at position 4
    plt.subplot(2, 2, 4)
    plt.title("Displacement")
    plt.plot(cal_res['time_arr'], cal_res['dis_arr'])
    plt.xlabel('time(s)')
    plt.ylabel('dis(m)')

    # Set the margin
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.ion()
    plt.show()


def print_params():
    # This function is for printing the parameters

    global mass, length, drag_coef, time_step, initial_angle, total_time

    os.system('clear')
    print("DUISC Programming Assignment 2 Part A")
    print("Yuhao Li 2019")
    print("Pendulum Simulator")
    print("\n")
    print("1. Mass: %s (kg)" % mass)
    print("2. Length: %s (m)" % length)
    print("3. Drag coef: %s" % drag_coef)
    print("4. Time step: %s (s)" % time_step)
    print("5. Initial angle: %s (deg)" % initial_angle)
    print("6. Total time: %s (s)" % total_time)


def set_params(hint, default):
    # This function is for setting the parameters
    # inputs:	hint 	        (string)		        the hint for the input
    #           default 	    (float)		            default value
    #
    # outputs:  res             (float)                 result value after value-check

    res = float(0)
    try:
        print('\n')
        param_input = input(hint)
        res = float(param_input)

    # Catch the wrong input
    except Exception:
        res = default

    finally:
        return res


def print_res(cal_res):
    # This function is for previewing all the result in the terminal. It is only for preview
    # as terminal usually has the output length limit, which may erase the pervious printing.
    #
    # inputs:	cal_res	    (dictionary)        a dictionary that hold the all the result lists

    if len(cal_res['time_arr']) >= 200:
        print('\n')

        # if these are too many datas, ask user whether wish to print
        print(
            "There are more than 200 lines of data, do you wish to print? Yes[Y] No[N]")
        yes_no_input = input("Options: ")

        if yes_no_input == 'Y' or yes_no_input == 'y':
            table = PrettyTable()
            table.add_column("Time", cal_res['time_arr'])
            table.add_column("Ang", cal_res['ang_deg_arr'])
            table.add_column("Vel", cal_res['vel_arr'])
            table.add_column("Accel", cal_res['accel_arr'])
            table.add_column("Dis", cal_res['dis_arr'])
            table.add_column("Turning_Point", cal_res['turn_point_arr'])
            print(table)
            input("\nPress any key to continue")


def save_to_csv(cal_res):
    # This function is for saving all the result to a csv file.
    #
    # inputs:	cal_res	    (dictionary)        a dictionary that hold the all the result lists

    # open a file with 'write' mode
    f = open("res.csv", "w")

    # write the title (first line)
    f.write("time,angle,vel,accel,dis,turn_point\n")

    # write all results
    for i in range(len(cal_res['time_arr'])):
        f.write("%.2f,%.4f,%.4f,%.4f,%.4f,%d\n" % (
            cal_res['time_arr'][i], cal_res['ang_deg_arr'][i], cal_res['vel_arr'][i], cal_res['accel_arr'][i], cal_res['dis_arr'][i], cal_res['turn_point_arr'][i]))

    # close the file after finished
    f.close()

    print("Data successfully saved to res.csv")


def run_GUI(cal_res):
    # This function is for creating an animation GUI winodow for visualising the motion.
    # inputs:	cal_res	    (dictionary)        a dictionary that hold the all the result lists

    delay_ratio = 1/100

    # Delay constants
    real_time_delay = time_step / delay_ratio
    other_msg_delay = 0.1 / delay_ratio  # delay for 0.1s

    # Loop counter for the delay
    real_time_loop_counter = 0
    other_msg_loop_count = 0

    # System variables
    width = 800
    height = 600
    radius = 150

    # Create a window
    win = GraphWin("PendulumSim", width, height)

    # Draw the main circle which its arc to be the path of the object
    circle = Circle(Point(width/2, height/2), radius)
    circle.setFill(color_rgb(255,230,204))
    circle.setOutline(color_rgb(215,155,0))

    # Get the center point coordinate
    center_x = circle.getCenter().getX()
    center_y = circle.getCenter().getY()

    # Draw a small circle to be the fixed point of the line
    centerPoint = Circle(circle.getCenter(), 5)
    centerPoint.setFill(color_rgb(218,232,252))
    centerPoint.setOutline(color_rgb(108,142,191))

    # Calculate the initial coordinate of the object
    dx = center_x + (radius * math.sin(cal_res['ang_rad_arr'][0]))
    dy = center_y + (radius * math.cos(cal_res['ang_rad_arr'][0]))

    # Create a line to connect the object and the fixed point
    line = Line(circle.getCenter(), Point(dx, dy))
    line.setOutline(color_rgb(102,102,102))

    # Create mass object
    new_mass = Circle(Point(dx, dy), 10)
    new_mass.setFill(color_rgb(248,206,204))
    new_mass.setOutline(color_rgb(184,84,80))

    # Initialise the on-screens messages
    title_msg = Text(Point(width/2,60), "2-D Pendulum Simulator")
    author_msg = Text(Point(width/2,80),"Yuhao Li 2019")
    turn_point_msg = Text(Point(0, 0), "")
    press_continue_msg = Text(Point(width/2, 500), "Press any key to start!")
    ang_msg = Text(Point(100, 60), "ang : 0")
    vel_msg = Text(Point(100, 80), "vel : 0")
    accel_msg = Text(Point(100, 100), "accel : 0")
    dis_msg = Text(Point(100, 120), "dis : 0")
    sim_time_msg = Text(Point(100,140), "sim time : 0")
    rt_time_msg = Text(Point(100,160),"real time : 0")

    # Set font size
    title_msg.setSize(20)
    author_msg.setSize(16)

    # Draw elements
    press_continue_msg.draw(win)
    title_msg.draw(win)
    author_msg.draw(win)
    circle.draw(win)
    line.draw(win)
    centerPoint.draw(win)
    new_mass.draw(win)

    try:
        # Start after a key press
        win.getKey()
        press_continue_msg.undraw()
        t0 = time.time()
        i = 0
        check_key = ""

        while(i < len(cal_res['time_arr']) and check_key == ""):
            check_key = win.checkKey()
            sim_time_msg.undraw()
            rt_time_msg.undraw()
            
            if other_msg_loop_count >= other_msg_delay:

                # Undraw elements
                ang_msg.undraw()
                vel_msg.undraw()
                accel_msg.undraw()
                dis_msg.undraw()
                
                ang_msg.setText("ang : %+f deg" %
                               (cal_res['ang_deg_arr'][i]))
                vel_msg.setText("vel : %+f m/s" %
                               (cal_res['vel_arr'][i]))
                accel_msg.setText("accel : %+f m/s^2" %
                                 (cal_res['accel_arr'][i]))
                dis_msg.setText("dis : %+f m" %
                               (cal_res['dis_arr'][i]))
                               
                ang_msg.draw(win)
                vel_msg.draw(win)
                accel_msg.draw(win)
                dis_msg.draw(win)

                # Reset the loop counter
                other_msg_loop_count = 0

            if real_time_loop_counter >= real_time_delay:
                # Undraw all the elements
                new_mass.undraw()
                line.undraw()
                centerPoint.undraw()
                # Calculate the new coordinate
                dx = center_x + (radius * math.sin(cal_res['ang_rad_arr'][i]))
                dy = center_y + (radius * math.cos(cal_res['ang_rad_arr'][i]))

                line = Line(circle.getCenter(), Point(dx, dy))
                line.setOutline(color_rgb(102,102,102))
                
                new_mass = Circle(Point(dx, dy), 10)
                new_mass.setFill(color_rgb(248,206,204))
                new_mass.setOutline(color_rgb(184,84,80))

                # Draw new elements
                line.draw(win)
                centerPoint.draw(win)
                new_mass.draw(win)

                # Reset the loop counter
                real_time_loop_counter = 0

            # Print turing points
            if cal_res['turn_point_arr'][i]:
                turn_point_msg.undraw()
                turn_point_msg = Text(Point(new_mass.getCenter().getX(
                ), new_mass.getCenter().getY()+30), "%.4f deg" % cal_res['ang_deg_arr'][i])
                turn_point_msg.draw(win)
                
            tn = time.time() - t0
            sim_time_msg.setText("sim time : %+f s" % cal_res['time_arr'][i])
            rt_time_msg.setText("real time : %+F s" % tn)
            if tn > cal_res['time_arr'][i]:
                rt_time_msg.setTextColor("red")
                
                
            sim_time_msg.draw(win)
            rt_time_msg.draw(win)
            
            real_time_loop_counter += 1
            other_msg_loop_count += 1
            time.sleep(delay_ratio)
            i += 1
    except:
        print(traceback.format_exc())


def main():
    try:
        # Initial variables
        input_options = ''
        # Initial result dicitonary, with a new key 'isCalculate'
        # to show the status of the variable (whether being overwritten)
        cal_res = {
            "isCalculate": False
        }

        # Main loop
        while input_options != 'q':
            # Clean the terminal windows for each loop
            os.system('clear')

            # Print the option menu
            print("DUISC Programming Assignment 2 Part A")
            print("Yuhao Li 2019")
            print("Pendulum Simulator")
            print("\n")
            print("1. Edit params")
            print("2. Calculate")
            print("3. Plot data")
            print("4. Save to CSV")
            print("5. Open 2-D simulator")
            print("Quit -- q")
            print("\n")
            input_options = input("Options: ")

            # Determine the options
            if input_options == "1":
                print_params()

                # use the global variables
                global mass, length, drag_coef, time_step, initial_angle, total_time

                # set the value of the parameter and refresh the menu
                mass = set_params("Option[1] - Mass: ", mass)
                print_params()

                length = set_params("Option[2] - Length: ", length)
                print_params()

                drag_coef = set_params("Option[3] - Drag coef: ", drag_coef)
                print_params()

                time_step = set_params("Option[4] - Time step: ", time_step)
                print_params()

                initial_angle = set_params(
                    "Option[5] - Initial angle: ", initial_angle)
                print_params()

                total_time = set_params("Option[6] - Total time: ", total_time)
                print_params()

                # Each time when params are editted, reset the cal_res status
                cal_res['isCalculate'] = False

                input("\nPress any key to continue")

            elif input_options == "2":
                # Call the function to get the results
                cal_res = execute(mass, length, drag_coef,
                                  time_step, initial_angle, total_time)

                # Editing the 'isCalculate' key to show that results are gotten.
                cal_res['isCalculate'] = True

                # Print the results in the terminal
                print_res(cal_res)

            elif input_options == "3":
                if cal_res['isCalculate'] == True:
                    # Call the function to plot graphs
                    plot_data(cal_res)
                else:
                    print("Please calculate first")
                    input("\nPress any key to continue")

            elif input_options == "4":

                if cal_res['isCalculate'] == True:

                    # Call the function to save the result to a csv file
                    save_to_csv(cal_res)
                else:
                    print("Please calculate first")

                input("\nPress any key to continue")

            elif input_options == "5":

                if cal_res['isCalculate'] == True:

                    # Call the function to open the GUI simulator
                    run_GUI(cal_res)
                else:
                    print("Please calculate first")
                    input("\nPress any key to continue")

            elif input_options == "q":
                print("Exit the programme...")

    except Exception:
        print(traceback.format_exc())

if __name__ == "__main__":
    main()

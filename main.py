# DUISC Advanced Physics Project
# Projectile Motion Simulator
# Yuhao Li 2019
import os
import traceback
import platform
from projectile_object import *

# Check platform
sys_platform = platform.system()

# console clear command
if sys_platform is "Windows":
    sys_clear = "CLS"
else:
    sys_clear = "clear"

# Initialise global prompts
title = "DUISC Advanced Physics Project"
author_copyright = "Yuhao Li 2019"
name = "Projectile Motion Simulator"


def print_head_menu():
    # This function prints the copyright and the head tile of the application.

    os.system(sys_clear)
    print(title)
    print(author_copyright)
    print(name+"\n")


def print_main_menu():
    # This function prints the main menu in the console

    print_head_menu()
    print("+-------------------------------------------+")
    print("|{:^43s}|".format("Main menu"))
    print("+-------------------------------------------+")
    print("| {:<42s}|".format("1. Edit projectiles"))
    print("| {:<42s}|".format("2. Calculate"))
    print("| {:<42s}|".format("3. Plot data"))
    print("| {:<42s}|".format("4. Save to CSV"))
    print("| {:<42s}|".format("5. Open 2-D animation"))
    print("| {:<42s}|".format("Quit -- q"))
    print("+-------------------------------------------+\n")


def print_projectile_menu(option_list_callback):
    # This function prints the projectile table
    # inputs:	option_list_callback 	        (string)		        the options menu functions

    print_head_menu()
    print("+-------------------------------------------------------------+")
    print("|{:^30s}|{:^30s}|".format("Projectiles", "Calculation Status"))
    print("+-------------------------------------------------------------+")
    index = int(1)

    for ob in projectile_object.object_list:
        name = str(index) + ". " + ob.name
        calculate_status = str(ob.cal_res["is_calculated"])
        print("|{:^30s}|{:^30s}|".format(name, calculate_status))
        index += 1

    if len(projectile_object.object_list) == 0:
        print("|{:^30s}|{:^30s}|".format("", ""))
    print("+-------------------------------------------------------------+\n")
    option_list_callback()


def print_plot_menu():
    # This function prints ploting option menu in the console

    print_head_menu()
    print("+----------------------------------------------------------+")
    print("|{:^58s}|".format("Plot options"))
    print("+----------------------------------------------------------+")
    print("| {:<56s} |".format("1. Print acceleration x"))
    print("| {:<56s} |".format("2. Print acceleration y"))
    print("| {:<56s} |".format("3. Print velocity x"))
    print("| {:<56s} |".format("4. Print velocity y"))
    print("| {:<56s} |".format("5. Print displacement x"))
    print("| {:<56s} |".format("6. Print displacement y"))
    print("| {:<56s} |".format("7. Print x-y displacement"))
    print("| {:<56s} |".format("8. Print angle"))
    print("| {:<56s} |".format("9. Print four comprehensive graphs"))
    print("| {:<56s} |".format("Quit -- q"))
    print("+----------------------------------------------------------+\n")


def case_1_options_callback():
    # This function prints the options for the projectile editing menu

    print("1. Add projectiles")
    print("2. Edit parameters")
    print("3. Delete a projectile")
    print("4. Delete all projectiles")
    print("Quit -- q\n")


def case_2_options_callback():
    # This function prints the options for the calculation menu
    
    print("1. View result table")
    print("2. View summary")
    print("Quit -- q\n")


def object_has_result():
    # This function checks if there is at least one object in the 
    # object_list that has been calculated
    # outputs:  True       (boolean)                has result
    #           False      (boolean)                no result available 

    for ob in projectile_object.object_list:
        if ob.cal_res["is_calculated"]:
            return True

    return False


def g_edit_projectiles():
    # This function allows user the edit the projectiles.

    user_option = ""

    while user_option is not "q":
        print_projectile_menu(case_1_options_callback)
        user_option = input("Options: ")

        try:
            if user_option is "1":    # Add projectiles
                object_names = input("Object name: ").split(",")    # Names splotted by ","
                for name in object_names:
                    projectile_object(name)    # add the projectiles to the list orderly

            elif user_option is "2":    # Edit the parameters
                # Select a projectile by inputting a index
                object_index = int(input("Object index: ")) - 1
                ob = projectile_object.object_list[object_index]
                ob.set_params(print_head_menu)

            elif user_option is "3":    # Delete a projectile
                # Select a projectile by inputting a index
                object_index = int(input("Object index: ")) - 1
                ob = projectile_object.object_list[object_index]
                projectile_object.remove_from_list(ob)

            elif user_option is "4":    # Delete all projectiles
                projectile_object.remove_all()
        except:
            pass


def g_calculation():
    # This function calculates the results of each projectile in the object_list

    # All the projectiles in the list will be calculated
    for ob in projectile_object.object_list:
        # Re-calculated is not necessary if the parameters are not changed
        if not ob.cal_res["is_calculated"]:     
            ob.calculate()
        print_projectile_menu(case_2_options_callback)      # Calculation status is refreshed

    if object_has_result(): # If there is any result available to be previewed
        user_option = ""

        while user_option is not "q":
            print_projectile_menu(case_2_options_callback)
            user_option = input("Options: ")

            try:
                if user_option is "1":      # Print result table
                    # Select a projectile by inputting a index
                    object_index = int(input("Object index: ")) - 1
                    ob = projectile_object.object_list[object_index]
                    ob.print_res_table(print_head_menu)

                elif user_option is "2":    # Print summary
                    # Select a projectile by inputting a index
                    object_index = int(input("Object index: ")) - 1
                    ob = projectile_object.object_list[object_index]
                    ob.print_summary(print_head_menu)
            except:
                pass
    else:
        input("No available results to plot, press any key to continue")


def g_plot_data():
    # The function plots the graphs of the results of each projectile

    if object_has_result():  # If there is any result available to be plotted
        user_option = ""

        while user_option is not "q":
            print_plot_menu()   # Print the plotting option menu
            user_option = input("Options: ")    # Input the chosen option
            projectile_object.plot_graphs(user_option)
    else:
        input("No available results to plot, press any key to continue")


def g_save_csv():
    # The function saves the results of each projectile into csv file

    if object_has_result():  # If there is any result available to be saved

        for ob in projectile_object.object_list:
            ob.save_to_csv()
        input("Saving complete, press any key to continue") 
    else:
        input("No available results to save, press any key to continue")


def g_animation():
    # The function runs an animation of all the projectiles
    
    if object_has_result():  # If there is any result available to be saved
        projectile_object.run_animation()
    else:
        input("No available results to save, press any key to continue")


def main():
    input_options = ""  # Input option variable

    # Main loop starts
    while input_options is not "q":
        try:
            print_main_menu()
            input_options = input("Options: ")

            if input_options is "1":
                g_edit_projectiles()

            elif input_options is "2":
                g_calculation()

            elif input_options is "3":
                g_plot_data()

            elif input_options is "4":
                g_save_csv()

            elif input_options is "5":
                g_animation()

            elif input_options is "q":
                print("Exit the programme...")

        except Exception:
            pass


if __name__ == "__main__" and run_programme:
    main()

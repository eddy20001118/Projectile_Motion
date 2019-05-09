import math
import matplotlib.pyplot as plt
import os
import time

list_x=[]
list_t=[]		
list_v=[]					
list_vx=[]
list_vy=[]                    
list_angle=[]                      
list_x=[] 
list_y=[]
list_a=[]

initial_angle = math.radians(60)
total_time = 30.0
step_size = 0.05
air_resistance = 0.1
mass = 20.0
velocity = 10.0
object_area_x = 0.02
object_area_y = 0.02
air_density = 1.205
gravity_acceleration = 9.81
initial_height = 40.0





def design_mass(prompt,default):
    try:
        value=float(input(prompt))
        if 0<value:
            print("Your value is value,return value...")
            return value
        else:
            print(" You print an invalid mass, and make sure mass should be bigger than 0 ")
            print(" return default...")			
    except ValueError:
        print("invalid value")              
        return default

def design_angle(prompt,default):
    try:
        value=float(input(prompt))
        if 0<value<=90:
            print("Your value is value,return value...")
            return value
        else:
            print(" You print an invalid degree, and make sure degree should be bigger than 0 and less than or equal to 90")
            print(" return default...")			
    except ValueError:
        print("invalid value")
        return default
        
def design_float(prompt,default):
    try:
        value=float(input(prompt))  
        return value                
    except ValueError:
        print("invalid float")       
        return default		


def design_parameters():
    initial_angle=math.radians(design_angle("iniital angle:", 60))
    total_time=design_float("total simulation time:", 30)
    step_size=design_float("step size:", 0.05)
    air_resistance=design_float("air resistance:",0.05)
    mass=design_mass("mass:",20)
    velocity=design_float("velocity:",10)
    object_area_x=design_float("horizontal area:",0.02)
    object_area_y=design_float("vertical area:",0.02)
    air_density=design_float("air density:",1.205)
    gravity_acceleration=design_float("gravity acceleration:",10)
    initial_height=design_float("initial height:",40)
    
    return initial_angle,total_time,step_size,\
        air_resistance,mass,velocity,\
            object_area_x,object_area_y,\
                air_density,gravity_acceleration,initial_height

def show_params(initial_angle,total_time,step_size,\
        air_resistance,mass,velocity,\
            object_area_x,object_area_y,\
                air_density,gravity_acceleration,initial_height):
                pass


def menu():
    
    print("------------------------------------------------------------")
    print(" Press 1 is to enter system parameters and simulation properties")
    print(" Press 2 is to calculate the data with related formulae")
    print(" Press 3 is to display calculated data")
    print(" Press 4 is to make a animation about the simulation")
    print(" Press 5 is to plot the graph")
    print(" Press 6 is to save to file in CSV format")
    print(" Press Q is to quit the programming")
    print("----------------------------------------------------------------")
    print('\n\n\n')





def save_data(list_angle,list_x,list_y,list_t,list_v,list_vx,list_vy):
    
    
    f = open("projectile motion.csv",'w')
    projectile_motion ='number，time,velocity,angle,vertical velocity,horizontal velocity,distance,height\n'
    f.write(projectile_motion)
    
    
    for i in range(0,len(list_t)):
        print('  %d  %f  %f  %f  %f  %f  %f  %f  '  % \
            (i , list_t[i] , list_v[i] , list_angle[i] , list_vx[i] , list_vy[i] , list_x[i] , list_y[i] ))
        f.write(projectile_motion)
    
    
    
    print('save_data complete')		
    input('Please [Enter] to coninue...\n')
    f.close()



def calculation(initial_angle,total_time,step_size,\
    air_resistance,mass,velocity,object_area_x,\
        object_area_y,air_density,gravity_acceleration,initial_height):

    i=0
    

    list_y = [initial_height]
    list_v.append(velocity)
    list_x.append(0.0)
    list_t.append(0.0)	
    vx1 = velocity*math.cos(initial_angle)
    vy1 = velocity*math.sin(initial_angle)
    list_vx.append(vx1)
    list_vy.append(vy1)
    list_angle.append(57.2958*initial_angle)     
    


    
    #maximum_height = (velocity*velocity*math.sin(list_angle[i])*math.sin(list_angle[i]))/ 2*g
    #maximum_distance = (velocity*velocity*math.sin(2*list_angle[i])) / g
    
    

    while list_t[i] <= total_time:
        zeroHVelConstant = list_vx[i-1]*list_vx[i]
        
        ay = -(gravity_acceleration+0.5*air_density*list_vy[i]*math.fabs(list_vy[i])*air_resistance*object_area_y)
        ax = (-0.5)*air_density*list_vx[i]*list_vx[i]*air_resistance*object_area_x   
        a=math.sqrt(ax*ax+ay*ay)

        next_velocity=list_v[i]+a*step_size
        next_time=list_t[i]+step_size                
        next_vertical_velocity=list_vy[i-1]+ay*step_size

        if zeroHVelConstant > 0:  
            next_horizontal_velocity=list_vx[i-1]+ax*step_size
            next_distance=list_x[i-1]+list_vx[i]*step_size
            next_angle=list_vy[i]/list_vx[i]   
            next_height=list_y[i-1]+list_vy[i]*step_size      
            list_angle.append(57.2958*math.atan(next_angle))   
        else:
            next_horizontal_velocity=0
            next_distance=list_x[i]*1.00 
            next_height=list_y[i-1]+list_vy[i]*step_size
            list_angle.append(-90.000)


        list_x.append(next_distance)
        list_y.append(next_height)
        list_t.append(next_time)
        list_v.append(next_velocity)
        list_vx.append(next_horizontal_velocity)
        list_vy.append(next_vertical_velocity)
        i=i+1
    
    max_height_index = list_y.index(max(list_y))

    print("calculation complete ...")               
    print('Total data points: %s'%(len(list_x)))
    print('Maximum height:%f'%max(list_y))
    print('Maximum velocity:%f'%max(list_v))
    print('Time to maximum height:%f'%list_t[max_height_index])  

    input("enter to continue") 

    return list_angle,list_x,list_y,list_t,list_v,list_vx,list_vy           


def showing_data(list_angle,list_x,list_y,list_t,list_v,list_vx,list_vy):
    
    command = ''
    
    while command !='8':

        
        print("number  time  velocity  angle  vertical velocity  horizontal velocity  distance  height")
        
        for i in range(0,len(list_t)):
            print("%d  %f  %f  %f  %f  %f  %f  %f"  %(i , list_t[i] , list_v[i] , list_angle[i] , list_vy[i] , list_vx[i] , list_x[i] , list_y[i]))
            
        input('Press any key to continue...')
        
        
        
        os.system('cls')
        
        print("--------------------------------------------------------------------------------------------")
        print("Press 1 to show the time of the object ")     
        print("Press 2 to show the velocity of the simulation")                                                    
        print("Press 3 to show the angle of the each point simulation")                                            
        print("Press 4 to show the vertical velocity of the object along circular path with reference to vertical")    
        print("Press 5 to show the horizontal velocity along the vertical direction")
        print("Press 6 to show the distance from the initial point to the ending point")
        print("Press 7 to show the height from the ground to the height at each point")
        print("Press 8 to return to menu ")
        print("--------------------------------------------------------------------------------------------")	
        
        command = input("print an option from the menu above:")
        
        if command == '1':
            print(list_t)
            input('Press [Enter] to continue...\n')
            
    
        elif command == '2':
            print(list_v)
            input('Press [Enter] to continue...\n')
            
        
        elif command == '3':
            print(list_angle)
            input('Press [Enter] to continue...\n')
            
        
        elif command == '4':
            print(list_vx)
            input('Press [Enter] to continue...\n')
            
            
        elif command == '5':
            print(list_vy)
            input('Press [Enter] to continue...\n')
    
    
        elif command == '6':
            print(list_x)
            input('Press [Enter] to continue...\n')
            
            
        elif command == '7':
            print(list_y)
            input('Press [Enter] to continue...\n')
            
            
        elif command == '8':
            break
            
            
        else:
            print('Please enter an option which is not bigger that 8')
            input('Press [Enter] to continue...\n')


def menu_plot_graph(list_angle,list_x,list_y,list_t,list_v,list_vx,list_vy):
    
    command_input=''
    
    
    
    while command_input != '5':
    
            
        os.system('cls')
        
        print("--------------------------------------------------------------------")
        print("Press 1 to plot the Y-X graph")
        print("Press 2 to plot the Y-t graph")
        print("Press 3 to plot the X-t graph")
        print("Press 4 to plot the θ-t graph")
        print("Press 5 to return to the menu")
        print("--------------------------------------------------------------------")
        print("\n\n\n")
    
        
        
        
        command_input = input("enter a choice in the plot menu:")
        
        if command_input == "1":
            plt.plot(list_x,list_y)
            plt.xlabel('distance.x(m)')               
            plt.ylabel('distance.y(m)')            
            plt.title("The Projectile motion")  
            plt.ion()  
            plt.show()	

        elif command_input == "2":
            plt.plot(list_t,list_y)
            plt.xlabel('time.t(s)')               
            plt.ylabel('height.h(m)')            
            plt.title("The Projectile motion")   
            plt.ion() 
            plt.show()
            
        elif command_input == "3":
            plt.plot(list_t,list_x)
            plt.xlabel('time.t(s)')               
            plt.ylabel('velocity.v(m/s)')            
            plt.title("The Projectile motion") 
            plt.ion()   
            plt.show()	

        elif command_input == "4":
            plt.plot(list_t,list_angle)
            plt.xlabel('time.t(s)')               
            plt.ylabel('angle.θ(rads)')            
            plt.title("The Projectile motion")  
            plt.ion()  
            plt.show()	

        else:	
            print("Invaild option")





#--------------------------------------------------------------------------------------------------------



# initial command is empty
command_option = ''

# main loop - keep going until user enters 'q' 
while command_option != 'Q':
    
    os.system('cls') # windows clear screen
    
    # show the menu
    menu()
    
    command_option = input('enter menu choice: ')


    # press 1 to execute the first function 
    if command_option =='1':
        initial_angle,total_time,step_size,air_resistance,mass,velocity,object_area_x,object_area_y,air_density,gravity_acceleration,initial_height = design_parameters()
        
        
    # press 2 to execute the second function
    elif command_option == '2':
        list_angle,list_x,list_y,list_t,list_v,list_vx,list_vy = calculation(initial_angle,total_time,step_size,air_resistance,mass,velocity,object_area_x,object_area_y,air_density,gravity_acceleration,initial_height)
        
        
    # press 3 to execute the third function
    elif command_option == '3':
        showing_data(list_angle,list_x,list_y,list_t,list_v,list_vx,list_vy)
        

    # press 4 to execute the fourth function
    elif command_option == '4':		
        save_data(list_angle,list_x,list_y,list_t,list_v,list_vx,list_vy)
    
    
    # press 5 to execute the fifth function
    elif command_option == '5':
        menu_plot_graph(list_angle,list_x,list_y,list_t,list_v,list_vx,list_vy)
            
    
    # press Q to quit the programming
    elif command_option == 'Q':
        print('The program is over!')
        
    
    # this is avoid the user entering other options
    else:
        print('Invalid command.')
        print('Please enter an option which is not bigger that 5')
    


# this would be printed when the user enter an invalid option
    print('Thanks for using.\nGoodbye!!')




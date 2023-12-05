#===================================================================
# Created by Behrad Rezaie, Maxime Courchesne
# As part of the course ECSE 211, McGill University
#
# Last modified by Maxime Courchesne on December 12th 4:39
# Reason: Remove useless comments and testing code, add spacings to improve readability
#
#
#===================================================================

from NavigationIteration1.FireTruckNavigation import FireTruck
from libs.pathfinding import getRobotMovementList
from utils.brick import Motor
from utils.brick import wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor
import time

# Initializing sensors
motor_right = Motor("D")
motor_left = Motor("A")
color_left = EV3ColorSensor("1")
color_right = EV3ColorSensor("2")
spinner = Motor('B')
pusher = Motor('C')
ultrasonic_sensor = EV3UltrasonicSensor('3')
wait_ready_sensors()


# Creating an instance of the FireTruck class
FireTruck1 = FireTruck(motor_left, motor_right, color_left,
                       color_right, spinner, pusher, ultrasonic_sensor)

# Simple command to make the program wait before the robot starts
input("Enter to start pathfinding")
path = getRobotMovementList((1, 1), "red", (2, 1), "purple", (3, 3), "green")
# We make sure that the motors are not already running before starting
FireTruck1.stop_motors()

# Here, we are just changing the syntax of our turn instructions so that they are compatible with the Navigation methods
for i in range(len(path)):
    if path[i] == 90:
        path[i]= "turn_right"
    elif path[i] == -90:
        path[i] = 'turn_left'
    elif path[i] == 180 or path[i] == -180:
        path[i] = 'flip'
        
# This is the "for loop" that will iterate through the list of instructions and call the appropriate methods
commands = path
print(commands)
input("Enter to start.")
for i in range(len(commands)):
    print("Doing:",str(commands[i]))
    FireTruck1.parse_command(commands[i])
    if i != len(commands)-1:
        print('next command:',commands[i+1])
    time.sleep(0.5)

# When we are done, we want to make sure that no motor is running
FireTruck1.stop_motors()


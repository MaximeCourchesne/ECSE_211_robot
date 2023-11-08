from FireTruckNavigation import FireTruck
from libs.pathfinding import getRobotMovementList
from utils.brick import Motor
from utils.brick import wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor
import time

#color_sensor = EV3ColorSensor(1) # port S1
#wait_ready_sensors()

motor_right = Motor("D")
motor_left = Motor("A")
color_left = EV3ColorSensor("2")
color_right = EV3ColorSensor("4")
FireTruck1 = FireTruck(motor_left, motor_right, color_left,color_right)


# inputs: block positions and colors
# outputs: list of instructions for the robot to execute
# example: print(getRobotMovementList((1, 0), "purple", (3, 2), "red", (2, 1), "green"))
# >>> [90, 'drop_purple', -90, 'foward', 90, 'foward', -90, 'foward', 90, 'foward', 'drop_red', 90, 'drop_green', 90, 'foward', 'foward', -90, 'foward', 'foward']
path = getRobotMovementList((1, 0), "purple", (3, 2), "red", (2, 1), "green")
print(path)
    
#FireTruck1.turn(90)
#FireTruck1.stop_motors()
print("adusting")
FireTruck1.adjust_direction("left")
print("adjusted")
'''
# main loop
for instruction in path:
    if isinstance(instruction, int):
        FireTruck1.turn(instruction)
        print("turn")
    elif instruction == "forward":
        FireTruck1.move_forward()
        print("forward")
    elif "drop" in instruction:
        #FireTruck1.drop()
        print("drop cube")
'''
'''
while True:
    colors = FireTruck1.get_colors()
    if "Red" in colors[0] or "Blue" in colors[0]:
        FireTruck1.adjust_direction("left")
    elif "Red" in colors[1] or "Blue" in colors[1]:
        FireTruck1.adjust_direction("right")
'''
print("alegedly turning 90")
#FireTruck1.turn(90)
FireTruck1.stop_motors()

"""
command = input("Enter a command: ")
while "quit" not in command:
    FireTruck1.parse_command(command)
    command = input("Enter a command: ")"""


#FireTruck1.turn(90)
commands = ['forward','left','forward','forward','left','forward','left','forward','forward','left']
for command in commands:
    FireTruck1.parse_command(command)
    time.sleep(2)

FireTruck1.stop_motors()


#FireTRuck1.move_forward()
    
        
    #FireTruck1.move_forward()

#FireTruck1.stop_motors()

from FireTruckNavigation import FireTruck
from libs.pathfinding import getRobotMovementList
from utils.brick import Motor
from utils.brick import wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor


#color_sensor = EV3ColorSensor(1) # port S1
#wait_ready_sensors()

motor_right = Motor("D")
motor_left = Motor("A")
FireTruck1 = FireTruck(motor_left, motor_right, "color_sensor")


# inputs: block positions and colors
# outputs: list of instructions for the robot to execute
# example: print(getRobotMovementList((1, 0), "purple", (3, 2), "red", (2, 1), "green"))
# >>> [90, 'drop_purple', -90, 'foward', 90, 'foward', -90, 'foward', 90, 'foward', 'drop_red', 90, 'drop_green', 90, 'foward', 'foward', -90, 'foward', 'foward']
path = getRobotMovementList((1, 0), "purple", (3, 2), "red", (2, 1), "green")
print(path)

FireTruck1.turn(90)
FireTruck1.stop_motors()

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



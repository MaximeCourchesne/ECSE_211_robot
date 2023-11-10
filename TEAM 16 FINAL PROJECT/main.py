from FireTruckNavigation import FireTruck
from libs.pathfinding import getRobotMovementList
from utils.brick import Motor
from utils.brick import wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor
import time

#color_sensor = EV3ColorSensor(1) # port S1
#wait_ready_sensors()

motor_right = Motor("D")
motor_left = Motor("A")
color_left = EV3ColorSensor("1")
color_right = EV3ColorSensor("2")
spinner = Motor('B')
pusher = Motor('C')

FireTruck1 = FireTruck(motor_left, motor_right, color_left,color_right, spinner, pusher)


path = getRobotMovementList((1, 0), "purple", (3, 2), "red", (2, 1), "green")


FireTruck1.stop_motors()
#FireTruck1.turn(90)
print(path)
input()
['yellow','blue','green','red','purple','orange']
commands = ['forward','drop_yellow', 'turn_left','turn_right','forward']
for i in range(len(path)):
    if path[i] == 90:
        path[i]= "turn_right"
    elif path[i] == -90:
        path[i] = 'turn_left'
commands = path
for i in range(len(commands)):
    print("Doing:",str(commands[i]))
    FireTruck1.parse_command(commands[i])
    if i != len(commands)-1:
        print('next command:',commands[i+1])
    input()

FireTruck1.stop_motors()


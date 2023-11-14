"""Module containing class object that handles navigation."""
import math
import time
from utils.brick import Motor
from utils.brick import wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor
#TODO Change all docstrings to smt more descriptive

class FireTruck:
    """Class object for system that implements navigation methods."""
    def __init__(self, left_motor, right_motor, color_sensor_left, color_sensor_right, spider_spinner, spider_pusher) -> None:
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.color_sensor_left = color_sensor_left
        self.color_sensor_right = color_sensor_right
        self.spinner = spider_spinner
        
        self.spinner.set_limits(power=50)
        self.pusher = spider_pusher
        self.current_line_color = "Red"
        
        self.directions = ['n','e','s','w']
        self.direction_index = 0
        self.facing_direction =  self.directions[0]
        #self.spinner.reset_encoder()
        self.suppressant_order = ['blue','yellow','green','red','orange','purple']

    def set_color_order(self):
        order = []
        colors = input("enter letters of colors").lower()
        for l in colors:
            if l == 'b':
                order.append("blue")
            elif l == 'y':
                order.append("yellow")
            elif l == 'g':
                order.append("green")
            elif l == 'o':
                order.append("orange")
            elif l == 'r':
                order.append("red")
            elif l == 'p':
                order.append("purple")
            else:
                print("invalid input: ",l)
                continue
            self.suppressant_order = order
    def stop_motors(self):
        """Stop all motors from rotating"""

        self.left_motor.set_dps(0)
        self.right_motor.set_dps(0)
        self.left_motor.set_power(0)
        self.right_motor.set_power(0)

    def reverse_off_green(self):
        print("AOWEJDpaodwe")
        self.left_motor.set_power(100)
        self.right_motor.set_power(100)
        colors = self.get_colors()
        while 'Green' in colors:
            print(colors, 'waiting to leave green')
            colors = self.get_colors()
            if self.current_line_color in colors[0]:
                self.adjust_direction("left")
            elif self.current_line_color in colors[1]:
                self.adjust_direction("right")
            self.left_motor.set_dps(-360)
            self.right_motor.set_dps(-360)
        self.stop_motors()
            
    def move_until_green(self, backwards = False):
        self.left_motor.set_power(60)
        self.right_motor.set_power(60)
        direction =1
        if backwards:
            direction = -1
        colors = self.get_colors()

        while "Green" not in colors:
            colors = self.get_colors()
            if self.current_line_color in colors[0]:
                self.adjust_direction("left")
            elif self.current_line_color in colors[1]:
                self.adjust_direction("right")
            self.left_motor.set_dps(360*direction)
            self.right_motor.set_dps(360*direction)
        self.stop_motors()
    
    def center_on_green(self):
        
        colors = []
        colors = self.get_colors()
        while "Green" in colors:
            colors = self.get_colors()
            if self.current_line_color in colors[0]:
                self.adjust_direction("left")
            elif self.current_line_color in colors[1]:
                self.adjust_direction("right")
            self.left_motor.set_dps(360)
            self.right_motor.set_dps(360)
        self.stop_motors()
    
        count_extra_loops=0
        while count_extra_loops<200: #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #print(count_extra_loops)
            colors = self.get_colors()
            if self.current_line_color in colors[0]:
                self.adjust_direction("left")
            elif self.current_line_color in colors[1]:
                self.adjust_direction("right")
            self.left_motor.set_dps(360)
            self.right_motor.set_dps(360)
            count_extra_loops+=1
        self.stop_motors()
    
    
    def move_forward(self):
        """Move the robot forward by 1 edge, 30 cm, by rotating the motors."""
        self.left_motor.set_power(100)
        self.right_motor.set_power(100)
        colors = self.get_colors()
        print(colors)
        while "Green" not in colors:
            print(colors)
            self.auto_adjust()
            self.left_motor.set_dps(360)
            self.right_motor.set_dps(360)
        print("green reached")
        self.stop_motors()
        count_extra_loops=0
        while count_extra_loops<250:
            #print(count_extra_loops)
            colors = self.get_colors()
            if self.current_line_color in colors[0]:
                self.adjust_direction("left")
            elif self.current_line_color in colors[1]:
                self.adjust_direction("right")
            self.left_motor.set_dps(360)
            self.right_motor.set_dps(360)
            count_extra_loops+=1
        self.stop_motors()

    def turn_until_line(self):
        self.left_motor.set_limits(power=70, dps=360)
        self.right_motor.set_limits(power=70, dps=360)
        colors = self.get_colors()
        while self.current_line_color not in colors:
            colors = self.get_colors()
            self.left_motor.set_position_relative(360)
            self.right_motor.set_position_relative(-360)
        self.stop_motors()
        self.auto_adjust()
        time.sleep(0.5)
        
    def turn_off_line(self):
        self.left_motor.set_limits(dps=360)
        self.right_motor.set_limits(dps=360)
        
        self.left_motor.set_position_relative(360)
        self.right_motor.set_position_relative(-360)
        time.sleep(0.5)
    def spin_to_color(self, color):
        self.spinner.set_limits(dps=360,power=80)
        index = self.suppressant_order.index(color)
        if index == -1:
            return index
        print('spinning to ', color)
        
        self.spinner.set_position(index * 60 *-1)
        time.sleep(1)
        return index
    def push_color(self):
        self.pusher.set_limits(power=80, dps=360)
        self.pusher.set_position_relative(-360)
        
        time.sleep(1.5)        
        self.spinner.set_position(0)

    def get_colors(self):
        return (self.color_sensor_left.get_color_name(), self.color_sensor_right.get_color_name())
    
    def turn(self, turn_angle):
        """Turn the robot by a number of degrees, without changing its coordinates.
        
        Parameters:
            turn_angle -- Turn a number of degrees clockwise
        """
        if turn_angle == -90:
            self.direction_index -= 1
        elif turn_angle == 90:
            self.direction_index += 1
        if self.direction_index < 0:
            self.direction_index = 3
        elif self.direction_index > 3:
            self.direction_index = 0
        
        toFlip = False
        if abs(turn_angle) == 90:
            if self.current_line_color == 'Blue':
                self.current_line_color = 'Red'
            else:
                self.current_line_color = 'Blue'
        
        
        print("following " + self.current_line_color)
        
        movement = 4 * turn_angle
        
        
        self.right_motor.set_limits(power=80, dps=360)
        self.left_motor.set_limits(power=80, dps=360)
        
        colors = self.get_colors()
        # turn until you see a line of the desired color
        while self.current_line_color not in colors:
            colors = self.get_colors()
            self.right_motor.set_position_relative(-1 * movement)
            self.left_motor.set_position_relative(movement)
        self.auto_adjust()
        
    def math_turn(self):
        self.right_motor.set_limits(power=70, dps=360)
        self.left_motor.set_limits(power=70,dps=360)
        self.right_motor.set_position_relative(360)
        self.left_motor.set_position_relative(-1*360)
        time.sleep(2)
    
    def auto_adjust(self):
        colors = self.get_colors()
        if self.current_line_color in colors[0]:
            self.adjust_direction("left")
        elif self.current_line_color in colors[1]:
            self.adjust_direction("right")
            
    def adjust_direction(self, direction):
        """Adjust the robots position if it ever trails off the line, determined by the color sensor detecting a different color than expected.
        Initial idea is to spin the robot to the left by 20 degrees to check if the line is in the 20 degrees to its left 
            (assumes it went off on the right side of the street line). If line is found, continue previous instruction
        Else, spin to right by 20 degrees to reset, and then another 20 degrees to the right to check if line is in the 20 degrees
            to its right (assumes it went off on the left side of the street lane)
        """
        self.left_motor.set_limits(dps=360, power=100)
        self.right_motor.set_limits(dps=360, power=100)
        print(self.color_sensor_left.get_color_name())
        print(self.color_sensor_right.get_color_name())
        if direction == "left":
            print("turning")
            while self.current_line_color in self.color_sensor_left.get_color_name():
                self.left_motor.set_position_relative(-10)
                self.right_motor.set_position_relative(10)
            self.left_motor.set_position_relative(-60)
            self.right_motor.set_position_relative(60)

        if direction == "right":
            print("turning")
            while self.current_line_color in self.color_sensor_right.get_color_name():
                
                self.left_motor.set_position_relative(10)
                self.right_motor.set_position_relative(-10)
            self.left_motor.set_position_relative(60)
            self.right_motor.set_position_relative(-60)
        
        
    def parse_command(self, command):
        if "forward" in command:
            self.move_until_green()
            self.center_on_green()
        elif "right" in command:
            self.turn(90)
        elif "left" in command:
            self.turn(-90)
        elif 'flip' in command:
            self.turn_off_line()
            self.turn_until_line()
        elif "drop" in command:
            self.move_until_green()
            self.spin_to_color(command[5:])
            time.sleep(1)
            self.push_color()
            time.sleep(0.1)
            self.reverse_off_green()
            time.sleep(0.2)
            self.move_until_green(True)
            self.center_on_green()
        else:
            self.stop_motors()
            print("invalid command")

if __name__ == "__main__":
    #conduct any testing here
    print("Running main...")
    motor_right = Motor("D")
    motor_left = Motor("A")
    color_left = EV3ColorSensor("1")
    color_right = EV3ColorSensor("2")
    spinner = Motor('B')
    pusher = Motor('C')
    wait_ready_sensors()
    #spinner.set_position_relative(60)
    FireTruck1 = FireTruck(motor_left, motor_right, color_left,color_right, spinner, pusher)

    commands = ['drop_purple', 'drop_blue']
    input()
    for command in commands:
        print(command)
        time.sleep(0.5)
        FireTruck1.parse_command(command)
    time.sleep(1)
    FireTruck1.stop_motors()


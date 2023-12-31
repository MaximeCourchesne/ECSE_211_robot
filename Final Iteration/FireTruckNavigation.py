#===================================================================
# Created by Maxime Courchesne, Behrad Rezaie, Michael Popescu, Le-Tao Li
# As part of the course ECSE 211, McGill University
#
# Last modified by Maxime Courchesne on December 12th 4:35
# Reason: Remove useless comments and testing code, add spacings to improve readability
#
#
#===================================================================


import math
import time
from utils.brick import Motor
from utils.brick import wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor


class FireTruck:
    """Class object for system that implements navigation methods."""
    def __init__(self, left_motor, right_motor, color_sensor_left, color_sensor_right,
                 spider_spinner, spider_pusher, distance_sensor) -> None:
        # initialization instance variables

        self.left_motor = left_motor
        self.right_motor = right_motor
        self.color_sensor_left = color_sensor_left
        self.color_sensor_right = color_sensor_right
        
        self.spinner = spider_spinner
        self.reverse_sensor = distance_sensor
        
        self.pusher = spider_pusher
        self.current_line_color = "Red"
                
        self.power = 90
        self.movement_speed = 270
        
        self.spinner.set_limits(power=self.power,dps=360)
        self.right_motor.set_limits(power=self.power)
        self.left_motor.set_limits(power=self.power)
        self.pusher.set_limits(power=self.power)

        # order in which we will have to place the suppressants on the robot
        self.suppressant_order = ['yellow','green','red','orange','purple','blue']

    def adjust_spinner(self):
        '''
        Function to adjust the robot's "spinner" which is where the cubes are placed. This will be used before the main function starts(before the robot starts delivering the suppressants).
        '''
        adjustment = input("Enter degrees to turn by, or X to exit")
        while adjustment.isnumeric():
            self.spinner.set_position_relative(int(adjustment))
            adjustment = input("Enter degrees to turn by, or X to exit")
            
    def set_color_order(self):
        '''Helper method for setting the order of the colored cubes
        Used only for testing, default order is written in initialization
        Takes input of letters indicating which color to append to order of extinguishers
        '''

        #Order of extinguishers to set
        order = [] 
        
        #Take input of letters, in lowercase, only first 6 letters
        colors = input("enter letters of colors").lower()[:6] 
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

        #Set robot's order to input order
        self.suppressant_order = order


    def stop_motors(self):
        '''Function to stop all motors from rotating in a single command'''

        self.left_motor.set_dps(0)
        self.right_motor.set_dps(0)
        self.left_motor.set_power(0)
        self.right_motor.set_power(0)

    def reverse_off_green(self):
        '''
        Function that reverses until sensors do not detect green anymore. 
        '''

        #Set movement motors powers
        self.left_motor.set_power(self.power)
        self.right_motor.set_power(self.power)
        
        #Continuous movement in reverse until green is no longer detected
        colors = self.get_colors()
        while 'Green' in colors:
            print(colors, 'waiting to leave green')
            colors = self.get_colors()
            if self.current_line_color in colors[0]:
                self.adjust_direction("left")
            elif self.current_line_color in colors[1]:
                self.adjust_direction("right")
            self.left_motor.set_dps(-1*self.movement_speed)
            self.right_motor.set_dps(-1*self.movement_speed)
        
        #Stop movement once off green
        self.stop_motors()
            
    def move_until_green(self, backwards = False):
        '''
        Method that can takes input a boolean "backwards" as input, indicating movement in reverse.
        Moves in specified direction until sensors detect a green square
        Called when robot's sensors are not on green squares
        '''
        #Set movement motors power
        self.left_motor.set_power(self.power)
        self.right_motor.set_power(self.power)
        
        #Set negative direction if movement is in reverse
        direction =1
        if backwards:
            direction = -1
        
        #Continuous movement in specified direction until green detected
        colors = self.get_colors()
        
        reverse_distance = self.reverse_sensor.get_cm()
        while reverse_distance is None:
            reverse_distance = self.reverse_sensor.get_cm()
            
        while "Green" not in colors and reverse_distance < 30:
            reverse_distance = self.reverse_sensor.get_cm()
            while reverse_distance is None:
                reverse_distance = self.reverse_sensor.get_cm()
            
            colors = self.get_colors()
            self.auto_adjust()
            self.left_motor.set_dps(self.movement_speed*direction)
            self.right_motor.set_dps(self.movement_speed*direction)
        
        #Stop motors once green detected
        self.stop_motors()
    
    def center_on_green(self):
        '''
        Method that is called when robot's sensors are on green. Moves forwards by 3cm.
        Used to center robot's center directly above the green square
        '''
        #Continuous movement forward until green no longer detected
        colors = self.get_colors()
        while "Green" in colors:
            colors = self.get_colors()
            if self.current_line_color in colors[0]:
                self.adjust_direction("left")
            elif self.current_line_color in colors[1]:
                self.adjust_direction("right")
            self.left_motor.set_dps(self.movement_speed)
            self.right_motor.set_dps(self.movement_speed)
        self.stop_motors()
    
        #Hardcoded movement forward by an estimated 4 cm
        count_extra_loops=0
        while count_extra_loops<200:
            colors = self.get_colors()
            if self.current_line_color in colors[0]:
                self.adjust_direction("left")
            elif self.current_line_color in colors[1]:
                self.adjust_direction("right")
            self.left_motor.set_dps(self.movement_speed)
            self.right_motor.set_dps(self.movement_speed)
            count_extra_loops+=1
        self.stop_motors()
    

    def turn_off_line(self):
        '''Turns robot counter-clockwise by an estimated 90 degrees mathematically
        Used when calling a 180 turn, to avoid automatically adjusting to lines'''
        
        #Set motor limits
        self.left_motor.set_limits(dps=self.movement_speed,power=self.power)
        self.right_motor.set_limits(dps=self.movement_speed,power=self.power)
        
        #Turn by estimated 90 degrees without checking for lines
        self.left_motor.set_position_relative(360)
        self.right_motor.set_position_relative(-360)
        time.sleep(1)

    def turn_until_line(self):
        '''Turns robot counter-clockwise until the facing direction line is detected.
        Auto adjusts to detected line.
        Used in calling a 180 turn to complete the turn.'''
        
        #Set movement motor limits
        self.left_motor.set_limits(power=self.power, dps=self.movement_speed)
        self.right_motor.set_limits(power=self.power, dps=self.movement_speed)

        #Continuous rotation until the "drop-off" zone is detected
        colors = self.get_colors()
        while self.current_line_color not in colors:
            colors = self.get_colors()
            self.left_motor.set_position_relative(360)
            self.right_motor.set_position_relative(-360)
        
        #Stop motors and adjust to newly detected line
        self.stop_motors()
        self.auto_adjust()
        time.sleep(0.5)
        
    def spin_to_color(self, color, reverse=False):
        '''
        Takes as input 'color': name of the color to spin to
        Spins the robot's color choosing spinner motor to a color's position,
        aligning the specified color directly below the color pusher
        '''
        #Set spinner limits
        #Index at which color is in robot's order of colors
        index = self.suppressant_order.index(color)
        
        #Case where color is not found in order of colors
        if index == -1:
            return index
        
        direction=-1
        if reverse:
            direction=1
        #Set spinner to position of color        
        
        print("spinning to index", index)
        print("Adjusting spin by ",index * 60 * direction)
        self.spinner.set_position_relative(index * 60 *direction)
        
        #Estimated time to complete setting position
        time.sleep(0.5)
    
    def push_color(self):
        '''Spins the robot's cube pushing arm by 360 degrees
        Called once the spin_to_color is complete.
        Arm spins and pushes cube beneath it into the funnel'''
        
        #Set arm limit
        self.pusher.set_limits(power=80, dps=360)
        
        #Spin arm counter-clockwise
        self.pusher.set_position_relative(-360)
        
        #Estimated time for cube to fall through funnel
        time.sleep(1.5)  


    def get_colors(self):
        '''
        Returns a tuple of the colors detected by the left and right color
        sensors respectively.
        '''
        colors = (self.color_sensor_left.get_color_name(), self.color_sensor_right.get_color_name())
        
    
    def turn(self, direction):
        '''
        Takes as input 'direction': 90 or -90 
        Flips the robot's target line color between Red/Blue
        Positive direction indicates clockwise turning, negative indicates CC
        Turns robot in specified direction until target color is detected
        Calls auto-adjust function to adjust on new line
        '''
                
        #Toggle the target line's color
        if self.current_line_color == 'Blue':
            self.current_line_color = 'Red'
        else:
            self.current_line_color = 'Blue'
        
        #Set motor's limits for turning
        self.right_motor.set_limits(power=self.power, dps=self.movement_speed)
        self.left_motor.set_limits(power=self.power, dps=self.movement_speed)
        
        #Amount to turn by repeatedly
        movement = 4 * direction
        colors = self.get_colors()
        #Loop until target color is detected
        while self.current_line_color not in colors:
            colors = self.get_colors()
            self.right_motor.set_position_relative(-1 * movement)
            self.left_motor.set_position_relative(movement)
        #Adjust with the detected color after turn
        self.auto_adjust()
        
    
    def auto_adjust(self):
        '''
        Automatically check if adjustment is needed and call directional adjust functions
        Gets detected colors and checks if the target line color is in either of them
        '''
        #Initialize value of colors 
        colors = self.get_colors()
        if self.current_line_color in colors[0]:
            #Left sensor detected target color
            self.adjust_direction("left")
        elif self.current_line_color in colors[1]:
            #Right sensor detected target color
            self.adjust_direction("right")

    def adjust_direction(self, direction):
        '''
        Takes as input 'direction': String 'left' or right'
        Turns in specified direction until the specified direction's respective sensor
        no longer detects the target line color.
        '''
        
        #Set motor limits for turning
        self.left_motor.set_limits(dps=self.movement_speed, power=self.power)
        self.right_motor.set_limits(dps=self.movement_speed, power=self.power)

        #Execution of adjusting to the left
        if direction == "left":
            #Infinite loop until target color no longer detected
            while self.current_line_color in self.color_sensor_left.get_color_name():
                self.left_motor.set_position_relative(-10)
                self.right_motor.set_position_relative(10)
            #Minor extra adjustment after moving off color
            self.left_motor.set_position_relative(-60)
            self.right_motor.set_position_relative(60)

        #Execution of adjusting to the right
        elif direction == "right":
            #Infinite loop until target color no longer detected
            while self.current_line_color in self.color_sensor_right.get_color_name():
                self.left_motor.set_position_relative(10)
                self.right_motor.set_position_relative(-10)
            #Minor extra adjustment after moving off color
            self.left_motor.set_position_relative(60)
            self.right_motor.set_position_relative(-60)
        
    def parse_command(self, command):
        '''
        Takes as input 'command': String indicating a command for the robot to execute
        Detects if any valid commands are in the input, and executes the required methods accordingly
        Stops the robot if no valid commands are detected in the command
        '''
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
            time.sleep(0.1)
            self.reverse_off_green()
            time.sleep(0.3)
            self.spin_to_color(command[5:])
            time.sleep(0.6)
            self.push_color()
            time.sleep(0.2)
            self.spin_to_color(command[5:], True)
            self.reverse_off_green()
            time.sleep(0.2)
            self.move_until_green(True)
            self.center_on_green()
        else:
            self.stop_motors()
            print("invalid command")


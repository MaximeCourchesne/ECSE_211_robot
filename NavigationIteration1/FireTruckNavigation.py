"""Module containing class object that handles navigation."""
import math
import time
#TODO Change all docstrings to smt more descriptive

class FireTruck:
    """Class object for system that implements navigation methods."""
    # Radius and circumference of wheels in cm
    WHEEL_DIAMETER = 4.5
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi

    # Desired time should it take for the robot to travel 30 cm in seconds
    TRAVEL_DURATION = 3
    # What is the speed of the robot in cm/s?
    SPEED = 30 / TRAVEL_DURATION

    # Diameter of motion in cm, which is distance between the two parallel motors
    MOTION_DIAMETER = 11.5
    # Arc length of 360 degrees of motion in cm/s
    MOTION_CIRCUMFERENCE = (MOTION_DIAMETER * math.pi)

    # Desired time should it take for the robot to turn 360 degrees
    TURN_DURATION = 12
    # What is the turn rate of the robot in cm/s for a full rotation?
    TURN_RATE = MOTION_CIRCUMFERENCE / TURN_DURATION

    def __init__(self, left_motor, right_motor, color_sensor) -> None:
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.color_sensor = color_sensor

        # List containing string instructions generated by pathfinding algorithm
        self.directions = []

    def stop_motors(self):
        """Stop all motors from rotating"""

        self.left_motor.set_dps(0)
        self.right_motor.set_dps(0)
        self.left_motor.set_power(0)
        self.right_motor.set_power(0)

    def move_forward(self):
        """Move the robot forward by 1 edge, 30 cm, by rotating the motors."""

        # Set both motors to 100% power
        self.left_motor.set_power(100)
        self.right_motor.set_power(100)

        # How many wheel rotations before we travel self.speed?
        rotations = self.SPEED / self.WHEEL_CIRCUMFERENCE
        degrees_to_turn = rotations * 360

        # Travel self.speed in 1 second
        self.left_motor.set_dps(degrees_to_turn)
        self.right_motor.set_dps(degrees_to_turn)

        # Wait the full duration to travel 30 cm
        time.sleep(self.TRAVEL_DURATION)
        self.left_motor.set_power(0)
        self.right_motor.set_power(0)
        # After the duration ends, stop the motors
        self.stop_motors()



    def turn(self, turn_angle):
        """Turn the robot by a number of degrees, without changing its coordinates.
        
        Parameters:
            turn_angle -- Turn a number of degrees clockwise
        """

        

        # How many degrees for the wheels before we travel the fraction of turn rate?
        degrees_to_turn = (self.TURN_RATE * turn_angle) / self.WHEEL_CIRCUMFERENCE
        print(degrees_to_turn)
        # Travel self.turn_rate in 1 second
        # Set the right motor to go backward
        self.right_motor.set_limits(dps=360, power=-50)
        self.right_motor.set_position_relative(-360)
        # Set the left motor to go forward
        self.left_motor.set_limits(dps=360, power=50)
        self.left_motor.set_position_relative(360)
        time.sleep(12)
        # Wait for the full turn duration to rotate 90 degrees
        # time.sleep(self.TURN_DURATION * (turn_angle / 360))
        
        # After the duration ends, stop the motors
        # self.stop_motors()

    
    def adjust_direction(self):
        """Adjust the robots position if it ever trails off the line, determined by the color sensor detecting a different color than expected.
        Initial idea is to spin the robot to the left by 20 degrees to check if the line is in the 20 degrees to its left 
            (assumes it went off on the right side of the street line). If line is found, continue previous instruction
        Else, spin to right by 20 degrees to reset, and then another 20 degrees to the right to check if line is in the 20 degrees
            to its right (assumes it went off on the left side of the street lane)
        
        """
        # Doesn't have to be 20 degrees, have to account for edge cases, many tests involved
        pass
    
        
if __name__ == "__main__":
    #conduct any testing here
    print("Running main...")
    pass
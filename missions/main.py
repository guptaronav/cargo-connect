from spike import PrimeHub, Motor, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import math
from math import *
from spike import MotorPair

# Initialize the Distance Sensor.
distance = DistanceSensor('D')
hub= PrimeHub
# Initialize the Color Sensor
color = ColorSensor('B')
left_motor = Motor('C')
left_motor.stop()
left_motor.set_stop_action('coast')

# If the left motor is connected to Port B,
# and the right motor is connected to Port A.
motor_pair = MotorPair('A', 'E')
motor_pair.set_default_speed(40)
motor_pair.set_stop_action('coast')

def move_to_black():
    motor_pair.start()
    color.wait_until_color('black')
    motor_pair.stop()

def move_x_bot(distance):
    motor_pair.start()
    motor_pair.move_tank(distance, 'cm', left_speed=40, right_speed=40)
    motor_pair.stop()

def s_move():
    motor_pair.start()
    motor_pair.move_tank(6, 'cm', left_speed=15, right_speed=30)
    motor_pair.stop()
    motor_pair.start()
    motor_pair.move_tank(6, 'cm', left_speed=30, right_speed=15)
    motor_pair.stop()

def go_around():
    motor_pair.move(65, unit='cm', steering=0)
    motor_pair.move_tank(20, 'cm', left_speed=20, right_speed=40)
    motor_pair.move_tank(20, 'cm', left_speed=20, right_speed=40)
    motor_pair.move(30, unit='cm', steering=0)
    motor_pair.move_tank(10, 'cm', left_speed=20, right_speed=40)
    motor_pair.move(45, unit='cm', steering=0)
    motor_pair.move(50, unit='cm', steering=0, speed=100)

###################### ROUND 1 ###########################
move_to_black()

#turn robot
motor_pair.start()
motor_pair.move_tank(3, 'cm', left_speed=20, right_speed=20)
motor_pair.move_tank(17, 'cm', left_speed=43, right_speed=20)

# Mission 05: Switch engine (20 points)
left_motor.start()
left_motor.run_for_degrees(50,7)
left_motor.stop()
motor_pair.move_tank(-18, 'cm', left_speed=45, right_speed=20)
motor_pair.move_tank(-5, 'cm', left_speed=20, right_speed=20)
# Make a tank move
motor_pair.move_tank(10, 'cm', left_speed=40, right_speed=-56)

# Mission 03: Unload Cargo Plane (20+10+10)
left_motor.run_for_seconds(1,70)
# Raise the right Hand
left_motor.run_for_degrees(-100,60)    

# Mission 13: Platooning Trucks (10+10+10)
motor_pair.move_tank(33, 'cm', left_speed=35, right_speed=41)
motor_pair.move_tank(6, 'cm', left_speed=20, right_speed=20)
motor_pair.move_tank(-20, 'cm', left_speed=20, right_speed=20)

# S-Move
s_move()
move_to_black()


from spike import PrimeHub, LightMatrix, Button, StatusLight, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer

from math import *

hub= PrimeHub
# Initialize the Color Sensor
color = ColorSensor('B')

left_motor = Motor('C')
left_motor.set_default_speed(40)
# left_motor.set_stop_action('coast')

motor_pair = MotorPair('A', 'E')
motor_pair.set_default_speed(40)
motor_pair.set_stop_action('coast')

def move_to_black(initialDelay=0):
    motor_pair.start()
    wait_for_seconds(initialDelay)
    color.wait_until_color('black')
    motor_pair.stop()

def move_x_bot(distance, stop):
    motor_pair.start()
    motor_pair.move_tank(distance, 'cm', left_speed=40, right_speed=40)
    if stop:
        motor_pair.stop()

def s_move():
    motor_pair.start()
    motor_pair.move_tank(7, 'cm', left_speed=15, right_speed=30)
    motor_pair.stop()
    motor_pair.start()
    motor_pair.move_tank(7, 'cm', left_speed=30, right_speed=15)
    motor_pair.stop()

def go_around():
    motor_pair.move(65, unit='cm', steering=0)
    motor_pair.move_tank(20, 'cm', left_speed=20, right_speed=40)
    motor_pair.move_tank(20, 'cm', left_speed=20, right_speed=40)
    motor_pair.move(30, unit='cm', steering=0)
    motor_pair.move_tank(10, 'cm', left_speed=20, right_speed=40)
    motor_pair.move(45, unit='cm', steering=0)
    motor_pair.move(50, unit='cm', steering=0, speed=100)

# Mission 05: Switch engine (20 points)
def mission_05():
    left_motor.start()
    left_motor.run_for_degrees(50,6)
    left_motor.stop()

# Mission 03: Unload Cargo Plane (20+10+10)
def mission_03():
    left_motor.start()
    left_motor.run_for_seconds(1,70)
    # Move the right Hand forward 
    left_motor.run_for_degrees(-170,60)
    left_motor.stop()

###################### ROUND 1 ###########################
# move_x_bot(20)
move_to_black(1)

#turn robot
motor_pair.start()
motor_pair.move_tank(4, 'cm', left_speed=20, right_speed=20)
motor_pair.stop()
motor_pair.start()
#motor_pair.move_tank(15, 'cm', left_speed=30, right_speed=20)
motor_pair.move_tank(312, 'degrees', left_speed=30, right_speed=20)
motor_pair.stop()

mission_05()

motor_pair.start()
# motor_pair.move_tank(-15, 'cm', left_speed=30, right_speed=20)
motor_pair.move_tank(-312, 'degrees', left_speed=30, right_speed=20)
motor_pair.stop()
motor_pair.start()
motor_pair.move_tank(-6, 'cm', left_speed=30, right_speed=30)
# Make a tank move
motor_pair.stop()
motor_pair.start()
motor_pair.move_tank(9, 'cm', left_speed=40, right_speed=-57)
motor_pair.stop()

mission_03()

# # Mission 13: Platooning Trucks (10+10+10)
motor_pair.start()
motor_pair.move_tank(28, 'cm', left_speed=35, right_speed=40)
motor_pair.stop()
motor_pair.start()
motor_pair.move_tank(8, 'cm', left_speed=30, right_speed=30)
# motor_pair.move_tank(-20, 'cm', left_speed=20, right_speed=20)
motor_pair.stop()

move_x_bot(-12,True)
# # S-Move
s_move()
move_to_black()

move_x_bot(8,True)
move_x_bot(-8,True)

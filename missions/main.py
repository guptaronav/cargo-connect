from spike import PrimeHub, LightMatrix, Button, StatusLight, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import sys
from math import *

hub=PrimeHub()
# Initialize the Color Sensor
color = ColorSensor('B')

left_motor = Motor('D')
left_motor.set_default_speed(40)
# left_motor.set_stop_action('coast')

motor_pair = MotorPair('A', 'E')
motor_pair.set_default_speed(40)
motor_pair.set_stop_action('coast')

hub.motion_sensor.reset_yaw_angle()

def get_yaw():
    return hub.motion_sensor.get_yaw_angle()

def print_yaw(name):
    print(name, get_yaw())

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
    motor_pair.move_tank(6.5, 'cm', left_speed=15, right_speed=30)
    motor_pair.stop()
    motor_pair.start()
    motor_pair.move_tank(6.5, 'cm', left_speed=30, right_speed=15)
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
    left_motor.run_for_degrees(50,5)
    left_motor.stop()

# Mission 03: Unload Cargo Plane (20+10+10)
def mission_03():
    left_motor.start()
    left_motor.run_for_seconds(1,70)
    # Move the right Hand forward 
    left_motor.run_for_degrees(-170,60)
    left_motor.stop()

def tank_to_yaw(angle):
    motor_pair.start_tank(left_speed=5, right_speed=-5)
    while True:
        a=get_yaw()
        if a < angle:
            print_yaw("Yaw")
        else:
            motor_pair.stop()
            print_yaw("Yaw")
            break

def turn_to_yaw(angle):
    motor_pair.start_tank(left_speed=20, right_speed=10)
    while True:
        a=get_yaw()
        if a < angle - 1:
            print_yaw("Yaw")
        else:
            motor_pair.stop()
            print_yaw("Yaw")
            break
    
def turn_to_yaw(arc_angle, radius):
    motor_pair.start_tank(left_speed=20/radius, right_speed=20)
    while True: 
        a=get_yaw()
        if a < arc_angle - 1:
            print_yaw("Yaw")
        else:
            motor_pair.stop()
            print_yaw("Yaw")
            break

###################### ROUND 1 ###########################
# move_x_bot(20)
print_yaw("start")

turn_to_yaw(90, 2)
sys.exit()

move_to_black(1)

#turn robot
move_x_bot(4,True)
motor_pair.start()
motor_pair.move_tank(312, 'degrees', left_speed=30, right_speed=20)
motor_pair.stop()

move_x_bot(-1,True)
print_yaw("Before M05 Switch engine")
mission_05()

motor_pair.start()
motor_pair.move_tank(-310, 'degrees', left_speed=33, right_speed=20)
motor_pair.stop()
print_yaw("After M05 Switch engine")
move_x_bot(-6,True)

motor_pair.start()
motor_pair.move_tank(10.4, 'cm', left_speed=40, right_speed=-60)
motor_pair.stop()
move_x_bot(-2,True)
print_yaw("Before M03 Unload Cargo Plane")
mission_03()


# # Mission 13: Platooning Trucks (10+10+10)
motor_pair.start()
motor_pair.move_tank(28, 'cm', left_speed=35, right_speed=40)
motor_pair.stop()
motor_pair.start()
motor_pair.move_tank(8, 'cm', left_speed=30, right_speed=30)
# motor_pair.move_tank(-20, 'cm', left_speed=20, right_speed=20)
motor_pair.stop()
print_yaw("After M13 Platooning Trucks")
move_x_bot(-12,True)
sys.exit()
# # S-Move
s_move()
move_to_black()

move_x_bot(15,True)
move_x_bot(-15,True)

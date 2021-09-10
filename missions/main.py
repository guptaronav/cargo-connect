from spike import PrimeHub, Motor, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import math
from math import *

# Initialize the Distance Sensor.
distance = DistanceSensor('D')
hub= PrimeHub
# Initialize the Color Sensor
color = ColorSensor('B')
left_motor = Motor('C')

from spike import MotorPair

# If the left motor is connected to Port B,
# and the right motor is connected to Port A.
motor_pair = MotorPair('A', 'E')
motor_pair.set_default_speed(40)
motor_pair.set_stop_action('coast')

# motor_pair.start()
# move straight from starting box and turn right some angle
#motor_pair.move_tank(20, 'cm', left_speed=80, right_speed=57)
#motor_pair.set_motor_rotation(8.25 * math.pi, 'cm')
# move straight till you get to the bridge at constant speed


# def left_turn_end():
#         return hub.motion_senor.get_yaw_andle() >90

# wait_until(left_turn_end)
# motor_pair.stop();

# Robot Go around
# motor_pair.move(65, unit='cm', steering=0)
# motor_pair.move_tank(20, 'cm', left_speed=20, right_speed=40)
# motor_pair.move_tank(20, 'cm', left_speed=20, right_speed=40)
# motor_pair.move(30, unit='cm', steering=0)
# motor_pair.move_tank(10, 'cm', left_speed=20, right_speed=40)
# motor_pair.move(45, unit='cm', steering=0)

motor_pair.move(50, unit='cm', steering=0, speed=100)
# color.wait_until_color('black')
# motor_pair.stop();
# left_motor.run_for_degrees(-290,100)

# motor_pair.move_tank(10, 'cm', left_speed=40, right_speed=20)
# motor_pair.start()
# color.wait_until_color('black')
# motor_pair.stop();

#distance_sensor.wait_for_distance_close_than(15,'cm')
#if distance.get_distance_cm()<12:
    #motor_pair.stop()

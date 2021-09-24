from spike import PrimeHub, LightMatrix, Button, StatusLight, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import sys
import math

hub = PrimeHub()
color = ColorSensor('B')
left_motor = Motor('D')
left_motor.set_default_speed(40)
motor_pair = MotorPair('A', 'E')
wheel_radius = 4.4
axle_width = 12.5
default_speed = 30
turn_speed = 30
yaw_speed = 10
stop_action = 'coast' # values: brake | hold | coast
rotate_cm_deg = (math.pi * axle_width) / 360;

def setup():
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.set_stop_action(stop_action)
    motor_pair.set_motor_rotation(2 * math.pi * wheel_radius, 'cm')
    motor_pair.set_default_speed(default_speed)

def exit():
    sys.exit();

def wait(secs=0):
    wait_for_seconds(secs)

def start(steering=0, speed=default_speed):
    motor_pair.start(steering, speed);

def start_for(secs, steering=0, speed=default_speed):
    start(steering, speed);
    wait(secs);
    stop();

def back(steering=0, speed=default_speed):
    motor_pair.start(steering, -speed);

def back_for(secs, steering=0, speed=default_speed):
    reverse(steering, speed);
    wait(secs);
    stop();

def stop():
    motor_pair.stop();

def turn_right(deg, dur, speed=turn_speed):
   start(deg, speed)
   wait(dur)
   start();

def turn_left(deg, dur, speed=turn_speed):
    start(-deg, speed)
    wait(dur)
    start();

def rotate_right(deg, speed=turn_speed):
    stop();
    motor_pair.move(rotate_cm_deg * deg, 'cm', steering=100)

def rotate_left(deg, speed=turn_speed):
    stop();
    motor_pair.move(rotate_cm_deg * deg, 'cm', steering=-100)

def circle_right(value):
    motor_pair.start(value)

def circle_left(value):
    motor_pair.start(-value)

def get_yaw():
    return hub.motion_sensor.get_yaw_angle()

def print_yaw(name):
    print(name, get_yaw())

def move_to_color(colorStr, delay=0):
    start()
    wait_for_seconds(delay)
    color.wait_until_color(colorStr)
    stop()

def move_to_black(delay=0):
    move_to_color('black', delay)

def move_to_white(delay=0):
    move_to_color('white', delay)

def move(cms):
    motor_pair.move(cms)

def reverse(cms):
    motor_pair.move(cms, steering=-100)

def rotate_right_yaw(angle,speed=yaw_speed):
    motor_pair.start_tank(left_speed=speed, right_speed=-speed)
    while True:
        a=get_yaw()
        if a < angle - 1:
            get_yaw()
        else:
            motor_pair.stop()
            break

def rotate_left_yaw(angle,speed=yaw_speed):
    motor_pair.start_tank(left_speed=-speed, right_speed=speed)
    while True:
        a=get_yaw()
        if a < angle - 1:
            get_yaw()
        else:
            motor_pair.stop()
            break

setup();

rotate_right_yaw(90)

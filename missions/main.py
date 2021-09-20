from spike import PrimeHub, LightMatrix, Button, StatusLight, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

# Initialize Hub
hub=PrimeHub()

# Initialize the Color Sensor
color = ColorSensor('B')

# Initialize Left Hand
left_motor = Motor('D')
left_motor.set_default_speed(40)

# Initialize Motor Pair
motor_pair = MotorPair('A', 'E')
motor_pair.set_default_speed(30)
motor_pair.set_stop_action('coast')

# Initialize Timer
timer = Timer()

def reset_yaw():
    hub.motion_sensor.reset_yaw_angle()

def get_yaw():
    return hub.motion_sensor.get_yaw_angle()

def print_yaw(name):
    print(name + ", yaw =", get_yaw())

def print_color_sensor_stats():
    print("Reflected",color.get_reflected_light(),"Ambient",color.get_ambient_light(), "RGB", color.get_rgb_intensity())

def wait_for_black():
    while True:
        (r,g,b,i) = color.get_rgb_intensity()
        c = color.get_color()
        if r < 80 and b < 80 and g < 80:
            print("FOUND",r,g,b,i,c)
            # 54 73 73 148
            # 62 78 79 162
            break
        else:
            print(r,g,b,i,c)
            continue

def move_to_black(initialDelay=0):
    motor_pair.start()
    wait_for_seconds(initialDelay)
    color.wait_until_color('black')
    motor_pair.stop()

def move_x_bot(distance, stop):
    motor_pair.start()
    motor_pair.move_tank(distance, 'cm', left_speed=50, right_speed=50)
    if stop:
        motor_pair.stop()

def turn_x_bot(degrees, left_speed, right_speed):
    motor_pair.start()
    motor_pair.move_tank(degrees, 'degrees', left_speed, right_speed)
    motor_pair.stop()

def s_move(degrees, left_speed, right_speed):
    turn_x_bot(degrees,left_speed,right_speed)
    turn_x_bot(degrees,right_speed,left_speed)


def go_around():
    motor_pair.move(65, unit='cm', steering=0)
    motor_pair.move_tank(20, 'cm', left_speed=20, right_speed=40)
    motor_pair.move_tank(20, 'cm', left_speed=20, right_speed=40)
    motor_pair.move(30, unit='cm', steering=0)
    motor_pair.move_tank(10, 'cm', left_speed=20, right_speed=40)
    motor_pair.move(45, unit='cm', steering=0)
    motor_pair.move(50, unit='cm', steering=0, speed=100)


def tank_to_yaw(angle, speed):
    motor_pair.start_tank(speed, -speed)
    while True:
        if get_yaw() >= angle - 1:
            motor_pair.stop()
            print_yaw("Tank Yaw")
            break

def turn_right_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    left_speed = int(speed * ratio)
    print("left",left_speed,"right",speed)
    motor_pair.start_tank(left_speed, right_speed=speed)
    while True:
        a=get_yaw()
        if a >= angle - 1:
            motor_pair.stop()
            print_yaw("Yaw")
            break

def back_right_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    left_speed = int(speed * ratio)
    print("left",left_speed,"right",speed)
    motor_pair.start_tank(left_speed, right_speed=speed)
    while True:
        a=get_yaw()
        if a <= angle + 1:
            motor_pair.stop()
            print_yaw("Yaw")
            break

def turn_left_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    right_speed = int(speed * ratio)
    print("left",speed,"right",right_speed)
    motor_pair.start_tank(speed, right_speed)
    while True:
        a=get_yaw()
        if a <= angle + 1:
            motor_pair.stop()
            print_yaw("Yaw")
            break

def back_left_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    right_speed = int(speed * ratio)
    print("left",speed,"right",right_speed)
    motor_pair.start_tank(speed, right_speed)
    while True:
        a=get_yaw()
        if a >= angle - 1:
            motor_pair.stop()
            print_yaw("Yaw")
            break

def s_move_new(speed, radius):
    yaw=get_yaw()
    turn_left_to_yaw(yaw-45,speed,radius)
    turn_right_to_yaw(yaw,speed,radius)

def set_position(pos):
    yaw=get_yaw()
    if yaw < pos:
        print("Turning a bit right to set yaw from", yaw, "to", pos)
        turn_right_to_yaw(pos,5,2) #angle, speed, radius
    elif yaw > pos:
        print("Turning a bit left to set yaw from", yaw, "to", pos)
        turn_left_to_yaw(pos,5,2)

def initialize_x_bot():
    timer.reset()
    print("========================================")
    print_yaw("Initializing")
    move_x_bot(-2,True)
    left_motor.start()
    left_motor.run_for_seconds(1,-10)
    left_motor.stop()
    reset_yaw()
    
# Mission 05: Switch engine (20 points)
def mission_05():
    print_yaw("Mission 05: Switch engine")
    move_to_black(1)
    move_x_bot(4,True)
    print_yaw("Mission 05: Before turn")
    turn_right_to_yaw(89,10,4.6) #angle, speed, radius in inches
    # turn_x_bot(312,30,20)
    print_yaw("Mission 05: After turn")
    move_x_bot(-1,True)
    left_motor.start()
    left_motor.run_for_degrees(40,4)
    left_motor.stop()
    move_x_bot(1,True)
    # turn_x_bot(-310,33,20)
    back_right_to_yaw(-40,-10,5.5) #angle, speed, radius in inches
    print_yaw("Mission 05: Back to original")


# Mission 03: Unload Cargo Plane (20+10+10)
def mission_03():
    print_yaw("Mission 03: Unload Cargo Plane")
    move_x_bot(-6,True)
    tank_to_yaw(129,20) #angle, speed
    # turn_x_bot(240,40,-60)
    print_yaw("Mission 03: After Tank Move")
    move_x_bot(-5.5,True)
    left_motor.start()
    left_motor.run_for_seconds(1,60)
    # Move the right Hand forward
    left_motor.run_for_degrees(-170,60)
    left_motor.stop()


# Mission 13: Platooning Trucks (10+10+10)
def mission_13():
    set_position(136)
    print_yaw("Mission 13: Platooning Trucks")
    turn_left_to_yaw(89,20,16)  #angle, speed, radius in inches
    # turn_x_bot(350,35,43)
    set_position(90)
    print_yaw("Mission 13: After turning")
    motor_pair.start()
    motor_pair.move_tank(12, 'cm', left_speed=30, right_speed=30)
    motor_pair.stop()
    print_yaw("Mission 13: After moving the truck")
    move_x_bot(-12,True)
    set_position(90)

# Mission 14: Bridge (10+10)
def mission_14():
    print_yaw("Mission 14: Bridge")
    s_move_new(10,9) #speed, radius
    set_position(90)
    # s_move(130,15,30)
    move_to_black()
    move_x_bot(25,True)
    print_yaw("Mission 14: After First Bridge")
    move_x_bot(-40,True)
    print_yaw("Mission 14: After Second Bridge")

# Mission 07: Unload Cargo Ship (20+10)
def mission_07():
    set_position(90)
    print_yaw("Mission 07: Unload Cargo Ship")
    s_move_new(15,8) #speed, radius
    # s_move(150,23,40)
    move_x_bot(20,True)

# Mission 08: Air Drop (20+10+10)
def mission_08():
    print_yaw("Mission 08: Air Drop")
    move_x_bot(-15,True)
    exit()
    back_left_to_yaw(130,20,4) #angle, speed, radius in inches
    turn_left_to_yaw(45,20,40)
    # turn_x_bot(-100,20,30)


# Mission 04: Transportation Journey (10+10+10)
def mission_04():
    print_yaw("Mission 04: Transportation Journey")


# Mission 01: Innovation Project Model (20)
def mission_01():
    print_yaw("Mission 01: Innovation Project Model")

# Mission 02: Unused Capacity (20+10)
def mission_02():
    print_yaw("Mission 02: Unused Capacity")

# Mission 06: Accident Avoidance (20+10)
def mission_06():
    print_yaw("Mission 06: Accident Avoidance")

# Mission 09: Train Tracks (20+20)
def mission_09():
    print_yaw("Mission 09: Train Tracks")

# Mission 10: Sorting Center (20)
def mission_10():
    print_yaw("Mission 10: Sorting Center")

# Mission 11: Home Delivery (20+10)
def mission_11():
    print_yaw("Mission 11: Home Delivery")

# Mission 12: Large Delivery (20+10 + 5+5)
def mission_12():
    print_yaw("Mission 12: Large Delivery")

# Mission 15: Load Cargo (100+)
def mission_15():
    print_yaw("Mission 15: Load Cargo")

# Mission 16: Cargo Connect (5+5+20+20+10)
def mission_16():
    print_yaw("Mission 16: Cargo Connect")
    
###################### ROUND 1 ###########################
initialize_x_bot()
# tank_to_yaw(136,20)
# exit()

mission_05()
mission_03()
mission_13()
mission_14()
mission_07()
mission_08()
mission_04()
print("Time taken = ", timer.now())

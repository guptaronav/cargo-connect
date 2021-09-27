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
front_motor = Motor('F')

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

def move_cargo(height):
    front_motor.start()
    front_motor.run_for_degrees(height,20)
    front_motor.stop()

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

def tank_to_yaw(angle, speed):
    motor_pair.start_tank(speed, -speed)
    while True:
        if get_yaw() >= angle - 1: 
            motor_pair.stop()
            break
    
def tank_to_yaw_reverse(angle, speed):
    motor_pair.start_tank(-speed, speed)
    while True:
        if get_yaw() < angle + 2:
            motor_pair.stop()
            break

def tank_to_yaw_reverse_check_negative(angle, speed):
    if get_yaw() < 0:
        angle = -abs(angle)
    else:
        angle = abs(angle)
    motor_pair.start_tank(-speed, speed)
    while True:
     
        if get_yaw() < angle + 2:
            motor_pair.stop()
            break
def turn_right_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    left_speed = int(speed * ratio)
    motor_pair.start_tank(left_speed, right_speed=speed)
    while True:
        a=get_yaw()
        if a >= angle - 1:
            motor_pair.stop()
            break

def back_right_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    left_speed = int(speed * ratio)
    motor_pair.start_tank(left_speed, right_speed=speed)
    while True:
        a=get_yaw()
        if a <= angle + 1:
            motor_pair.stop()
            break

def turn_left_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    right_speed = int(speed * ratio)
    motor_pair.start_tank(speed, right_speed)
    while True:
        a=get_yaw()
        if a <= angle + 1:
            motor_pair.stop()
            break

def back_left_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    right_speed = int(speed * ratio)
    motor_pair.start_tank(speed, right_speed)
    while True:
        if get_yaw() >= angle - 1:
            motor_pair.stop()
            break

def s_move(speed, radius):
    yaw=get_yaw()
    turn_left_to_yaw(yaw-45,speed,radius)
    turn_right_to_yaw(yaw,speed,radius)

def s_move_reverse(speed, radius):
    yaw=get_yaw()
    back_left_to_yaw(90-yaw,-speed,radius)
    back_right_to_yaw(yaw,-speed,radius)

def set_position(pos):
    yaw=get_yaw()
    if yaw < pos - 1:
        print("Turning a bit right to set yaw from", yaw, "to", pos)
        turn_right_to_yaw(pos,4,2) #angle, speed, radius
    elif yaw > pos + 1:
        print("Turning a bit left to set yaw from", yaw, "to", pos)
        turn_left_to_yaw(pos,4,2)

def initialize_x_bot():
    timer.reset()
    print("========================================")
    print_yaw("Initializing")
    move_x_bot(-2,True)
    left_motor.start()
    left_motor.run_for_seconds(1,-10)
    left_motor.stop()
    #front_motor.run_to_position(242)
    reset_yaw()
    
# Mission 05: Switch engine (20 points)
def mission_05():
    print_yaw("Mission 05: Switch engine")
    move_to_black(1)
    move_x_bot(4,True)
    set_position(0)
    print_yaw("Mission 05: Before turn")
    turn_right_to_yaw(89,10,4.65) #angle, speed, radius in inches
    set_position(90)
    print_yaw("Mission 05: After turn")
    move_x_bot(-1,True)
    left_motor.start()
    left_motor.run_for_degrees(40,4)
    left_motor.stop()
    move_x_bot(1,True)
    back_right_to_yaw(-40,-10,5.5) #angle, speed, radius in inches
    print_yaw("Mission 05: Back to original")


# Mission 03: Unload Cargo Plane (20+10+10)
def mission_03():
    print_yaw("Mission 03: Unload Cargo Plane")
    move_x_bot(-6,True)
    tank_to_yaw(128,20) #angle, speed
    set_position(130)
    print_yaw("Mission 03: After Tank Move")
    move_x_bot(-5.7,True)
    left_motor.start()
    left_motor.run_for_seconds(0.6,60)
    # Move the right Hand forward
    left_motor.run_for_degrees(-155,60)
    left_motor.stop()


# Mission 13: Platooning Trucks (10+10+10)
def mission_13():
    set_position(136)
    print_yaw("Mission 13: Platooning Trucks")
    turn_left_to_yaw(90,20,17)  #angle, speed, radius in inches
    set_position(90)
    print_yaw("Mission 13: After turning")
    motor_pair.start()
    motor_pair.move_tank(11, 'cm', left_speed=30, right_speed=30)
    motor_pair.stop()
    move_cargo(200)
    print_yaw("Mission 13: After moving the truck")
    move_x_bot(-12,True)
    set_position(90)

# Mission 14: Bridge (10+10)
def mission_14():
    print_yaw("Mission 14: Bridge")
    s_move(11,9) #speed, radius
    set_position(90)
    set_position(90)
    motor_pair.set_default_speed(60)
    move_x_bot(40,True)
    print_yaw("Mission 14: After First Bridge")
    move_x_bot(-50,True)
    print_yaw("Mission 14: After Second Bridge")
    motor_pair.set_default_speed(30)

# Mission 07: Unload Cargo Ship (20+10)
def mission_07():
    set_position(90)
    set_position(90)
    print_yaw("Mission 07: Unload Cargo Ship")
    s_move(15,8.2) #speed, radius
    set_position(90)
    print_yaw("Mission 07: After S-Move")
    move_x_bot(21,True)

# Mission 08: Air Drop (20+10+10)
def mission_08():
    print_yaw("Mission 08: Air Drop")
    move_x_bot(-4,True)
    set_position(90)
    back_left_to_yaw(130,-20,20)
    set_position(135)
    print_yaw("Mission 08: Before slam")
    turn_left_to_yaw(45,60,16)
    set_position(45)
    move_x_bot(5.4,True)
    turn_x_bot(30,30,10)
    move_x_bot(5,True)

# Mission 09: Train Tracks (20+20)
def mission_09():
    print_yaw("Mission 09: Train Tracks")
    #set_position(60)
    back_right_to_yaw(-0,-20,9) #angle, speed, radius in inches
    move_x_bot(-10,True)
    tank_to_yaw_reverse(-80,20) #angle, speed
    move_x_bot(-5,True)
    set_position(-90)
    left_motor.start()
    left_motor.run_for_seconds(1,18)
    left_motor.stop()
    move_x_bot(5,True)
    #left_motor.run_for_degrees(-150,60)
    #tank_to_yaw(0,20)
    #set_position(0)
    
def push_train():
    #s_move(12,7)
    reset_yaw()
    move_cargo(200)
    turn_left_to_yaw(-60,10,4) #angle, speed radius
    #move_x_bot(2, True)
    turn_right_to_yaw(0,10,4)
    set_position(0)
    move_x_bot(-5, True)
    motor_pair.set_default_speed(100)
    move_x_bot(29, True)
    motor_pair.set_default_speed(20)
    move_cargo(-100)
    back_right_to_yaw(-45,-10,4)
    back_left_to_yaw(0,-10,4)
    set_position(0)
    move_x_bot(-15, True)
    turn_right_to_yaw(90,10,5)
    set_position(90)
    move_x_bot(50,True)
    s_move(8,2) #speed, radius
    set_position(90)
    move_x_bot(50,True)

def mission_09_2():
    print_yaw("Mission 09_2: Train Tracks 2")
    left_motor.run_for_degrees(-90,60)
    move_x_bot(-4,True)
    tank_to_yaw_reverse_check_negative(-178,20)
    print_yaw("Mission 09_2: Before reversing")
    motor_pair.set_default_speed(-40)
    motor_pair.start()
    wait_for_seconds(2)
    motor_pair.stop()
    motor_pair.set_default_speed(30)
    print_yaw("Mission 09_2: After reversing")
    push_train()
    exit()


# Mission 02: Unused Capacity (20+10)
def mission_02():
    print_yaw("Mission 02: Unused Capacity")
    turn_left_to_yaw(-86,20,5.5)
    set_position(-90)
    print_yaw("Mission 02: Turned back")
    move_x_bot(40,True)
    s_move(17,5) #speed, radius
    print_yaw("Mission 02: After S Move")
    set_position(-86)
    move_x_bot(50,True)



# Mission 04: Transportation Journey (10+10+10)
def mission_04():
    print_yaw("Mission 04: Transportation Journey")

# Mission 01: Innovation Project Model (20)
def mission_01():
    print_yaw("Mission 01: Innovation Project Model")

# Mission 06: Accident Avoidance (20+10)
def mission_06():
    print_yaw("Mission 06: Accident Avoidance")

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

def round_one():
    initialize_x_bot()
    #move_cargo(-200) #reset
    mission_05() # switch engine
    mission_03() # unload cargo plane
    mission_13() # platooning trucks
    mission_14() # bridge closing
    mission_07() # unload cargo
    mission_08() # air drop
    mission_09() # part 1 - completing track
    mission_09_2() # part 2 - moving cars
    #mission_02() #unused capacity and come home
    print("Time taken = ", timer.now())

round_one()
#push_train()
#move_cargo(-200)

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

def move_cargo(height, speed=20):
    front_motor.start()
    front_motor.run_for_degrees(height,speed)
    front_motor.stop()

def move_to_black(initialDelay=0):
    motor_pair.start()
    wait_for_seconds(initialDelay)
    color.wait_until_color('black')
    motor_pair.stop()

def move_x_bot(distance, stop, speed=50):
    motor_pair.start()
    #motor_pair.move_tank(distance, 'cm', left_speed=50, right_speed=50)
    motor_pair.set_default_speed(speed)
    motor_pair.move(distance)
    motor_pair.set_default_speed(40)
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

def initialize_x_bot(move_hand = True):
    timer.reset()
    print("========================================")
    print_yaw("Initializing")
    left_motor.set_default_speed(10)
    move_x_bot(-2,True)
    if move_hand:
        left_motor.set_default_speed(40)
        left_motor.start()
        left_motor.run_for_seconds(1,-10)
        left_motor.stop()
    reset_yaw()
    
# Mission 05: Switch engine (20 points)
def mission_05():
    print_yaw("Mission 05: Switch engine")
    move_to_black(1)
    move_x_bot(4,True)
    set_position(0)
    print_yaw("Mission 05: Before turn")
    turn_right_to_yaw(89,12,4.65) #angle, speed, radius in inches
    set_position(90)
    print_yaw("Mission 05: After turn")
    move_x_bot(-1,True)
    left_motor.start()
    left_motor.run_for_degrees(40,4)
    left_motor.stop()
    move_x_bot(1,True)
    back_right_to_yaw(-40,-12,5.5) #angle, speed, radius in inches
    print_yaw("Mission 05: Back to original")


# Mission 03: Unload Cargo Plane (20+10+10)
def mission_03():
    print_yaw("Mission 03: Unload Cargo Plane")
    move_x_bot(-6,True)
    tank_to_yaw(129,20) #angle, speed
    set_position(130)
    print_yaw("Mission 03: After Tank Move")
    move_x_bot(-5.8,True)
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
    move_x_bot(-14,True)
    set_position(90)

# Mission 14: Bridge (10+10)
def mission_14():
    print_yaw("Mission 14: Bridge")
    s_move(11,9) #speed, radius
    set_position(90)
    set_position(90)
    motor_pair.set_default_speed(50)
    move_x_bot(40,True)
    print_yaw("Mission 14: After First Bridge")
    move_x_bot(-49,True)
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
    move_x_bot(20.6,True)

# Mission 08: Air Drop (20+10+10)
def mission_08():
    print_yaw("Mission 08: Air Drop")
    move_x_bot(-4,True)
    set_position(90)
    back_left_to_yaw(130,-20,20)
    set_position(135)
    left_motor.start()
    # Move the right Hand forward
    left_motor.run_for_degrees(55,60)
    left_motor.stop()
    print_yaw("Mission 08: Before slam")
    turn_left_to_yaw(45,60,16)
    set_position(45)
    move_x_bot(5.4,True)
    turn_x_bot(30,30,10)
    move_x_bot(5,True)

# Mission 09: Train Tracks (20+20)
def mission_09():
    print_yaw("Mission 09: Train Tracks")
    back_right_to_yaw(0,-20,9) #angle, speed, radius in inches
    move_x_bot(-10,True)
    tank_to_yaw_reverse(-80,20) #angle, speed
    move_x_bot(-5,True)
    set_position(-90)
    left_motor.start()
    left_motor.run_for_seconds(1,18)
    left_motor.stop()
    move_x_bot(6,True)
    #left_motor.run_for_degrees(-150,60)
    #tank_to_yaw(0,20)
    #set_position(0)
    
def push_train():
    print_yaw("Push Train")
    reset_yaw()
    print_yaw("Push Train: After Yaw Reset")
    move_cargo(300)
    turn_left_to_yaw(-60,10,4) #angle, speed radius
    # move_x_bot(0.5, True)
    turn_right_to_yaw(0,10,4)
    set_position(0)
    print_yaw("Push Train: before stepping back")
    move_x_bot(-5, True)
    motor_pair.set_default_speed(100)
    move_x_bot(30, True)
    motor_pair.set_default_speed(20)
    print_yaw("Push Train: after the run")
    move_cargo(-300)
    back_right_to_yaw(-45,-10,4)
    back_left_to_yaw(0,-10,4)
    set_position(0)
    print_yaw("Push Train: back up")
    move_x_bot(-15, True)
    turn_right_to_yaw(90,10,5)
    set_position(90)

def mission_09_2():
    print_yaw("Mission 09_2: Train Tracks 2")
    left_motor.run_for_degrees(-75,60)
    move_x_bot(-4,True)
    tank_to_yaw_reverse_check_negative(-176,20)
    print_yaw("Mission 09_2: Before reversing")
    motor_pair.set_default_speed(-40)
    motor_pair.start()
    wait_for_seconds(2)
    motor_pair.stop()
    turn_x_bot(10,0,-5)
    motor_pair.set_default_speed(30)
    print_yaw("Mission 09_2: After reversing")
    push_train()

# Mission 02: Unused Capacity (20+10)
def mission_02():
    print_yaw("Mission 02: Unused Capacity")
    move_x_bot(50,True)
    s_move(8,2.5) #speed, radius
    set_position(90)
    print_yaw("Mission 02: After S-Move")
    motor_pair.set_default_speed(100)
    move_x_bot(55,True)

## ROUND 2
def mission_16():
    print_yaw("Mission 16: Cargo Connect")
    turn_left_to_yaw(-10,10,4.65) #angle, speed, radius in inches
    move_x_bot(21,True)
    turn_right_to_yaw(47,10,10) #angle, speed, radius in inches
    move_x_bot(13.5,True)
    move_x_bot(-35,True)
    back_right_to_yaw(3,-20,5)

# Mission 01: Innovation Project Model (20)
def mission_01():
    print_yaw("Mission 01: Innovation Project Model")
    turn_right_to_yaw(86, 12, 4)
    set_position(90)
    move_x_bot(48, False, 30)
    turn_left_to_yaw(33, 12, 7)
    move_x_bot(-3, False, 30)
    back_left_to_yaw(88,-10,3)

def home_delivery():
    move_cargo(500)
    move_x_bot(-5,True, 60)
    turn_x_bot(40,60,60)
    turn_x_bot(-40,60,60)

# Mission 11: Home Delivery (20+10)
def mission_11():
    print_yaw("Mission 11: Home Delivery")
    turn_right_to_yaw(120,10,3)
    move_x_bot(12.5, True, 35)
    turn_left_to_yaw(110,40,3)
    set_position(94)
    print_yaw("Mission 11: Before Delivery")
    home_delivery() #deliver
    move_cargo(-500,50)
    set_position(90)
    move_x_bot(9, True)
    back_left_to_yaw(110,-8,2) #getting out
    move_x_bot(-11, True, 50)
    print_yaw("Mission 11: Backing out")
    back_right_to_yaw(95,-8,2)
    set_position(90)
    
# Mission 10: Sorting Center (20)
def mission_10():
    print_yaw("Mission 10: Sorting Center")
    move_x_bot(-7, True, 50)
    turn_left_to_yaw(50,10,8)
    move_x_bot(30, True, 50)
    tank_to_yaw(140,30)

# Mission 06: Accident Avoidance (20+10)
def mission_06():
    print_yaw("Mission 06: Accident Avoidance")

# Mission 04: Transportation Journey (10+10+10)
def mission_04():
    print_yaw("Mission 04: Transportation Journey")
    #not attempting

# Mission 12: Large Delivery (20+10 + 5+5)
def mission_12():
    print_yaw("Mission 12: Large Delivery")
    #not attempting

# Mission 15: Load Cargo (100+)
def mission_15():
    print_yaw("Mission 15: Load Cargo")
    #not attempting

def test_cargo():
    move_cargo(200) #platooning trucks
    wait_for_seconds(5)
    move_cargo(300) # Bay
    wait_for_seconds(5)
    move_cargo(-300) # Raise

###################### ROUND 1 ###########################

def round_one():
    initialize_x_bot()
    mission_05() # switch engine
    mission_03() # unload cargo plane
    mission_13() # platooning trucks
    mission_14() # bridge closing
    mission_07() # unload cargo
    mission_08() # air drop
    mission_09() # part 1 - completing track
    mission_09_2() # part 2 - moving cars
    mission_02() #unused capacity and come home

###################### ROUND 2 ###########################
def round_two():
    initialize_x_bot(False)
    mission_16() # cargo connect

###################### ROUND 3 ###########################
def round_three():
    initialize_x_bot(False)
    mission_01() # innovation project model
    mission_11() # home delivery
    mission_10() # sorting center
    mission_06() # accident avoidance - last one


#round_one()
#push_train()
#round_two()
#move_cargo(-500)
round_three()

print("Time taken = ", timer.now())

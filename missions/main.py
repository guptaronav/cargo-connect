from spike import PrimeHub, LightMatrix, Button, StatusLight, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

# Initialize Hub
hub=PrimeHub()

# Initialize the Color Sensor
color_left = ColorSensor('B')
color_right = ColorSensor('C')


# Initialize Left Hand
left_motor = Motor('D')
left_motor.set_default_speed(40)
front_motor = Motor('F')

# Initialize Motor Pair
robot_speed=32
motor_pair = MotorPair('A', 'E')
motor_pair.set_default_speed(robot_speed)
motor_pair.set_stop_action('coast')
left_wheel = Motor('A')
right_wheel = Motor('E')

# Initialize Timer
timer = Timer()

#Prints Current Color Detected By The Right Sensor
def print_color_details():
    print("get_ambient_light",color_right.get_ambient_light())
    print("get_reflected_light",color_right.get_reflected_light())
    print("get_rgb_intensity",color_right.get_rgb_intensity())

def reset_yaw():
    hub.motion_sensor.reset_yaw_angle()

def get_yaw():
    return hub.motion_sensor.get_yaw_angle()

def print_yaw(name):
    print(name + ", yaw =", get_yaw())

def print_left(name):
    print(name + ", left =", left_wheel.get_degrees_counted())
    
def print_right(name):
    print(name + ", right =", right_wheel.get_degrees_counted())

#Moves Forklift To Default Height
def reset_cargo():
    print("reset_cargo")
    front_motor.start()
    front_motor.run_for_seconds(1)
    front_motor.run_for_degrees(-610, 100) #-110 -200
    front_motor.stop()

#Moves Forklift to Given Height
def move_cargo(height, speed=20):
    front_motor.start()
    front_motor.run_for_degrees(height,speed)
    front_motor.stop()

#Accelerates From Current to Target Speed In Given Time
def accelerate(current_speed, to_speed, time=0.5):
    increase_by=to_speed - current_speed
    rounds=20
    for i in range(rounds,0,-1):
        motor_pair.start(speed=int(to_speed - i*increase_by/rounds))
        wait_for_seconds(time/rounds)

#Decelerates From Current to Target Speed In Given Time
def decelerate(current_speed, to_speed, time=0.5):
    delta=to_speed - current_speed
    rounds=20
    for i in range(1,rounds+1,1):
        s=int(current_speed + i*delta/rounds)
        motor_pair.start(speed=s)
        wait_for_seconds(time/rounds)
        #print("i",i,"s",s)

#Moves X-Bot Given Degrees
def move_x_degrees(degrees):
    start=right_wheel.get_degrees_counted()
    if degrees > 0:
        while(right_wheel.get_degrees_counted() < start+degrees):
            wait_for_seconds(0.004)
    else:
        while(right_wheel.get_degrees_counted() > start+degrees):
            wait_for_seconds(0.004)

#Moves X-Bot Forever Until Left Sensor Detects Black Line
def move_to_black(initialDelay=0, stop=True, speed=40):
    motor_pair.set_default_speed(40)
    motor_pair.start()
    wait_for_seconds(initialDelay)
    color_left.wait_until_color('black')
    if stop:
        motor_pair.stop()
    motor_pair.set_default_speed(robot_speed)

#Moves X-Bot Forever Until Right Sensor Detects Black Line
def move_to_black2(initialDelay=0, stop=True, speed=40):
    motor_pair.set_default_speed(40)
    motor_pair.start()
    wait_for_seconds(initialDelay)
    color_right.wait_until_color('black')
    if stop:
        motor_pair.stop()
    motor_pair.set_default_speed(robot_speed)

#Moves X-Bot Forever Until Left Sensor Detects White
def move_to_white(initialDelay=0, stop=True, speed=40):
    motor_pair.set_default_speed(40)
    motor_pair.start()
    wait_for_seconds(initialDelay)
    color_left.wait_until_color('white')
    if stop:
        motor_pair.stop()
    motor_pair.set_default_speed(robot_speed)

#Moves X-Bot Given Distance And Speed
def move_x_bot(distance, stop, speed=50):
    motor_pair.start()
    motor_pair.set_default_speed(speed)
    motor_pair.move(distance)
    motor_pair.set_default_speed(robot_speed)
    if stop:
        motor_pair.stop()
        
#Turns X-Bot Given Degrees And Speed
def turn_x_bot(degrees, left_speed, right_speed):
    motor_pair.start()
    motor_pair.move_tank(degrees, 'degrees', left_speed, right_speed)
    motor_pair.stop()
    
#Turns X-Bot Using Both Wheels Forward
def tank_to_yaw(angle, speed):
    motor_pair.start_tank(speed, -speed)
    while True:
        if get_yaw() >= angle - 1: 
            motor_pair.stop()
            break
            
#Turns X-Bot Using Both Wheels Backwards To The Left
def tank_to_yaw_reverse(angle, speed):
    motor_pair.start_tank(-speed, speed)
    while True:
        if get_yaw() < angle + 2:
            motor_pair.stop()
            break
            
#Turns X-Bot Using Both Wheels Backwards To The Right
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

#Turns X-Bot To The Right
def turn_right_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    left_speed = int(speed * ratio)
    motor_pair.start_tank(left_speed, right_speed=speed)
    while True:
        a=get_yaw()
        if a >= angle - 1:
            motor_pair.stop()
            break

#Turns X-Bot To The Right Backwards
def back_right_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    left_speed = int(speed * ratio)
    motor_pair.start_tank(left_speed, right_speed=speed)
    while True:
        a=get_yaw()
        if a <= angle + 1:
            motor_pair.stop()
            break

#Turns X-Bot To The Left
def turn_left_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    right_speed = int(speed * ratio)
    motor_pair.start_tank(speed, right_speed)
    while True:
        a=get_yaw()
        if a <= angle + 1:
            motor_pair.stop()
            break

#Turns X-Bot To The Left Backwards
def back_left_to_yaw(angle, speed, radius):
    ratio = 1 + (20 * 7 / (22 * radius))
    right_speed = int(speed * ratio)
    motor_pair.start_tank(speed, right_speed)
    while True:
        if get_yaw() >= angle - 1:
            motor_pair.stop()
            break

#Turns X-Bot In The Shape Of An S
def s_move(speed, radius):
    yaw=get_yaw()
    turn_left_to_yaw(yaw-45,speed,radius)
    turn_right_to_yaw(yaw,speed,radius)

#Turns X-Bot In The Shape Of An S Backwards
def s_move_reverse(speed, radius):
    yaw=get_yaw()
    back_left_to_yaw(90-yaw,-speed,radius)
    back_right_to_yaw(yaw,-speed,radius)

#Turns X-Bot To The Given Position
def set_position(pos):
    yaw=get_yaw()
    if yaw < pos - 1:
        print("Turning a bit right to set yaw from", yaw, "to", pos)
        tank_to_yaw(pos,4)
    elif yaw > pos + 1:
        print("Turning a bit left to set yaw from", yaw, "to", pos)
        tank_to_yaw_reverse(pos,4)

#Initializes X-Bot 
def initialize_x_bot(move_hand = True):
    timer.reset()
    print("========================================")
    print_yaw("Initializing")
    left_motor.set_default_speed(10)
    if move_hand:
        left_motor.set_default_speed(40)
        left_motor.start()
        left_motor.run_for_seconds(1,-10)
        left_motor.stop()
    reset_yaw()
    left_motor.set_degrees_counted(0)
    left_wheel.set_degrees_counted(0)
    right_wheel.set_degrees_counted(0)
    
# Mission 05: Switch engine (20 points)
def mission_05():
    print_yaw("Mission 05: Switch engine")
    move_x_bot(41,True,25)
    print_yaw("Mission 05: At Black Line")
    turn_right_to_yaw(88,12,4.8) #angle, speed, radius in 
    print_yaw("Mission 05: About to switch engine")
    left_motor.start()
    left_motor.run_for_degrees(40,4)
    left_motor.run_for_degrees(-14,4)
    left_motor.stop()
    back_right_to_yaw(40,-12,5.9)
    print_yaw("Mission 05: Before backing up into unfilled cargo")
    accelerate(0,-robot_speed,0.2)
    move_x_degrees(-390)
    decelerate(-robot_speed,0,0.2)
    print_yaw("Mission 05: After backing up")    

# Mission 03: Unload Cargo Plane (20+10+10)
def mission_03():
    print_yaw("Mission 03: Unload Cargo Plane")
    turn_right_to_yaw(132,12,4.2)
    left_motor.start()
    left_motor.run_for_seconds(0.6,60)
    left_motor.run_for_degrees(-150,60)
    left_motor.stop()
    accelerate(0,robot_speed,0.2)
    decelerate(robot_speed,0,0.2)
    print_yaw("Mission 03: Unload Cargo Done")
    print_left("Mission 03")

# Mission 13: Platooning Trucks (10+10+10)
def mission_13():
    set_position(137)
    print_yaw("Mission 13: Platooning Trucks")
    move_to_black(0,True,40)
    tank_to_yaw_reverse(95,9)
    set_position(90)
    print_yaw("Mission 13: After turning")
    accelerate(0,robot_speed,0.2)
    move_x_degrees(390) #170
    decelerate(robot_speed,0,0.3)
    move_cargo(200)
    print_yaw("Mission 13: After moving the truck")
    accelerate(0,-robot_speed,0.2)
    move_x_degrees(-200)
    decelerate(-robot_speed,0,0.3)
    set_position(90)
    print_left("Mission 13")

# Mission 14: Bridge (10+10)
def mission_14():
    print_yaw("Mission 14: Bridge")
    turn_left_to_yaw(44.7,11,8.75)
    turn_right_to_yaw(90,11,8.75)
    print_yaw("Mission 14: After S-Move")
    set_position(90)
    accelerate(0, 80, 0.2)
    move_x_degrees(500)
    print_yaw("Mission 14: Before Decelerate")
    decelerate(80,0,0.5)
    print_yaw("Mission 14: After First Bridge")
    set_position(90)
    accelerate(0, -80, 0.2)
    move_x_degrees(-600)
    decelerate(-80,0,0.5)
    set_position(90)
    print_yaw("Mission 14: After Second Bridge")
    print_left("Mission 14")

# Mission 07: Unload Cargo Ship (20+10)
def mission_07():
    set_position(90)
    print_yaw("Mission 07: Unload Cargo Ship")
    turn_left_to_yaw(45,15,7.8)
    turn_right_to_yaw(90,15,7.8)
    set_position(90)
    print_yaw("Mission 07: After S-Move")
    move_x_bot(15,True)

# Mission 08: Air Drop (20+10+10)
def mission_08():
    print_yaw("Mission 08: Air Drop")
    move_x_bot(-4,True)
    set_position(90)
    back_left_to_yaw(130,-20,20)
    set_position(134)
    left_motor.start()
    # Move the right Hand forward
    left_motor.run_for_degrees(55,60)
    left_motor.stop()
    print_yaw("Mission 08: Before slam")
    turn_left_to_yaw(45,50,18.8) #angle,speed,radius
    set_position(45)
    move_x_bot(5.4,True)
    turn_x_bot(30,30,12) 
    move_x_bot(2,True)

# Mission 09: Train Tracks (20+20)
def mission_09():
    print_yaw("Mission 09: Train Tracks")
    back_right_to_yaw(0,-20,9) #angle, speed, radius in inches
    move_x_bot(-11,True)
    tank_to_yaw_reverse(-80,20) #angle, speed
    move_x_bot(-5,True,20)
    set_position(-90)
    left_motor.start()
    left_motor.run_for_seconds(1,18)
    left_motor.stop()
    move_x_bot(6,True)

#Pushes The Train Across The Tracks
def push_train():
    print_yaw("Push Train")
    reset_yaw()
    print_yaw("Push Train: After Yaw Reset")
    move_cargo(290)
    turn_left_to_yaw(-60,10,4) #angle, speed radius
    turn_right_to_yaw(0,10,4)
    set_position(0)
    print_yaw("Push Train: before stepping back")
    move_x_bot(-4, True)
    motor_pair.set_default_speed(50)
    move_x_bot(30, True)
    motor_pair.set_default_speed(20)
    print_yaw("Push Train: after the run")
    move_cargo(-290)
    back_right_to_yaw(-45,-10,4)
    back_left_to_yaw(0,-10,4)
    set_position(0)
    print_yaw("Push Train: back up")
    move_x_bot(-15, True)
    turn_right_to_yaw(90,10,5)
    set_position(90)

#Maneuvers X-Bot Into The Position To Push The Train
def mission_09_2():
    print_yaw("Mission 09_2: Train Tracks 2")
    left_motor.run_for_degrees(-75,60)
    move_x_bot(-1,True,20)
    tank_to_yaw_reverse_check_negative(-178,18)
    print_yaw("Mission 09_2: Before reversing")
    motor_pair.set_default_speed(-40)
    motor_pair.start()
    wait_for_seconds(3)
    motor_pair.stop()
    motor_pair.set_default_speed(robot_speed)
    print_yaw("Mission 09_2: After reversing")
    push_train()

#Returns The X-Bot To The Home Area
def go_home():
    print_yaw("Go Home")
    accelerate(0, 80, 0.2)
    move_x_degrees(700)
    decelerate(80,0,0.5)
    turn_left_to_yaw(65,10,4)
    move_x_bot(72,True,100)

## ROUND 2
#Old Function
def mission_16():
    print_yaw("Mission 16: Cargo Connect")
    turn_left_to_yaw(-10,10,4.65) #angle, speed, radius in inches
    move_x_bot(21,True)
    turn_right_to_yaw(47,10,10) #angle, speed, radius in inches
    move_x_bot(13.5,True)
    move_x_bot(-35,True)
    back_right_to_yaw(3,-20,5)

def mission_16_new():
    print_yaw("Mission 16: Cargo Connect")
    move_x_bot(25,True,35)
    turn_right_to_yaw(40,10,10) #angle, speed, radius in inches
    move_x_bot(13.5,True)
    move_x_bot(-44,True,50)
    back_right_to_yaw(3,-20,5)

# Mission 01: Innovation Project Model (20)
def mission_01():
    print_yaw("Mission 01: Innovation Project Model")
    turn_right_to_yaw(86, 12, 4)
    set_position(90)
    move_x_bot(48, False, 35)
    turn_left_to_yaw(33, 12, 7)
    move_x_bot(-3.3, False, 30)
    back_left_to_yaw(88,-10,3)

# Mission 11: Home Delivery (20+10)
def mission_11():
    print_yaw("Mission 11: Home Delivery")
    turn_right_to_yaw(119,10,3)
    move_x_bot(15, True, 30)
    turn_left_to_yaw(110,10,3) #angle,speed,radius
    set_position(94)
    print_yaw("Mission 11: Before Delivery")
    move_x_bot(5,True)
    move_cargo(300, 100)
    move_cargo(-300,100)
    back_left_to_yaw(110,-8,2) #getting out
    move_x_bot(-13, True, 50)
    print_yaw("Mission 11: Backing out")
    back_right_to_yaw(95,-8,2)
    set_position(90)
    move_x_bot(-5, True, 50)

# Mission 10: Sorting Center (20)
def mission_10():
    print_yaw("Mission 10: Sorting Center")
    move_x_bot(-7, True, 50)
    turn_left_to_yaw(50,10,8)
    move_x_bot(30, True, 50)
    tank_to_yaw(129,30) #angle,speed
    reset_yaw()
    tank_to_yaw(35,30)
    print_yaw("Mission 10: After Tank Move")
    move_x_bot(-30, True, 50)
    reset_yaw()
    move_cargo(320)
    move_x_bot(42,True)

# Mission 06: Accident Avoidance (20+10)
def mission_06():
    print_yaw("Mission 06: Accident Avoidance")
    turn_left_to_yaw(50,10,5)
    move_x_bot(12, True, 50)
    turn_left_to_yaw(0,40,5)
    tank_to_yaw(-90,40)
    turn_left_to_yaw(-90,10,5)
    move_x_bot(12, True, 50)
    set_position(-90)
    turn_right_to_yaw(-25,10,5)
    move_x_bot(6, True, 40)
    turn_left_to_yaw(-90,10,5)
    set_position(-90)
    move_x_bot(2, True, 3)


def test_cargo():
    move_cargo(200) #platooning trucks
    wait_for_seconds(5)
    move_cargo(300) # Bay
    wait_for_seconds(5)
    move_cargo(-300) # Raise

###################### ROUND 1 ###########################
def round_zero():
    initialize_x_bot()
    reset_cargo()

def round_one():
    mission_05() # switch engine
    mission_03() # unload cargo plane
    mission_13() # platooning trucks
    mission_14() # bridge closing
    mission_07() # unload cargo ship
    mission_08() # air drop
    mission_09() # part 1 - completing track
    mission_09_2() # part 2 - moving cars
    go_home() 

###################### ROUND 2 ###########################
def round_two():
    reset_yaw()
    mission_16_new() # cargo connect
    move_cargo(-200)

###################### ROUND 3 ###########################
def round_three():
    timer.reset()
    reset_yaw()
    left_wheel.set_degrees_counted(0)
    right_wheel.set_degrees_counted(0)
    mission_01() # innovation project model
    mission_11() # home delivery
    mission_06() # accident avoidance - last one

def test_accel_decel():
    initialize_x_bot()
    yaw=get_yaw()
    print_yaw("start")
    print_right("start")
    accelerate(0,80,0.2)
    print_right("80 speed")
    move_x_degrees(700)
    print_right("about to slow down")
    decelerate(80,0,0.5)
    accelerate(0,-80,0.2)
    print_right("back")
    move_x_degrees(-700)
    decelerate(-80,0,0.5)
    print_right("stopped")
    print_yaw("end")
    if yaw == get_yaw():
        print("TEST PASS")
    else:
        print("TEST FAIL")

print("-------START-------")

#round_zero()
round_one()
#round_two()
#round_three()

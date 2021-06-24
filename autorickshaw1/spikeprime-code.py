from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math
from mindstorms import DistanceSensor

# Initialize the Distance Sensor.
distance = DistanceSensor('C')

from mindstorms import MotorPair

# If the left motor is connected to Port B,
# and the right motor is connected to Port A.
motor_pair = MotorPair('E', 'A')




# Create your objects here.
hub = MSHub()


# Write your program here.
hub.speaker.beep()

# motor_pair.move(100, 'cm', 0, 100)

motor_pair.start(0,20)

while True:
    d=distance.get_distance_cm()
    print(d)
    if d != None:
        d=int(d)
        if (d <= 10):
            print("obstacle")
            motor_pair.stop()
        else:
            print("all clear")
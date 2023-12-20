import sys
import pygame
import serial
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
# a script to control the create 3 robot with a Dualshock 4 controller

# set to create3 bluetooth name
create3_name = "chompions"

# initialize dependencies
robot = Create3(Bluetooth(name=create3_name))
pygame.init()
pygame.joystick.init()
ser = serial.Serial("COM7", 9600, timeout = 1)

# check for controller connection
if pygame.joystick.get_count() == 0:
    print("No controller found. Please connect a controller.")
    sys.exit(1)

controller = pygame.joystick.Joystick(0)
controller.init()

# write a data packet as serial
def sendData(packet):
    ser.write(packet)

# set l/r motor values based on controller trigger and axis values
def set_motor_values(controller):
    speed = 50

    # raw data
    left_joystick_x = controller.get_axis(0)
    left_trigger = controller.get_axis(4)
    right_trigger = controller.get_axis(5)

    # normalized from 0-1
    ltv = (left_trigger + 1) / 2
    rtv = (right_trigger + 1) / 2
    abs_trigger = rtv - ltv

    # sharp turning
    if abs_trigger == 0:
        if left_joystick_x > 0.01 :
            l_differential = abs(left_joystick_x)
            r_differential = - abs(left_joystick_x)
        elif left_joystick_x < -0.01:
            l_differential = - abs(left_joystick_x)
            r_differential = abs(left_joystick_x)
        else:
            l_differential = 0
            r_differential = 0
        left_motor = l_differential * speed * 0.5
        right_motor = r_differential * speed * 0.5
    # forward driving
    elif abs_trigger > 0:
        if left_joystick_x > 0.01 :
            l_differential = 0
            r_differential = abs(left_joystick_x)
        elif left_joystick_x < -0.01:
            l_differential = abs(left_joystick_x)
            r_differential = 0
        else:
            l_differential = 0
            r_differential = 0
        left_motor = -(abs_trigger - (r_differential/1.1)) * speed
        right_motor = -(abs_trigger - (l_differential/1.1)) * speed
    # backwards driving
    elif abs_trigger < 0:
        if left_joystick_x > 0.01 :
            l_differential = abs(left_joystick_x)
            r_differential = 0
        elif left_joystick_x < -0.01:
            l_differential = 0
            r_differential = abs(left_joystick_x)
        else:
            l_differential = 0
            r_differential = 0
        left_motor = -(abs_trigger + (l_differential/1.1)) * speed
        right_motor = -(abs_trigger + (r_differential/1.1)) * speed
    
    return left_motor, right_motor

# send data packets to arduino to control auxilary motors
def control_motors(controller):
    if controller.get_button(0) == 1:
        print("Starting spinner.")
        sendData(b'1')
    if controller.get_button(1) == 1:
        print("Stopping spinner.")
        sendData(b'2')
    if controller.get_button(2) == 1:
        print("Opening door.")
        sendData(b'3')
    if controller.get_button(3) == 1:
        print("Closing Door.")
        sendData(b'4')
    if controller.get_button(9) == 1:
        print("Decreasing Speed.")
        sendData(b'5')
    if controller.get_button(10) == 1:
        print("Increasing Speed.")
        sendData(b'6')

# main looping function
@event(robot.when_play)
async def play(robot):
    print('Ready for control.')

    pygame.event.pump()
    control_motors(controller)
    motor_values = set_motor_values(controller)

    await robot.set_wheel_speeds(motor_values[0], motor_values[1])

robot.play()
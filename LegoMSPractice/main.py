#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

def detect_black(colorsensor):
    """
    ラインから外れているのを検知した時
    """
    BLACK = 9
    WHITE = 60
    threshold = (BLACK + WHITE) / 2

    return colorsensor.reflection() < threshold

# EV3
ev3 = EV3Brick()

# Motor Settings
left = Motor(Port.B)
right = Motor(Port.C)
robot = DriveBase(left, right, 56, 114)

# Line Sensor Instance
line_sensor_L = ColorSensor(Port.S1)
line_sensor_C = ColorSensor(Port.S2)
line_sensor_R = ColorSensor(Port.S3)

# Speed Parametor
normal = 250
slow = 200
take_care = 120

# Rotate Parametor
degree = 80

# Exit Flag
final_flag = False

last_detected = line_sensor_C

# Main Sequence
robot.drive(normal, 0)
while True:
    # 直線補正
    if (detect_black(line_sensor_C)):
        robot.drive(normal, 0)

        if(detect_black(line_sensor_L)):
            last_detected = line_sensor_L

        if(detect_black(line_sensor_R)):
            last_detected = line_sensor_R
    
    # カーブ制御(右)
    if (detect_black(line_sensor_R)):
        robot.drive(slow, degree)
        wait(20)

        if (detect_black(line_sensor_R)):
            robot.drive(take_care, degree)
        
    # カーブ制御(左)
    if (detect_black(line_sensor_L)):
        robot.drive(slow, -degree)
        wait(20)

        if (detect_black(line_sensor_L)):
            robot.drive(take_care, -degree)

    # 全て黒色になった時
    if (detect_black(line_sensor_C) and detect_black(line_sensor_L) and detect_black(line_sensor_R)):
        # TODO もう少しなんとか条件を緩めないと、突然全部黒になった時に停止しちゃう

        while(True):
            robot.drive(slow, 0)
            wait(20)

            # 十字路
            if((not detect_black(line_sensor_L)) and detect_black(line_sensor_C) and (not detect_black(line_sensor_R))):
                break

            
            # 終了
            if((not detect_black(line_sensor_L)) and (not detect_black(line_sensor_C)) and (not detect_black(line_sensor_R))):
                final_flag = True
                break
    
    if((not detect_black(line_sensor_L)) and (not detect_black(line_sensor_C)) and (not detect_black(line_sensor_R))):
        if (last_detected == line_sensor_L):
            robot.drive(take_care, -(degree+20))

        if (last_detected == line_sensor_R):
            robot.drive(take_care, (degree+20))
        
        wait(20)

    if(final_flag):
        break

    wait(10)

robot.stop()

ev3.speaker.play_notes(['C4/4', 'C4/4', 'G4/4', 'G4/4'])

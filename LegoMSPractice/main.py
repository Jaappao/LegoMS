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
normal = 300
slow = 230
take_care = 120

# Rotate Parametor
degree = 80

# Exit Flag
final_flag = False

# 直角カーブで行きすぎて真っ白になった時に最後に黒を補足した側に曲がるためのインスタンスを格納
last_detected = line_sensor_C

# Main Sequence
BLACK = line_sensor_C.reflection()
WHITE = (line_sensor_L.reflection() + line_sensor_R.reflection()) / 2

robot.drive(normal, 0)

while True:
    # 直線補正
    if (detect_black(line_sensor_C)):
        robot.drive(normal, 0)

        # 直角カーブで行きすぎて真っ白になった時に最後に黒を補足した側に曲がるためのインスタンスを格納
        if(detect_black(line_sensor_L)):
            last_detected = line_sensor_L
        
        if(detect_black(line_sensor_R)):
            last_detected = line_sensor_R
    
    # カーブ制御(右)
    if (detect_black(line_sensor_R)):
        robot.drive(slow, degree)
        wait(10)

        if (detect_black(line_sensor_R)):
            robot.drive(take_care, degree)
        
    # カーブ制御(左)
    if (detect_black(line_sensor_L)):
        robot.drive(slow, -degree)
        wait(10)

        if (detect_black(line_sensor_L)):
            robot.drive(take_care, -degree)

    # 全て黒色になった時
    if (detect_black(line_sensor_C) and detect_black(line_sensor_L) and detect_black(line_sensor_R)):

        while(True):
            robot.drive(slow, 0)
            wait(25)

            # 十字路
            if((not detect_black(line_sensor_L)) and detect_black(line_sensor_C) and (not detect_black(line_sensor_R))):
                break

            
            # 終了
            if((not detect_black(line_sensor_L)) and (not detect_black(line_sensor_C)) and (not detect_black(line_sensor_R))):
                final_flag = True
                break
    
    # 直角カーブや緩いカーブで全て白になるまでオーバーシュートした時に、最後に黒を検知した方向に曲がる
    if((not detect_black(line_sensor_L)) and (not detect_black(line_sensor_C)) and (not detect_black(line_sensor_R))):
        if (last_detected == line_sensor_L):
            robot.drive(take_care, -(degree))

        if (last_detected == line_sensor_R):
            robot.drive(take_care, (degree))
        
        wait(10)

    if(final_flag):
        break

    wait(10)

robot.stop()

ev3.speaker.play_notes(['C4/4', 'C4/4', 'G4/4', 'G4/4'])

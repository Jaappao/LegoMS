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


left = Motor(Port.B)
right = Motor(Port.C)
robot = DriveBase(left, right, 56, 114)

line_sensor_L = ColorSensor(Port.S1)
line_sensor_C = ColorSensor(Port.S2)
line_sensor_R = ColorSensor(Port.S3)

robot.drive(100, 0)

while True:
    if (detect_white(line_sensor_C) and detect_white(line_sensor_L) and detect_white(line_sensor_R)):
        break

    print(line_sensor_C.reflection())


    wait(10)

robot.stop()
#!/usr/bin/env python

from grizzly import *
from xbox_read import event_stream
import numpy as np
import sys
import time

g = Grizzly()
g.set_mode(ControlMode.POSITION_PID, DriveMode.DRIVE_BRAKE)

#constants for RS555
g.limit_acceleration(100)
g.limit_current(15)


inputs = event_stream(4000)

target = 0
for event in inputs:
    if event.key == "Y2":
        target = target + int(event.value)/328
        target = np.clip(target,0,2500)
        #0 is minimum.  2600 is maximum
        print("Target: " + str(target))
    if event.key == "A":
        print("Current: " + str(g.read_motor_current()) + "Encoder: " + str(g.read_encoder()))
    if event.key == "B":
        print("Grizzly position PID to target = " + str(target))    
        ####g.set_target(target/2.0**16)
        ####fixed_set = int(setpoint * (2 ** 16))
        buf = [cast_to_byte(target >> 8 * i) for i in range(5)]
        print 'Buf=',buf
        g.set_register(Addr.Speed, buf)
    if event.key == "X":
        print("Setting PID constants, use keyboard")
        p = sys.stdin.readline()
        p = float(p)
        i = sys.stdin.readline()
        i = float(i)
        d = sys.stdin.readline()
        d = float(d)
        print("P " + str(p) + " I " + str(i) + " D " + str(d) )
        g.init_pid(p,i,d)
        time.sleep(1.0)


# Appendix: Keys
# --------------
# Key:                      Range of values:
# X1                        -32768 : 32767
# Y1                        -32768 : 32767
# X2                        -32768 : 32767
# Y2                        -32768 : 32767
# du                        0, 1
# dd                        0, 1
# dl                        0, 1
# dr                        0, 1
# back                      0, 1
# guide                     0, 1
# start                     0, 1
# TL                        0, 1
# TR                        0, 1
# A                         0, 1
# B                         0, 1
# X                         0, 1
# Y                         0, 1
# LB                        0, 1
# RB                        0, 1
# LT                        0 : 255
# RT                        0 : 255

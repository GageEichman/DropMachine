import gpiozero
from gpiozero import Button
import time

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

bump=Button(23)

        ### LOWER PRINT ONLY RETURNS PRINT STATEMENTS SO YOU CAN CHECK IF THE SWITCH IS WIRED CORRECT ###
        ### LOWER_MOTOR IS HOW THE MOTOR LOWERS IN THE ACTUAL PROGRAM ###
        ### DELETE THE APOSTROPHESE ON 47 AND 52 TO RUN LOWER MOTOR         ###


def lower_print():
    while True:
        if bump.is_pressed:
            print('stopping')
            time.sleep(1)
            print('reversing slightly')
            time.sleep(1)
            print('stopping')
            break
        else:
            print('lowering')
            time.sleep(1)
            
def lower_motor():  # LOWER
        global bump
        print('lowering to home')
        while True:
            if bump.is_pressed:
                print('stopping')
                time.sleep(1)
                print('reversing slightly')
                for i in range(10):
                    kit1.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
                time.sleep(1)
                print('stopping')
                kit1.stepper1.release()
                break
            else:
                kit1.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        
    
lower_print()
'''
kit = MotorKit()
kit1= MotorKit(address=0x61)

lower_motor()
'''
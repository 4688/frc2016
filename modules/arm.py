#!/usr/bin/python3

import modules.joystick as j

import wpilib as wpi

# CONSTANTS
#===============================================================================

ARM_MOTOR_INDEX = 5

ARM_LIMIT_INDEX = 0

# CALCULATIONS
#===============================================================================

armState = ""
prevArmSpd = 0.0

def getArmSpeed(joystick: wpi.Joystick, limit: wpi.DigitalInput):
    """
        Calculates and returns the speed of the arm.
    """

    global armState, prevArmSpd

    xBtn = joystick.getRawButton(j.RETRACT_BTN_INDEX)
    yBtn = joystick.getRawButton(j.EXTEND_BTN_INDEX)

    if not xBtn and not yBtn:
        return 0.0

    armActive = (xBtn and not yBtn) or (yBtn and not xBtn)

    if xBtn and not yBtn:
        armState = "e"
    elif yBtn and not xBtn:
        armState = "r"
    else:
        armState = armState

    speedMult = 1 if armState == "e" else -1
    limitMult = -1 # if limit.get() else 1

    oldArmSpd = prevArmSpd
    speed = 0.75 * speedMult * limitMult # TODO change this to a real value
    prevArmSpd = speed if speed != prevArmSpd else prevArmSpd

    return speed

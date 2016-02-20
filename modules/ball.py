#!/usr/bin/python3

import modules.joystick as j

import wpilib as wpi

# CONSTANTS
#===============================================================================

# PWM port index of the intake motor controller.
# Default: 1
INTAKE_INDEX = 1

# PWN port index of the ball release lever.
# Default: 2
LEVER_INDEX = 2

# Divisor by which the speed of the intake motors is divided relative to input.
# Set this to a higher value if not using a low-torque motor!
# Default: 1
INTAKE_SPD_DIVISOR = 1

# Number of frames to wait for the lever to lift while the eject motors are
# speeding up.
# Default: 150 (3 seconds)
LEVER_WAIT_TIME = 150

# INTAKE & OUTPUT
#===============================================================================

ejectActive = False
ejectTimer = 0
ejectFinishing = False

def getIntakeSpeed(joystick):
    """
        Calculates and returns the speed of the intake motors, relative to
        input.
    """

    if ejectActive: return -1
    return ((joystick.getRawAxis(j.INTAKE_AXIS_INDEX) + 1) / INTAKE_SPD_DIVISOR)

def startEject():
    ejectTimer = 0 if not ejectActive
    ejectActive = True
    ejectFinishing = False

def tickEjectTimer():
    """
        Document this later.
    """

    if ejectActive: ejectTimer += 1

    if ejectTimer >= LEVER_WAIT_TIME and topLimit.get():
        ejectFinishing = True

    if ejectFinishing and bottomLimit.get():
        ejectFinishing = False
        ejectTimer = 0
        ejectActive = False

def getEjectLeverSpeed(upLimit, downLimit):
    """
        Returns the speed at which the lever should move to allow ball ejection.
    """

    if ejectActive:

        if not ejectFinishing:

            if ejectTimer >= LEVER_WAIT_TIME and not topLimit.get():

                return 0.1

            else:

                return 0.0

        elif ejectFinishing:

            return -0.1

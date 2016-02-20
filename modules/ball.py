#!/usr/bin/python3

import modules.joystick as j

import wpilib as wpi

# CONSTANTS
#===============================================================================

# PWM port index of the intake motor controller.
# Default: 1
INTAKE_INDEX = 1

# PWM port index of the ball release lever.
# Default: 2
LEVER_INDEX = 2

# PWM port indices of the release lever's limit switches.
# Indices are for up & down limits respectively.
# Default: 1, 2
LEVER_LIMIT_INDICES = (1, 2)

# Divisor by which the speed of the intake motors is divided relative to input.
# Set this to a higher value if not using a low-torque motor!
# Default: 1
INTAKE_SPD_DIVISOR = 1

# Number of frames to wait for the lever to lift while the eject motors are
# speeding up.
# Default: 150 (3 seconds)
LEVER_WAIT_TIME = 150

LEVER_FINISH_TIME = 100

# INTAKE & OUTPUT
#===============================================================================

ejectActive = False
ejectTimer = 0
leverTimer = 0
ejectFinishing = False

def getIntakeSpeed(joystick):
    """
        Calculates and returns the speed of the intake motors, relative to
        input.
    """

    if ejectActive: return -1
    return ((joystick.getRawAxis(j.INTAKE_AXIS_INDEX) + 1) / INTAKE_SPD_DIVISOR)

def startEject():
    if not ejectActive:
        ejectTimer = 0
        ejectActive = True
        ejectFinishing = False

def tickEjectTimer(limit):
    """
        Document this later.
    """

    global ejectActive, ejectTimer, ejectFinishing, leverTimer

    if ejectActive:
        ejectTimer += 1
        leverTimer += 1

    if ejectTimer >= LEVER_WAIT_TIME and leverTime >= LEVER_FINISH_TIME:
        ejectFinishing = True

    if ejectFinishing and limit.get():
        ejectFinishing = False
        ejectTimer = 0
        leverTimer = 0
        ejectActive = False

def getEjectLeverSpeed():
    """
        Returns the speed at which the lever should move to allow ball ejection.
    """

    if ejectActive:

        if not ejectFinishing:

            if ejectTimer >= LEVER_WAIT_TIME and leverTime < LEVER_FINISH_TIME:

                return 0.1

            else:

                return 0.0

        elif ejectFinishing:

            return -0.1

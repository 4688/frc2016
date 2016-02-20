#!/usr/bin/python3

import modules.joystick as j

import wpilib as wpi

# CONSTANTS
#===============================================================================

# PWM port index of the intake motor controller.
# Default: 1
INTAKE_INDEX = 1

# Divisor by which the speed of the intake motors is divided relative to input.
# Set this to a higher value if not using a low-torque motor!
# Default: 1
INTAKE_SPD_DIVISOR = 1

# CALCULATIONS
#===============================================================================

def getIntakeSpeed(joystick):
    """
        Calculates and returns the speed of the intake motors, relative to
        input.
    """

    reverse = 1 if joystick.getRawButton(j.EJECT_BTN_INDEX) else -1
    return (joystick.getRawAxis(j.INTAKE_AXIS_INDEX) + 1) * reverse / \
        INTAKE_SPD_DIVISOR

#!/usr/bin/python3

import modules.joystick as j

import wpilib as wpi

# CONSTANTS
#===============================================================================

# PWM port index of the left intake motor.
# Default: 1
L_INTAKE_INDEX = 1

# PWM port index of the right intake motor.
# Default: 2
R_INTAKE_INDEX = 2

# Divisor by which the speed of the intake motors is divided relative to input.
# Set this to a higher value if not using a low-torque motor!
# Default: 1
INTAKE_SPD_DIVISOR = 1

# CALCULATIONS
#===============================================================================

def getIntakeSpeed(joystick: wpi.Joystick):
    """
        Calculates and returns the speed of the intake motors, relative to
        input.
    """

    reverse = 1 if joystick.getRawButton(j.EJECT_BTN_INDEX) else -1
    return (joystick.getRawAxis(j.INTAKE_AXIS_INDEX) + 1) * reverse / \
        INTAKE_SPD_DIVISOR

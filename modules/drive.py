#!/usr/bin/python3

import modules.joystick as j

import wpilib as wpi

# CONSTANTS
#===============================================================================

# MOTORS
#-------------------------------------------------------------------------------

# CAN Bus indices for left drive motors, front motor first.
# Default: 1, 3
L_CAN_INDICES = (1, 3)

# CAN Bus indices for the right drive motors, front motor first.
# Default: 2, 4
R_CAN_INDICES = (2, 4)

# Deadband percent of the drive motors.
# Default: 0.04 (4%)
DRIVE_DEADBAND = 0.04

# DRIVING
#-------------------------------------------------------------------------------

# Divisor by which forward/backward & stationary pivot speed is divided.
# Default: 2.5
DRIVE_SPD_DIVISOR = 2.5

# Allow the driver to enable turbo mode?
# Make sure this is True on competition builds!
# Default: True
ALLOW_TURBO = True

# Factor by which the speed of the motors is multiplied while in turbo mode.
# Obviously, the actual speed is capped at 100%.
# Default: 2
TURBO_FACTOR = 2

# CALCULATIONS
#===============================================================================

def getDriveLeft(joystick):
    """
        Calculates and returns the speed of the left drive motors, relative to
        input.
    """

    # Joystick axes
    yAxis = joystick.getRawAxis(j.Y_AXIS_INDEX)
    xAxis = joystick.getRawAxis(j.X_AXIS_INDEX)

    # Turbo factor
    turbo = TURBO_FACTOR if joystick.getRawButton(j.TURBO_BTN_INDEX) else 1

    # Speed calculation
    forward = -yAxis / DRIVE_SPD_DIVISOR * turbo
    speed = forward

    if forward <= DRIVE_DEADBAND and abs(xAxis) > DRIVE_DEADBAND:
        # Pivot whilst stationary

        speed = xAxis / DRIVE_SPD_DIVISOR

    elif forward > DRIVE_DEADBAND or forward < -DRIVE_DEADBAND:
        # Turn whilst driving
        turnFactor = abs(xAxis) + 1

        if xAxis > DRIVE_DEADBAND:
            # X-axis is positive (turn to the right)
            speed *= turnFactor
        elif xAxis < -DRIVE_DEADBAND:
            # X-axis is negative (turn to the left)
            speed /= turnFactor

    return speed

def getDriveRight(joystick):
    """
        Calculates and returns the speed of the right drive motors, relative to
        input.
    """

    # Joystick axes
    yAxis = joystick.getRawAxis(j.Y_AXIS_INDEX)
    xAxis = joystick.getRawAxis(j.X_AXIS_INDEX)

    # Turbo factor
    turbo = TURBO_FACTOR if joystick.getRawButton(j.TURBO_BTN_INDEX) else 1

    # Speed calculation
    forward = -yAxis / DRIVE_SPD_DIVISOR * turbo
    speed = -forward

    if forward <= DRIVE_DEADBAND and abs(xAxis) > DRIVE_DEADBAND:
        # Pivot whilst stationary

        speed = xAxis / DRIVE_SPD_DIVISOR

    elif forward > DRIVE_DEADBAND or forward < -DRIVE_DEADBAND:
        # Turn whilst driving
        turnFactor = abs(xAxis) + 1

        if xAxis > DRIVE_DEADBAND:
            # X-axis is positive (turn to the right)
            speed /= turnFactor
        elif xAxis < -DRIVE_DEADBAND:
            # X-axis is negative (turn to the left)
            speed *= turnFactor

    return speed

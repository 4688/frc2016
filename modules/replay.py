#!/usr/bin/python3

import modules.joystick as j

import wpilib as wpi

# CONSTANTS
#===============================================================================

# Allow recording of input routines from user through joystick combo?
# Make sure this is False on competition builds!
# Default: True
ALLOW_MANUAL_RECORD = True

# Allow manual playback of input routines from user through joystick input?
# Make sure this is False on competition builds!
# Default: True
ALLOW_MANUAL_PLAYBACK = True


# ROUTINE MANAGEMENT
#===============================================================================

recording = False
playing = False

routines = [None, None, None, None]

def formatInputStateStr(joystick):
    """
        Generates a line of data for the routine file based on the state of the
        joystick.
    """

    axisValues = []
    btnStates = []

    # Store states of input
    for axisNum in range(joystick.getAxisCount()):
        axisValues.append(joystick.getRawAxis(axisNum))
    for btnNum in range(joystick.getButtonCount()):
        btnStates.append(joystick.getRawButton(btnNum))

    # Create segments
    btnStateStr = "".join([int(x) for x in btnStates])
    print(btnStateStr)

def logState(joystick):
    """
        If the robot is recording, log the joystick input this frame to the
        routine. If it isn't, do nothing.
    """

    if not recording:

        return

    else:

        pass

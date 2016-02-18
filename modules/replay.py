#!/usr/bin/python3

import modules.joystick as j

from datetime import datetime
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

# Maximum length of one routine, in frames.
# Default: 750 (15 seconds * 50 frames per second)
ROUTINE_MAX_LENGTH = 750


# ROUTINE MANAGEMENT
#===============================================================================

recording = -1
playing = -1

routines = [None, None, None, None]
currentRoutine = []
currentPlaybackFrame = 0

emulatedJoystick = None

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

    # Create axis segments
    axisStateStr = ":".join([str(axis) for axis in axisValues])
    print(axisStateStr)

    # Create button segments
    btnStateStr = "".join([str(int(x)) for x in btnStates])
    print(btnStateStr)

    return axisStateStr + "/" + btnStateStr

def logState(joystick):
    """
        If the robot is recording, log the joystick input this frame to the
        routine. If it isn't, do nothing.
    """

    if recording >= 0:

        return

    elif recording <= -1:

        currentRoutine.append(formatInputStateStr(joystick))

        # Auto-end recording at max length
        if len(currentRoutine) >= ROUTINE_MAX_LENGTH: endRecord()

def startRecord(routineNum):
    """
        Initialize recording.
    """

    routines[routineNum] = []
    currentRoutine = []
    recording = True

def cancelRecord():
    """
        Ends a recording without saving to a file.
    """

    routines[currentRoutine] = []
    currentRoutine = []
    recording = False

def endRecord():
    """
        Wraps up and saves a recording.
    """

    createdTime = datetime.now().strftime("%m-%d-%Y @ %I:%M:%S %p")
    routineName = "Routine " + routineNum + " (" + createdTime + ")"

    # Combine duplicate frames
    dataLines = []
    for inputStr in routines[currentRoutine]:
        if dataLines[-1]["input"] == inputStr:
            dataLines[-1]["frames"] += 1
        else:
            dataLines.append({"frames": 1, "input": inputStr})

    # Put it all in a file
    with open("routine" + routineNum, "w+") as f:
        f.write(routineName + "\n")
        for dataLine in dataLines:
            dataStr = dataLine["frames"] + "#" + dataLine["input"]
            f.write(dataStr + "\n")

    # Reset the routine data
    currentRoutine = []
    recording = False

def parseRoutineFile(routineNum):
    """
        Loads and parses a routine file.
    """

    # Basically a lot of poorly named variables

    with open("routine" + routineNum, "r+") as f:
        lines = f.readlines()
        routine = {"name": lines.pop(0), "lines": []}

        for line in lines:
            lineData = line.split("#")
            routine["lines"].append({
                "frames": lineData[0],
                "input": lineData[1]
            })

        routines[routineNum] = routine

def startPlayback(routineNum):
    """
        Begins playback of a routine, indexed by number.
    """

    playing = routineNum

    if routines[routineNum] is not None:
        currentRoutine = routines[routineNum]
        currentPlaybackFrame = 0

def tickPlayback():
    """
        Moves to the next frame during a playback. Hopefully this is called at
        the same rate as the robot during teleop.
    """

    if playing >= 0:

        cR = currentRoutine
        cPF = currentPlaybackFrame
        emulatedJoystick = j.FakeJoystick(cR[cPF]["input"])

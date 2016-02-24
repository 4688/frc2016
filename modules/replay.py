#!/usr/bin/python3

import modules.joystick as j

currentRoutine = None
currentFrame = 0
frameTimer = 0

def playRoutine(routineNum):
    global currentRoutine
    try:
        with open("media/sda1/routine" + str(routineNum), "r+") as rfile:
            currentRoutine = rfile.readlines()
            routineName = currentRoutine.pop(0).rstrip("\r\n")
    except FileNotFoundError:
        pass

def isPlaying():
    global currentRoutine
    return currentRoutine is not None

def stopPlaying():
    global currentRoutine, currentFrame
    currentRoutine = None
    currentFrame = 0
    frameTimer = 0
    print("stopped record")

def nextFrame():
    global currentRoutine, currentFrame, frameTimer
    frameTimer += 1
    currentFrame += 1
    if currentFrame >= len(currentRoutine): # we've passed the time limit!! o no
        stopPlaying()
        return

def tickPlayback():
    global currentRoutine, currentFrame, frameTimer
    print(currentRoutine, currentFrame, frameTimer)
    if frameTimer <= 0:
        nextFrame()
    elif frameTimer > 0:
        frameTimer -= 1
    return j.FakeJoystick(currentRoutine[currentFrame].split("#")[1].rstrip("\r\n"))

#!/usr/bin/python3

import wpilib as wpi

# CONSTANTS
#===============================================================================

CAMERA_NAME = "cam0"

# CAMERA STREAMING
#===============================================================================

camera = None
camServer = None

def startCamera():
    """
        Initialize the camera and begin the stream.
    """

    camera = wpi.USBCamera(name=CAMERA_NAME.encode())
    camServer = wpi.CameraServer()
    camServer.startAutomaticCapture(camera)

#!/usr/bin/env python3

import wpilib as wpi

class SweetAssRobot(wpi.IterativeRobot):

    def robotInit(self):
        print("  > Robot initialized.")

    def autonomousInit(self):
        print("  > Entered AUTO mode.")

    def teleopInit(self):
        print("  > Entered MANUAL mode.")

    def teleopPeriodic(self):
        pass

    def testPeriodic(self):
        wpi.LiveWindow.run()

if __name__ == "__main__":
    wpi.run(SweetAssRobot)

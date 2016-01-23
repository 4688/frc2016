#!/usr/bin/env python3

from robot_constants import *
import wpilib as wpi

class SweetAssRobot(wpi.IterativeRobot):

    def robotInit(self):
        self.lMotor = wpi.VictorSP(L_MOTOR_INDEX)
        self.lMotor.set(0.0)

        self.rMotor = wpi.VictorSP(R_MOTOR_INDEX)
        self.rMotor.set(0.0)

        self.controls = wpi.Joystick(JOYSTICK_INDEX)

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

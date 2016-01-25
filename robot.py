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
        yAxis = -self.controls.getRawAxis(FORWARD_AXIS_INDEX)
        xAxis = self.controls.getRawAxis(TURN_AXIS_INDEX)

        isTurbo = self.controls.getRawButton(TURBO_BUTTON_INDEX) and ALLOW_TURBO
        turboMultiplier = TURBO_MULT if isTurbo else 1

        forward = yAxis / FORWARD_DIVISOR * turboMultiplier
        leftSpeed = forward
        rightSpeed = -forward

        if forward <= MOTOR_DEADBAND: # or forward >= -MOTOR_DEADBAND:
            speed = xAxis / PIVOT_DIVISOR
            leftSpeed = speed
            rightSpeed = speed
        elif forward > MOTOR_DEADBAND: # or forward < -MOTOR_DEADBAND:
            multVal = forward * (abs(xAxis) + 1)
            divVal = forward / (abs(xAxis) + 1)
            if xAxis > MOTOR_DEADBAND:
                leftSpeed = multVal
                rightSpeed = -divVal
            elif xAxis < -MOTOR_DEADBAND:
                leftSpeed = divVal
                rightSpeed = -multVal

        print("  >", leftSpeed, rightSpeed)

        self.lMotor.set(leftSpeed)
        self.rMotor.set(rightSpeed)

    def testPeriodic(self):
        wpi.LiveWindow.run()

if __name__ == "__main__":
    wpi.run(SweetAssRobot)

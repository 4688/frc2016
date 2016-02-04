#!/usr/bin/env python3

from robot_constants import *
import wpilib as wpi

class SweetAssRobot(wpi.IterativeRobot):

    def robotInit(self):
        self.lMotor0 = wpi.CANTalon(L_MOTOR_INDICES[0])
        self.lMotor0.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.lMotor0.set(0.0)

        self.rMotor0 = wpi.CANTalon(R_MOTOR_INDICES[0])
        self.rMotor0.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.rMotor0.set(0.0)

        self.controls = wpi.Joystick(JOYSTICK_INDEX)

    def autonomousInit(self):
        print("  > Entered AUTO mode.")

    def teleopInit(self):
        print("  > Entered MANUAL mode.")

    def teleopPeriodic(self):
        yAxis = self.controls.getRawAxis(FORWARD_AXIS_INDEX)
        xAxis = self.controls.getRawAxis(TURN_AXIS_INDEX)

        isTurbo = self.controls.getRawButton(TURBO_BUTTON_INDEX) and ALLOW_TURBO
        turboMultiplier = TURBO_MULT if isTurbo else 1

        forward = -yAxis / FORWARD_DIVISOR * turboMultiplier
        leftSpeed = forward
        rightSpeed = -forward

        if forward <= MOTOR_DEADBAND and abs(xAxis) > MOTOR_DEADBAND:
            # Theoretical pivot routine
            turnSpeed = xAxis / PIVOT_DIVISOR
            leftSpeed = turnSpeed
            rightSpeed = turnSpeed
        elif forward > MOTOR_DEADBAND or forward < -MOTOR_DEADBAND:
            poorlyNamedVariable = (abs(xAxis) + 1)
            if xAxis > MOTOR_DEADBAND:
                leftSpeed *= poorlyNamedVariable
                rightSpeed /= poorlyNamedVariable
            elif xAxis < -MOTOR_DEADBAND:
                leftSpeed /= poorlyNamedVariable
                rightSpeed *= poorlyNamedVariable

        self.lMotor0.set(leftSpeed)
        self.rMotor0.set(rightSpeed)

    def testPeriodic(self):
        wpi.LiveWindow.run()

if __name__ == "__main__":
    wpi.run(SweetAssRobot)

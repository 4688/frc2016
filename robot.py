#!/usr/bin/env python3

from threading import Thread

import wpilib as wpi

from robot_constants import *
import sards.server as sards

class SweetAssRobot(wpi.IterativeRobot):

    def robotInit(self):
        """
            Called once when the robot starts up. This is where we initialize
            robot components accessible through WPIlib.
        """

        self.controls = wpi.Joystick(JOYSTICK_INDEX)

        # Movement motors

        self.lMotor0 = wpi.CANTalon(L_MOTOR_INDICES[0])
        self.lMotor0.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.lMotor0.set(0.0)

        self.lMotor1 = wpi.CANTalon(L_MOTOR_INDICES[1])
        self.lMotor1.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.lMotor1.set(0.0)

        self.rMotor0 = wpi.CANTalon(R_MOTOR_INDICES[0])
        self.rMotor0.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.rMotor0.set(0.0)

        self.rMotor1 = wpi.CANTalon(R_MOTOR_INDICES[1])
        self.rMotor1.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.rMotor1.set(0.0)

        # Ball intake motors

        self.lIntakeMotor = wpi.VictorSP(L_INTAKE_MOTOR_INDEX)
        self.lIntakeMotor.set(0.0)

        self.rIntakeMotor = wpi.VictorSP(R_INTAKE_MOTOR_INDEX)
        self.rIntakeMotor.set(0.0)

        # Thread(target=sards.beginSend)

        self.camera = wpi.USBCamera(name="cam0".encode())
        self.camera.startCapture()
        self.camServer = wpi.CameraServer()
        self.camServer.startAutomaticCapture(self.camera)

    def autonomousInit(self):
        """
            Called once every time autonomous mode is entered.
        """

        print("  > Entered AUTO mode.")

    def teleopInit(self):
        """
            Called once every time teleop (manual) mode is entered.
        """

        print("  > Entered MANUAL mode.")

    def teleopPeriodic(self):
        """
            Called 50 times per second while the robot is in teleop (manual)
            mode. This is essentially one "frame" of the robot code; that is,
            this is when we interpret input, process built-in logic, and
            send component commands, in that order.
        """

        # Control stick axes
        yAxis = self.controls.getRawAxis(FORWARD_AXIS_INDEX)
        xAxis = self.controls.getRawAxis(TURN_AXIS_INDEX)

        # Turbo stuff
        isTurbo = self.controls.getRawButton(TURBO_BUTTON_INDEX) and ALLOW_TURBO
        turboMultiplier = TURBO_MULT if isTurbo else 1

        # Amount to move forward
        forward = -yAxis / FORWARD_DIVISOR * turboMultiplier
        leftSpeed = forward
        rightSpeed = -forward

        if forward <= MOTOR_DEADBAND and abs(xAxis) > MOTOR_DEADBAND:
            # Pivot whilst stationary

            turnSpeed = xAxis / PIVOT_DIVISOR
            leftSpeed = turnSpeed
            rightSpeed = turnSpeed

        elif forward > MOTOR_DEADBAND or forward < -MOTOR_DEADBAND:
            # Turning whilst driving

            turnFactor = (abs(xAxis) + 1)

            if xAxis > MOTOR_DEADBAND:
                # X axis is positive (to the right)

                leftSpeed *= turnFactor
                rightSpeed /= turnFactor

            elif xAxis < -MOTOR_DEADBAND:
                # X axis if negative (to the left)

                leftSpeed /= turnFactor
                rightSpeed *= turnFactor

        ballOutputMultiplier = -1 if self.controls.getRawButton(1) else 1
        intakeSpeed = (self.controls.getRawAxis(BALL_INTAKE_AXIS_INDEX) + 1) / \
            INTAKE_SPEED_DIVISOR * ballOutputMultiplier

        self.lMotor0.set(leftSpeed)
        self.lMotor1.set(leftSpeed)
        self.rMotor0.set(rightSpeed)
        self.rMotor1.set(rightSpeed)

        self.lIntakeMotor.set(-intakeSpeed)
        self.rIntakeMotor.set(intakeSpeed)

    def testPeriodic(self):
        """
            Called 50 times per second while the robot is in test mode.
        """

        wpi.LiveWindow.run()

if __name__ == "__main__":
    wpi.run(SweetAssRobot)

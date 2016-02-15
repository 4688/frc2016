#!/usr/bin/env python3

import wpilib as wpi

from robot_constants import *

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

        # self.rIntakeMotor = wpi.VictorSP(R_INTAKE_MOTOR_INDEX)
        # self.rIntakeMotor.set(0.0)

        # Actuator and switch

        self.armMotor = wpi.VictorSP(2) # TODO move index to constant

        # If at limits -> True, if in between -> False
        # Only move actuator when this is False!
        self.armSwitch = wpi.DigitalInput(0) # TODO move index to constant

        # Camera

        self.camera = wpi.USBCamera(name="cam0".encode()) # TODO move name to constant
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

        # Ball intake

        ballOutputMultiplier = 1 if self.controls.getRawButton(1) else -1
        intakeSpeed = (self.controls.getRawAxis(BALL_INTAKE_AXIS_INDEX) + 1) / \
            INTAKE_SPEED_DIVISOR * ballOutputMultiplier

        # Arm movement

        """
        If X button (index 3) down & not Y button (index 4) down: // extend
            Set STATE to "e"
            Set ACTIVE to True
        If Y button (index 4) down & not X button (index 3) down: // retract
            Set STATE to "r"
            Set ACTIVE to True
        If neither button down:
            Set ACTIVE to False
        If ACTIVE:
            If STATE is "e" & not switch:
                Set so that arm extends
            O/W if STATE is "e" & switch:
                Set so that arm retracts a lil bit
            O/W if STATE is "r" & not switch:
                Set so that arm retracts
            O/W if STATE is "r" & switch:
                Set so that arm extends a lil bit
        """

        xBtn = self.controls.getRawButton(3)
        yBtn = self.controls.getRawButton(4)

        armActive = (xBtn and not yBtn) or (yBtn and not xBtn)
        state = ("e" if xBtn else "r") if xBtn != yBtn else state

        armSpeedMult = 1 if state == "e" else -1
        armLimitMult = -1 if self.armSwitch.get() else 1

        self.preservedArmSpeed = 0.1 * armSpeedMult * armLimitMult
        finalArmSpeed = self.preservedArmSpeed

        self.lMotor0.set(leftSpeed)
        self.lMotor1.set(leftSpeed)
        self.rMotor0.set(rightSpeed)
        self.rMotor1.set(rightSpeed)

        self.lIntakeMotor.set(-intakeSpeed)
        self.rIntakeMotor.set(intakeSpeed)

        if finalArmSpeed != self.preservedArmSpeed:
            self.armMotor.set(finalArmSpeed)

        # print(str(self.armSwitch.get()))

    def testPeriodic(self):
        """
            Called 50 times per second while the robot is in test mode.
        """

        wpi.LiveWindow.run()

if __name__ == "__main__":
    wpi.run(SweetAssRobot)

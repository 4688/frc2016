#!/usr/bin/python3

import os

import wpilib as wpi

from robot_modules.arm import ArmManager
from robot_modules.ball import BallManager
from robot_modules.drive import DriveManager
from robot_modules.joystick import JoystickManager

class LoRida(wpi.IterativeRobot):
    """
    TODO: COOL CATCHPHRASE HERE
    """

    def robotInit(self) -> None:
        """
        Called once each time the robot starts up.
        This is where all of the robot's components are initialized.
        """

        # Joystick
        self.joystick = wpi.Joystick(JoystickManager.JOYSTICK_INDEX)

        # Left front drive motor
        self.lMotor0 = wpi.CANTalon(DriveManager.L_CAN_INDICES[0])
        self.lMotor0.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.lMotor0.set(0.0)

        # Left rear drive motor
        self.lMotor1 = wpi.CANTalon(DriveManager.L_CAN_INDICES[1])
        self.lMotor1.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.lMotor1.set(0.0)

        # Right front drive motor
        self.rMotor0 = wpi.CANTalon(DriveManager.R_CAN_INDICES[0])
        self.rMotor0.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.rMotor0.set(0.0)

        # Right rear drive motor
        self.rMotor1 = wpi.CANTalon(DriveManager.R_CAN_INDICES[1])
        self.rMotor1.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.rMotor1.set(0.0)

        # Ball intake/ejection motors
        self.ballMotor = wpi.VictorSP(BallManager.BALL_MOTOR_INDEX)
        self.ballMotor.set(0.0)

        # Eject actuator motor
        self.ejectLever = wpi.VictorSP(BallManager.RELEASE_LEVER_INDEX)
        self.ejectLever.set(0.0)

        # Eject actuator limit switch
        self.leverLimit = wpi.DigitalInput(BallManager.LEVER_LIMIT_INDEX)

        # Boom actuator motor
        self.armMotor = wpi.CANTalon(ArmManager.BOOM_MOTOR_INDEX)
        self.armMotor.set(0.0)

        # Boom actuator limit switches
        self.armLowerLimit = wpi.DigitalInput(ArmManager.BOOM_LOWER_LIMIT_INDEX)
        self.armUpperLimit = wpi.DigitalInput(ArmManager.BOOM_UPPER_LIMIT_INDEX)

        # Autonomous routine control switches
        self.as1 = wpi.DigitalInput(8)
        self.as2 = wpi.DigitalInput(9)

    def autonomousInit(self) -> None:
        """
        Called once each time autonomous mode begins.
        """

        self.routineNum = int(self.as1.get() << 1) + int(self.as2.get())
        self.autoTimer = 0

    def autonomousPeriodic(self) -> None:
        """
        Called 50 times per second while auto mode is active.
        """

        if self.routineNum == 3: # Low bar
            if self.autoTimer < 200 and not self.armLowerLimit.get():
                self.armMotor.set(0.8)
            elif self.autoTimer < 200 and self.armLowerLimit.get():
                self.armMotor.set(0.0)
            elif 400 > self.autoTimer > 250:
                self.lMotor0.set(0.4)
                self.lMotor1.set(0.4)
                self.rMotor0.set(-0.4)
                self.rMotor1.set(-0.4)
            elif self.autoTimer > 400:
                self.lMotor0.set(0.0)
                self.lMotor1.set(0.0)
                self.rMotor0.set(0.0)
                self.rMotor1.set(0.0)
            print(self.autoTimer)
            self.autoTimer += 1

        if self.routineNum == 1 or self.routineNum == 2: # Port cullis
            if self.autoTimer < 200 and not self.armLowerLimit.get():
                self.armMotor.set(0.8)
            elif self.autoTimer < 200 and self.armLowerLimit.get():
                self.armMotor.set(0.0)
            elif 400 > self.autoTimer > 250:
                self.lMotor0.set(-0.4)
                self.lMotor1.set(-0.4)
                self.rMotor0.set(0.4)
                self.rMotor1.set(0.4)
            elif self.autoTimer > 400:
                self.lMotor0.set(0.0)
                self.lMotor1.set(0.0)
                self.rMotor0.set(0.0)
                self.rMotor1.set(0.0)
            print(self.autoTimer)
            self.autoTimer += 1

    def teleopInit(self) -> None:
        """
        Called once each time manual (teleop) mode begins.
        """

        pass

    def teleopPeriodic(self) -> None:
        """
        Called 50 times per second while manual mode is active.
        """

        joystickToUse = self.joystick
        self._tickDrive(joystickToUse=self.joystick)

    def testPeriodic(self) -> None:
        """
        Called 50 times per second while test mode is active.
        """

        wpi.LiveWindow.run()

    def _tickDrive(self, joystickToUse):
        """
        Sets motor speeds and the like.
        Callable from both teleop and autonomous modes.
        """

        lDriveSpd = DriveManager.getDriveLeft(joystick=joystickToUse)
        self.lMotor0.set(lDriveSpd)
        self.lMotor1.set(lDriveSpd)

        rDriveSpd = DriveManager.getDriveRight(joystick=joystickToUse)
        self.rMotor0.set(rDriveSpd)
        self.rMotor1.set(rDriveSpd)

        ballMotorSpd = BallManager.getIntakeSpeed(joystick=joystickToUse)
        self.ballMotor.set(ballMotorSpd)

        leverSpd = BallManager.getEjectLeverSpeed(joystick=joystickToUse,
                                                  limit=self.leverLimit)
        self.ejectLever.set(leverSpd)

        armSpd = ArmManager.getArmSpeed(joystick=joystickToUse,
                                        upLimit=self.armUpperLimit,
                                        downLimit=self.armLowerLimit)
        self.armMotor.set(armSpd)

if __name__ == "__main__":
    wpi.run(LoRida)
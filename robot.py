#!/usr/bin/python3

import modules.arm as a
import modules.ball as b
import modules.drive as d
import modules.joystick as j
import modules.replay as r
import modules.station as s

import wpilib as wpi

class SweetAssRobot(wpi.IterativeRobot):

    def robotInit(self):
        """
            Called once when the robot starts up.
            This is where we initialize all of the robot's components.
        """

        # Joystick
        self.joystick = wpi.Joystick(j.JOYSTICK_INDEX)

        # Left front drive motor
        self.lMotor0 = wpi.CANTalon(d.L_CAN_INDICES[0])
        self.lMotor0.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.lMotor0.set(0.0)

        # Left back drive motor
        self.lMotor1 = wpi.CANTalon(d.L_CAN_INDICES[1])
        self.lMotor1.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.lMotor1.set(0.0)

        # Right front drive motor
        self.rMotor0 = wpi.CANTalon(d.R_CAN_INDICES[0])
        self.rMotor0.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.rMotor0.set(0.0)

        # Right back drive motor
        self.rMotor1 = wpi.CANTalon(d.R_CAN_INDICES[1])
        self.rMotor1.changeControlMode(wpi.CANTalon.ControlMode.PercentVbus)
        self.rMotor1.set(0.0)

        # Intake motors
        self.intakeMotor = wpi.VictorSP(b.INTAKE_INDEX)
        self.intakeMotor.set(0.0)

        self.ejectLever = wpi.VictorSP(2)
        self.ejectLever.set(0.0)

        # Lever limit switches
        self.leverLimit = wpi.DigitalInput(b.LEVER_LIMIT_INDICES[1])

        # Boom actuator motor
        self.armMotor = wpi.CANTalon(a.ARM_MOTOR_INDEX)
        self.armMotor.set(0.0)

        # Boom limit switch
        self.armUpperLimit = wpi.DigitalInput(a.ARM_LIMIT_INDEX)
        self.armLowerLimit = wpi.DigitalInput(2) # TODO move index to constant

        # Autonomous routine control switches
        self.as1 = wpi.DigitalInput(8)
        self.as2 = wpi.DigitalInput(9)

    def autonomousInit(self):
        """
            Called once every time autonomous mode begins.
        """

        # good
        r.playRoutine(int(self.as1.get() << 1) + int(self.as2.get() << 0))

    def autonomousPeriodic(self):
        # also good

        if r.isPlaying():

            # good

            joystickToUse = r.tickPlayback()
            if joystickToUse is None:
                joystickToUse = self.joystick
            joystickToUse = j.FakeJoystick("0.0:0.4:0.0:0.0:0.0:0.0/000000000000")

            lDriveSpd = d.getDriveLeft(joystick=joystickToUse)
            self.lMotor0.set(lDriveSpd)
            self.lMotor1.set(lDriveSpd)

            rDriveSpd = d.getDriveRight(joystick=joystickToUse)
            self.rMotor0.set(rDriveSpd / 1.1)
            self.rMotor1.set(rDriveSpd / 1.1)

            intakeMotorSpd = b.getIntakeSpeed(joystick=joystickToUse)
            self.intakeMotor.set(intakeMotorSpd)

            leverSpd = b.getEjectLeverSpeed(joystick=joystickToUse,
                limit=self.leverLimit)
            self.ejectLever.set(leverSpd)

            armSpd = a.getArmSpeed(joystick=joystickToUse, limit=self.armUpperLimit)
            self.armMotor.set(armSpd)

    def teleopPeriodic(self):
        """
            Called 50 times per second while the robot is in teleop (manual)
            mode. This is essentially one "frame" of the robot code; i.e. this
            is where we interpret user input, process built-in logic, and send
            component commands, in that order.
        """

        joystickToUse = self.joystick

        lDriveSpd = d.getDriveLeft(joystick=joystickToUse)
        self.lMotor0.set(lDriveSpd)
        self.lMotor1.set(lDriveSpd)

        rDriveSpd = d.getDriveRight(joystick=joystickToUse)
        self.rMotor0.set(rDriveSpd / 1.13) # CAPITALISM
        self.rMotor1.set(rDriveSpd / 1.13)

        intakeMotorSpd = b.getIntakeSpeed(joystick=joystickToUse)
        self.intakeMotor.set(intakeMotorSpd)

        leverSpd = b.getEjectLeverSpeed(joystick=joystickToUse,
            limit=self.leverLimit)
        self.ejectLever.set(leverSpd)

        armSpd = a.getArmSpeed(joystick=joystickToUse, limit=self.armUpperLimit)
        self.armMotor.set(armSpd)

        # print(self.armLowerLimit.get(), self.armUpperLimit.get())

    def testPeriodic(self):
        """
            Called 50 times per second while the robot is in test mode.
        """

        wpi.LiveWindow.run()

if __name__ == "__main__":
    wpi.run(SweetAssRobot)

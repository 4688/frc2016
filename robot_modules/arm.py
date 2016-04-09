#!/usr/bin/python3

from robot_modules.joystick import JoystickManager

import wpilib as wpi

class ArmManager:
    """
    Remember, if you ever need a helping hand, it's at the end of your arm,
    as you get older, remember you have another hand: The first is to help
    yourself, the second is to help others.
     - Audrey Hepburn
    """

    # CAN device index of the boom actuator.
    # Default: 5
    BOOM_MOTOR_INDEX = 5

    # DIO port index of the upper boom limit switch.
    # Default: 0
    BOOM_UPPER_LIMIT_INDEX = 0

    # DIO port index of the lower boom limit switch.
    # Default: 2
    BOOM_LOWER_LIMIT_INDEX = 2

    # Base speed of the boom actuator, as a percentage of maximum speed.
    # Be careful about setting this too high!
    # Default: 0.90 (90%)
    BOOM_BASE_SPD = 0.9

    @classmethod
    def getArmSpeed(cls, joystick, upLimit, downLimit):
        """
        Calculates and returns the speed of the arm.
        """

        ie = JoystickManager.EXTEND_BTN_INDEX
        ir = JoystickManager.RETRACT_BTN_INDEX

        eBtn = joystick.getRawButton(ie) and not downLimit.get()
        rBtn = joystick.getRawButton(ir) and upLimit.get()

        return cls.BOOM_BASE_SPD * ((1 if eBtn else 0) + (-1 if rBtn else 0))
#!/usr/bin/python3

from robot_modules.joystick import JoystickManager

class DriveManager:
    """
    The road to success is not easy to navigate, but with hard work, drive and
    passion, it's possible to achieve the American dream.
     - Tommy Hilfiger
    """

    # CAN device indices for left drive motors, front first.
    # Default: 1, 3
    L_CAN_INDICES = (1, 3)

    # CAN device indices for right drive motors, front first.
    # Default: 2, 4
    R_CAN_INDICES = (2, 4)

    # Deadband percent of the drive motors.
    # Default: 0.04 (4%)
    DRIVE_DEADBAND = 0.04

    # Divisor applied to forward/backward speed.
    # Default: 2
    DRIVE_SPD_DIVISOR = 2

    # Divisor applied to stationary pivot speed.
    # Default: 1.75
    TURN_SPD_DIVISOR = 1.75

    # Allow the driver to enable turbo mode?
    # Make sure this is True on competition builds!
    # Default: True
    ALLOW_TURBO = True

    # Factor applied to drive motor speed while in turbo mode.
    # Obviously, actual speed is capped at 100%.
    TURBO_FACTOR = 2

    @classmethod
    def _getBaseDrive(cls, joystick) -> float:
        """
        Calculates base drive speed, regardless of side.
        """

        yAxis = joystick.getRawAxis(JoystickManager.Y_AXIS_INDEX)
        return -yAxis / cls.DRIVE_SPD_DIVISOR

    @classmethod
    def getDriveLeft(cls, joystick) -> float:
        """
        Calculates and returns the speed of the left drive motors, relative
        to input.
        """

        xAxis = joystick.getRawAxis(JoystickManager.X_AXIS_INDEX)
        fwd = cls._getBaseDrive(joystick)
        turbo = cls.TURBO_FACTOR if cls.ALLOW_TURBO and joystick.getRawButton(
            JoystickManager.TURBO_BTN_INDEX) else 1

        if abs(fwd) <= cls.DRIVE_DEADBAND < abs(xAxis): # Stationary pivot
            return xAxis / cls.TURN_SPD_DIVISOR * turbo
        elif abs(fwd) > cls.DRIVE_DEADBAND: # Turn whilst driving
            turn = abs(xAxis * cls.TURN_SPD_DIVISOR) + 1
            fwd *= turbo
            return (fwd * turn) if xAxis > cls.DRIVE_DEADBAND else (fwd / turn)
        return 0.0

    @classmethod
    def getDriveRight(cls, joystick) -> float:
        """
        Calculates and returns the speed of the right drive motors, relative
        to input.
        """

        xAxis = joystick.getRawAxis(JoystickManager.X_AXIS_INDEX)
        fwd = -cls._getBaseDrive(joystick)
        turbo = cls.TURBO_FACTOR if cls.ALLOW_TURBO and joystick.getRawButton(
            JoystickManager.TURBO_BTN_INDEX) else 1

        if abs(fwd) <= cls.DRIVE_DEADBAND < abs(xAxis):
            return xAxis / cls.TURN_SPD_DIVISOR * turbo
        elif abs(fwd) > cls.DRIVE_DEADBAND:
            turn = abs(xAxis) + 1
            fwd *= turbo
            return (fwd / turn) if xAxis > cls.DRIVE_DEADBAND else (fwd * turn)
        return 0.0

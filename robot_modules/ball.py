#!/usr/bin/python3

from robot_modules.joystick import JoystickManager

class BallManager:
    """
    God has already done everything He's going to do. The ball is now in your
    court.
     - Joel Osteen
    """

    # PWM port index of the intake/eject motor controller.
    # Default: 1
    BALL_MOTOR_INDEX = 1

    # PWM port index of the ball release lever.
    # Default: 2
    RELEASE_LEVER_INDEX = 2

    # DIO port index of the limit switch for the release lever.
    # Default: 1
    LEVER_LIMIT_INDEX = 1

    @classmethod
    def getIntakeSpeed(cls, joystick) -> float:
        """
        Calculates and returns the speed of the intake motors, relative to
        input.
        """

        intake = joystick.getRawAxis(JoystickManager.INTAKE_AXIS_INDEX)
        eject = joystick.getRawAxis(JoystickManager.EJECT_AXIS_INDEX)
        return min((intake - eject) * 1.5, 1.0)

    @classmethod
    def getEjectLeverSpeed(cls, joystick, limit) -> float:
        """
        Returns the speed at which the lever should move to release the ball.
        """

        btn = joystick.getRawButton(JoystickManager.RELEASE_BTN_INDEX)
        switch = limit.get()
        if btn:
            return 0.4
        elif switch and not btn:
            return -0.2
        return 0.0
#!/usr/bin/python3

class JoystickManager:
    """
    Programmer's note:
    Unsurprisingly, I was unable to find a famous quote containing the word
    "joystick".
    """

    # USB device port index of the joystick.
    # Default: 0 (first port)
    JOYSTICK_INDEX = 0

    # Joystick axis index for forward/backward drive control.
    # Default: 1 (Analog stick inverted Y-axis)
    Y_AXIS_INDEX = 1

    # Joystick axis index for left/right drive control.
    # Default: 3 (C-Stick X-axis)
    X_AXIS_INDEX = 3

    # Joystick axis index for ball intake motors.
    # Default: 5 (R button pressure)
    INTAKE_AXIS_INDEX = 5

    # Joystick axis index for ball eject motors.
    # Default: 2 (L button pressure)
    EJECT_AXIS_INDEX = 2

    # Joystick button index for turbo mode.
    # Default: 5 (Z button)
    TURBO_BTN_INDEX = 5

    # Joystick button index for ball ejection lever operation.
    # Default: 1 (A button)
    RELEASE_BTN_INDEX = 1

    # Joystick button index for boom extension.
    # Default: 4 (Y button)
    EXTEND_BTN_INDEX = 4

    # Joystick button index for boom retraction.
    # Default: 3 (X button)
    RETRACT_BTN_INDEX = 3

    # Joystick button index for manual routine recording.
    # Press this button in conjunction with the routine-specific buttons to
    #  delete an existing routine and begin recording a new one.
    # Default: 2 (B button)
    RECORD_BTN_INDEX = 2

    # Joystick button indices for manual routine playback.
    # Press one of these buttons to manually run the corresponding recorded
    #  routine. Order is Up, Left, Down, Right.
    # Default: 9, 12, 10, 11

    class FakeJoystick:
        """
        An emulated joystick that is generated during routine playback. Can
        be used to imitate the state of an actual joystick by implementing
        all the appropriate functions, and the program will never know the
        difference. Just pass it as an argument instead of the actual
        joystick while playing back a routine.
        """

        def __init__(self, stateStr) -> None:
            axesState, btnsState = stateStr.split("/")

            # Split axes and buttons into manageable lists
            self.axes = [float(num) for num in axesState.split(":")]
            self.buttons = [bool(int(btn)) for btn in list(btnsState)]

        def getRawButton(self, btnIndex) -> bool:
            """
            Get the state of a button by index. NOT zero-indexed.
            """

            return self.buttons[btnIndex - 1]

        def getRawAxis(self, axisIndex) -> float:
            """
            Get the value of an axis by index.
            """

            return self.axes[axisIndex]

        def getButtonCount(self) -> int:
            return len(self.buttons)

        def getAxisCount(self) -> int:
            return len(self.axes)
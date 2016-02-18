#!/usr/bin/python3

# CONSTANTS
#===============================================================================

# USB device port index of the joystick.
# Default: 0 (first port)
JOYSTICK_INDEX = 0

# AXES
#-------------------------------------------------------------------------------

# Joystick axis index for forward/backward drive control.
# Default: 1 (Analog stick inverted Y-axis)
Y_AXIS_INDEX = 1

# Joystick axis index for left/right drive control.
# Default: 3 (C-stick X-axis)
X_AXIS_INDEX = 3

# Joystick axis index for ball intake motors.
# Default: 2 (L button pressure)
INTAKE_AXIS_INDEX = 2

# BUTTONS
#-------------------------------------------------------------------------------

# Joystick button index for turbo mode.
# Default: 5 (Z button)
TURBO_BTN_INDEX = 5

# Joystick button index for ball ejection command.
# Default: 1 (A button)
EJECT_BTN_INDEX = 1

# Joystick button index for boom extension.
# Default: 3 (X button)
EXTEND_BTN_INDEX = 3

# Joystick button index for boom retraction.
# Default: 4 (Y button)
RETRACT_BTN_INDEX = 4

# Joystick button index for manual routine recording.
# Press this button in combination with the routine-specific buttons to delete
#   an existing routine and begin recording a new one.
# Default: 2 (B button)
RECORD_BTN_INDEX = 2

# Joystick button indices for manual routine playback.
# Press one of these buttons to manually run the corresponding recorded routine.
# Order is Up, Right, Down, Left.
# Default: 9, 10, 11, 12
ROUTINE_BTN_INDICES = (9, 12, 10, 11)

# REPLAY JOYSTICK
#===============================================================================

class FakeJoystick:
    """
        A fake joystick that is generated during playback. Can be used to
        imitate the state of an actual joystick by implementing all the
        appropriate functions, and the program will never be the wiser. Just
        pass it as an argument instead of the actual joystick while playing
        back a routine.
    """

    def __init__(self, stateStr):
        pass

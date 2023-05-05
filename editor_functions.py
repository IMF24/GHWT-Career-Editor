# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#     G H W T     C A R E E R     E D I T O R     F U N C T I O N S
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Import required modules.
from editor_constants import *
import os as OS
import sys as SYS
from win32api import GetSystemMetrics

# Reset working directory.
def reset_working_directory() -> None:
    """ Reset our working directory to the original directory at the start of execution. """
    OS.chdir(OWD)

# Get native monitor resolution.
def get_screen_resolution() -> list[int]:
    """
    Returns the native resolution of the user's PRIMARY monitor.
    
    Returns
    -------
    `list[int]` >> A list of 2 numbers holding the width and height of the primary monitor, respectively.

    Example of Use
    --------------
    >>> print(get_screen_resolution())
    [1920, 1080]
    """
    return [GetSystemMetrics(0), GetSystemMetrics(1)]

# Relative path function.
def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a given resource. Used for compatibility with Python scripts compiled to EXEs using PyInstaller whose files have been embedded into the EXE itself.

    Tries at first to use `sys._MEIPASS`, which is used for relative paths. In the event it doesn't work, it will use the absolute path, and join it with the relative path given by the function's arguments.
    
    Arguments
    ---------
    `relative_path` : `str` >> The relative path to convert to an actual path.

    Returns
    -------
    `str` >> The actual path to the given resource.

    Example of Use
    --------------
    The actual output value will vary from device to device. In the below example, `~\` refers to `\"C:\\Users\\Your Username\"`.

    >>> print(resource_path(\"res/icon.ico\"))
    \"~\\Desktop\\GHWT DE Mod Development IDE\\res/icon.ico\"
    """
    # Try and use the actual path, if it exists.
    try:
        base_path = SYS._MEIPASS

    # In the event it doesn't, use the absolute path.
    except Exception:
        base_path = OS.path.abspath(".")

    # Join the paths together!
    return OS.path.join(base_path, relative_path)

# Reverse list.
def reverse_list(initiallist: list) -> list:
    """ Takes a given list and inverts the order of its contents. """
    result = []

    for (item) in (initiallist): result = [item] + result

    return result

# Return venue aspect.
def venue_get_aspect(mode: str, value: str) -> str:
    """ Return a different aspect to a venue. """
    match (mode):
        case 'zone':
            for (optionName, zoneName, _) in (TIER_VENUE_LIST):
                if (value == optionName): return zoneName
            else: return TIER_VENUE_LIST[0][1]

        case 'poster':
            for (optionName, _, posterName) in (TIER_VENUE_LIST):
                if (value == optionName): return posterName
            else: return TIER_VENUE_LIST[0][2]
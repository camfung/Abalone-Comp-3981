import os
import sys


def resource_path(relative_path):
    """
    Return the absolute path to a bundled resource.
    Works both during development (relative to project root) and when
    frozen by PyInstaller (relative to sys._MEIPASS / _internal/).
    """
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, relative_path)

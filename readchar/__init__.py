import importlib.metadata


__doc__ = """Library to easily read single chars and key strokes"""

__version__ = importlib.metadata.version(__package__)
__all__ = [
    "readchar",
    "readkey",
    "key",
    "config",
    "tryreadchar",
    "tryreadkey",
    "claim_terminal",
    "unclaim_terminal",
]

from sys import platform

from ._config import config


if platform.startswith(("linux", "darwin", "freebsd", "openbsd", "android")):
    from . import _posix_key as key
    from ._posix_read import readchar, readkey
    from ._posix_tryread import (
        claim_terminal,
        tryreadchar,
        tryreadkey,
        unclaim_terminal,
    )
elif platform in ("win32", "cygwin"):
    from . import _win_key as key
    from ._win_read import readchar, readkey
    from ._win_tryread import claim_terminal, tryreadchar, tryreadkey, unclaim_terminal
else:
    raise NotImplementedError(f"The platform {platform} is not supported yet")


from ._base_tryread import TerminalSession

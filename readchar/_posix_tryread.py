import select
import sys
import termios

from ._config import config


# based on _posix_read.py


_old_settings = None


def claim_terminal() -> None:
    """Changes the terminal's settings to provide every keypress immediately.
    Calls to this function cannot be nested.
    The changes are global, even after the program exits:
    be sure to unclaim_terminal() before exiting."""
    global _old_settings

    if _old_settings is not None:
        raise RuntimeError(
            "Terminal already claimed; claim_terminal() cannot be nested"
        )

    fd = sys.stdin.fileno()

    _old_settings = termios.tcgetattr(fd)
    term = termios.tcgetattr(fd)

    term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
    termios.tcsetattr(fd, termios.TCSAFLUSH, term)


def unclaim_terminal() -> None:
    """Returns the terminal's settings to before the last call to claim_terminal().
    If the terminal was not claimed, calling this does nothing.
    Be sure to call this before exiting."""
    global _old_settings

    if _old_settings is None:
        return

    fd = sys.stdin.fileno()

    termios.tcsetattr(fd, termios.TCSADRAIN, _old_settings)

    _old_settings = None


def tryreadchar() -> str | None:
    """Tries to read a single character from the input stream.
    Use claim_terminal the terminal to get every keypress.
    If the stream is empty, returns None."""

    fd = sys.stdin.fileno()

    ready, _, _ = select.select([fd], [], [], 0)
    if ready:
        ch = sys.stdin.read(1)
        return ch
    else:
        return None


def tryreadkey() -> str | None:
    """Try to get a keypress. If an escaped key is pressed, the full sequence is
    read and returned as noted in `_posix_key.py`."""

    c1 = tryreadchar()

    if c1 is None:
        return None

    if c1 in config.INTERRUPT_KEYS:
        raise KeyboardInterrupt

    if c1 != "\x1B":
        return c1

    c2 = tryreadchar()
    if c2 not in "\x4F\x5B":
        return c1 + c2

    c3 = tryreadchar()
    if c3 not in "\x31\x32\x33\x35\x36":
        return c1 + c2 + c3

    c4 = tryreadchar()
    if c4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
        return c1 + c2 + c3 + c4

    c5 = tryreadchar()
    return c1 + c2 + c3 + c4 + c5

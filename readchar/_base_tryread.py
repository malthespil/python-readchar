from sys import platform


if platform.startswith(("linux", "darwin", "freebsd", "openbsd", "android")):
    from ._posix_tryread import claim_terminal, unclaim_terminal
elif platform in ("win32", "cygwin"):
    from ._win_tryread import claim_terminal, unclaim_terminal

class TerminalSession:
    def __enter__(self):
        claim_terminal()
    def __exit__(self, _0,_1,_2):
        unclaim_terminal()

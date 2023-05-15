import sys
from logging import getLogger
from subprocess import PIPE, Popen  # nosec

from pkg_resources import resource_filename

logger = getLogger(__name__)

_exe_name = "core.exe" if sys.platform == "win32" else "core"
executable_path = resource_filename("applitools.core_universal", "bin/" + _exe_name)


class SDKServer(object):
    log_file_name = None  # backward compatibility with eyes-selenium<=5.6

    def __init__(self):
        """Start core-universal service subprocess and obtain its port number."""
        command = [
            executable_path,
            "universal",
            "--no-singleton",
            "--shutdown-mode",
            "stdin",
        ]
        # Capture and keep stdin reference to notify USDK when it should terminate.
        # USDK is expected to terminate when it receives EOF on its stdin.
        # The pipe is automatically closed and EOF is sent by OS when python terminates.
        self._usdk_subprocess = Popen(command, stdin=PIPE, stdout=PIPE)  # nosec
        self.port = int(self._usdk_subprocess.stdout.readline())
        logger.info("Started Universal SDK server at %s", self.port)

    def __repr__(self):
        """Produce helpful debugging description."""
        return "SDKServer(port={})".format(self.port)

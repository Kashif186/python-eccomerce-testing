from enum import Enum

import attr

__all__ = ("SessionType", "FailureReports", "ServerInfo")


@attr.s
class ServerInfo(object):
    logs_dir = attr.ib()


class SessionType(Enum):
    # default type of sessions.
    SEQUENTIAL = "SEQUENTIAL"
    # a timing test session
    PROGRESSION = "PROGRESSION"


class FailureReports(Enum):
    """
    Failures are either reported immediately when they are detected, or when the test is closed.
    """

    # Failures are reported immediately when they are detected.
    IMMEDIATE = "Immediate"
    # Failures are reported when tests are completed (i.e., when
    # :py:class:`EyesBase.close()` is called).
    ON_CLOSE = "OnClose"

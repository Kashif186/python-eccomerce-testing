from itertools import count
from typing import TYPE_CHECKING

from .marshaller import Marshaller

if TYPE_CHECKING:
    from ..common.connection import USDKConnection
    from .object_registry import ObjectRegistry


class CommandContext(object):
    def __init__(self, connection, object_registry):
        # type: (USDKConnection, ObjectRegistry) -> None
        self._connection = connection
        self.object_registry = object_registry
        self.key = self.object_registry.next_command_key()
        self.marshaller = Marshaller(self.object_registry)

    def execute_callback(self, command):
        # type: (dict) -> None
        raise NotImplementedError


class SeleniumWebdriverCommandContext(CommandContext):
    pass

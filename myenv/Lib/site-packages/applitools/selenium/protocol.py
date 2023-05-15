from typing import TYPE_CHECKING

from .command_context import CommandContext, SeleniumWebdriverCommandContext
from .object_registry import ObjectRegistry, SeleniumWebdriverObjectRegistry

if TYPE_CHECKING:
    from typing import Optional

    from ..common.connection import USDKConnection


class USDKProtocol(object):
    KIND = None
    COMMANDS = None
    ObjectRegistry = ObjectRegistry
    CommandContext = CommandContext

    @classmethod
    def object_registry(cls):
        return cls.ObjectRegistry()

    @classmethod
    def context(cls, connection, object_registry=None):
        # type: (USDKConnection, Optional[ObjectRegistry]) -> CommandContext
        return cls.CommandContext(connection, object_registry or cls.object_registry())


class SeleniumWebDriver(USDKProtocol):
    KIND = "webdriver"
    ObjectRegistry = SeleniumWebdriverObjectRegistry
    CommandContext = SeleniumWebdriverCommandContext

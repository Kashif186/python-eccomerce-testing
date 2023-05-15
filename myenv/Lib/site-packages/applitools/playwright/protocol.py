from __future__ import absolute_import

from applitools.selenium.protocol import USDKProtocol

from .command_context import PlaywrightSpecDriverCommandContext
from .object_registry import PlaywrightSpecDriverObjectRegistry


class PlaywrightSpecDriver(USDKProtocol):
    KIND = "specdriver"
    COMMANDS = [
        "executeScript",
        "childContext",
        "findElement",
        "findElements",
        "getCookies",
        "getDriverInfo",
        "getTitle",
        "getUrl",
        "getViewportSize",
        "isDriver",
        "isElement",
        "isSelector",
        "mainContext",
        "setViewportSize",
        "takeScreenshot",
    ]
    ObjectRegistry = PlaywrightSpecDriverObjectRegistry
    CommandContext = PlaywrightSpecDriverCommandContext

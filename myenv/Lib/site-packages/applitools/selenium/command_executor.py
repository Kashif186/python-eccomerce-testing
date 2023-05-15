from __future__ import absolute_import

import logging
from enum import Enum
from os import getcwd
from threading import Lock
from typing import TYPE_CHECKING, Any, List, Optional, Text

from ..common import TestResults
from ..common.connection import USDKConnection
from ..common.errors import USDKFailure
from ..common.target import ImageTarget
from .schema import demarshal_error

if TYPE_CHECKING:
    from typing import Tuple, Type, Union

    from ..common.selenium import Configuration
    from ..common.utils.custom_types import ViewPort
    from ..core import TextRegionSettings, VisualLocatorSettings
    from ..core.batch_close import _EnabledBatchClose  # noqa
    from ..core.ec_client_settings import ECClientSettings
    from ..core.extract_text import OCRRegion
    from .command_context import CommandContext
    from .fluent import SeleniumCheckSettings
    from .object_registry import ObjectRegistry
    from .optional_deps import WebDriver
    from .protocol import USDKProtocol

logger = logging.getLogger(__name__)

Failure = USDKFailure  # backward compatibility with eyes-selenium==5.0.0


class ManagerType(Enum):
    UFG = "ufg"
    CLASSIC = "classic"


class CommandExecutor(object):
    @classmethod
    def create(cls, protocol, name, version):
        # type: (Type[USDKProtocol], Text, Text) -> CommandExecutor
        commands = cls(protocol, USDKConnection.create())
        commands.make_core("{}/{}".format(name, version), getcwd())
        return commands

    @classmethod
    def get_instance(cls, protocol, name, version):
        # type: (Type[USDKProtocol], Text, Text) -> CommandExecutor
        with _instances_lock:
            key = (protocol, name, version)
            if key in _instances:
                return _instances[key]
            else:
                return _instances.setdefault(key, cls.create(*key))

    def __init__(self, protocol, connection):
        # type: (Type[USDKProtocol], USDKConnection) -> None
        self._protocol = protocol
        self._connection = connection

    def make_core(self, agent_id, cwd):
        # type: (Text, Text) -> None
        spec = self._protocol.COMMANDS if self._protocol.COMMANDS else "webdriver"
        self._connection.notification(
            "Core.makeCore",
            {
                "agentId": agent_id,
                "cwd": cwd,
                "spec": spec,
            },
        )

    def core_make_ec_client(self, ec_client_settings):
        # type: (ECClientSettings) -> Text
        context = self._protocol.context(self._connection)
        m = context.marshaller
        settings = m.marshal_ec_client_settings(ec_client_settings)
        return self._checked_command(
            context, "Core.makeECClient", {"settings": settings}
        )

    def core_make_manager(
        self, manager_type, concurrency=None, legacy_concurrency=None, agent_id=None
    ):
        # type: (ManagerType, Optional[int], Optional[int], Optional[Text]) -> dict
        context = self._protocol.context(self._connection)
        settings = {}
        if concurrency is not None:
            settings["concurrency"] = concurrency
        if legacy_concurrency is not None:
            settings["legacyConcurrency"] = legacy_concurrency
        if agent_id is not None:
            settings["agentId"] = agent_id
        payload = {"type": manager_type.value, "settings": settings}
        return self._checked_command(context, "Core.makeManager", payload)

    def core_get_viewport_size(self, driver):
        # type: (WebDriver) -> dict
        context = self._protocol.context(self._connection)
        m = context.marshaller
        target = m.marshal_webdriver_ref(driver)
        return self._checked_command(
            context, "Core.getViewportSize", {"target": target}
        )

    def core_set_viewport_size(self, driver, size):
        # type: (WebDriver, ViewPort) -> None
        context = self._protocol.context(self._connection)
        m = context.marshaller
        target = m.marshal_webdriver_ref(driver)
        self._checked_command(
            context,
            "Core.setViewportSize",
            {"target": target, "size": m.marshal_viewport_size(size)},
        )

    def core_close_batch(self, close_batch_settings):
        # type: (_EnabledBatchClose) -> None
        context = self._protocol.context(self._connection)
        m = context.marshaller
        settings = []
        for batch_id in close_batch_settings._ids:  # noqa
            close_batch_settings.batch_id = batch_id
            settings.append(m.marshal_enabled_batch_close(close_batch_settings))
        self._checked_command(context, "Core.closeBatch", {"settings": settings})

    def core_delete_test(self, test_results):
        # type: (TestResults) -> None
        context = self._protocol.context(self._connection)
        m = context.marshaller
        settings = m.marshal_delete_test_settings(test_results)
        self._checked_command(context, "Core.deleteTest", {"settings": settings})

    def manager_open_eyes(
        self,
        object_registry,  # type: ObjectRegistry
        manager,  # type: dict
        target=None,  # type: Optional[WebDriver]
        config=None,  # type: Optional[Configuration]
    ):
        # type: (...) -> dict
        context = self._protocol.context(self._connection, object_registry)
        m = context.marshaller
        payload = {"manager": manager}
        if target is not None:
            payload["target"] = m.marshal_webdriver_ref(target)
        if config is not None:
            payload["config"] = m.marshal_configuration(config)
        return self._checked_command(context, "EyesManager.openEyes", payload)

    def manager_get_results(self, manager, raise_ex, remove_duplicate_tests, timeout):
        # type: (dict, bool, Optional[bool], float) -> List[dict]
        context = self._protocol.context(self._connection)
        settings = {"throwErr": raise_ex}
        if remove_duplicate_tests is not None:
            settings["removeDuplicateTests"] = remove_duplicate_tests

        return self._checked_command(
            context,
            "EyesManager.getResults",
            {"manager": manager, "settings": settings},
            wait_timeout=timeout,
        )

    def eyes_check(
        self,
        object_registry,  # type: ObjectRegistry
        eyes,  # type: dict
        target,  # type: Optional[ImageTarget]
        settings,  # type: SeleniumCheckSettings
        config,  # type: Configuration
    ):
        # type: (...) -> dict
        context = self._protocol.context(self._connection, object_registry)
        m = context.marshaller
        payload = {
            "eyes": eyes,
            "settings": m.marshal_check_settings(settings),
            "config": m.marshal_configuration(config),
        }
        if target:
            payload["target"] = m.marshal_image_target(target)
        return self._checked_command(context, "Eyes.check", payload)

    def core_locate(self, target, settings, config):
        # type: (WebDriver, VisualLocatorSettings, Configuration) -> dict
        context = self._protocol.context(self._connection)
        m = context.marshaller
        payload = {
            "target": m.marshal_webdriver_ref(target),
            "settings": m.marshal_locate_settings(settings),
            "config": m.marshal_configuration(config),
        }
        return self._checked_command(context, "Core.locate", payload)

    def core_extract_text(
        self,
        target,  # type: Union[WebDriver, ImageTarget]
        settings,  # type: Tuple[OCRRegion]
        config,  # type: Configuration
    ):
        # type: (...) -> List[Text]
        context = self._protocol.context(self._connection)
        m = context.marshaller
        payload = {
            "settings": m.marshal_ocr_extract_settings(settings),
            "config": m.marshal_configuration(config),
        }
        if isinstance(target, ImageTarget):
            payload["target"] = m.marshal_image_target(target)
        else:
            payload["target"] = m.marshal_webdriver_ref(target)
        return self._checked_command(context, "Core.extractText", payload)

    def core_locate_text(
        self,
        target,  # type: Union[WebDriver, ImageTarget]
        settings,  # type: TextRegionSettings
        config,  # type: Configuration
    ):
        # type: (...) -> dict
        context = self._protocol.context(self._connection)
        m = context.marshaller
        payload = {
            "settings": m.marshal_ocr_search_settings(settings),
            "config": m.marshal_configuration(config),
        }
        if isinstance(target, ImageTarget):
            payload["target"] = m.marshal_image_target(target)
        else:
            payload["target"] = m.marshal_webdriver_ref(target)
        return self._checked_command(context, "Core.locateText", payload)

    def eyes_close(self, object_registry, eyes, throw_err, config):
        # type: (ObjectRegistry, dict, bool, Configuration) -> List[dict]
        context = self._protocol.context(self._connection, object_registry)
        m = context.marshaller
        payload = {
            "eyes": eyes,
            "settings": {"throwErr": throw_err},
            "config": m.marshal_configuration(config),
        }
        return self._checked_command(context, "Eyes.close", payload)

    def eyes_abort(self, object_registry, eyes):
        # type: (ObjectRegistry, dict) -> List[dict]
        context = self._protocol.context(self._connection, object_registry)
        return self._checked_command(context, "Eyes.abort", {"eyes": eyes})

    def eyes_get_results(self, eyes, throw_err):
        context = self._protocol.context(self._connection)
        payload = {
            "eyes": eyes,
            "settings": {"throwErr": throw_err},
        }
        return self._checked_command(context, "Eyes.getResults", payload)

    def server_get_info(self):
        # type: () -> dict
        context = self._protocol.context(self._connection)
        return self._checked_command(context, "Server.getInfo", {})

    def _checked_command(self, command_context, name, payload, wait_timeout=9 * 60):
        # type: (CommandContext, Text, dict, float) -> Optional[Any]
        response = self._connection.command(
            command_context, name, payload, wait_timeout
        )
        response_payload = response["payload"]
        _check_error(response_payload)
        return response_payload.get("result")


def _check_error(payload):
    # type: (dict) -> None
    error = payload.get("error")
    if error:
        usdk_error = demarshal_error(error)
        logger.error("Re-raising an error received from SDK server: %r", usdk_error)
        raise usdk_error


_instances = {}
_instances_lock = Lock()

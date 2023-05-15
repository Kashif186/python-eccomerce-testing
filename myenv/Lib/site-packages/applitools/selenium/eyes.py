from __future__ import absolute_import, unicode_literals

import json
import typing
from typing import List, Optional, Text, Tuple, Union

from six import string_types

from applitools.common import (
    EyesError,
    FailureReports,
    ProxySettings,
    RectangleSize,
    TestFailedError,
    deprecated,
)
from applitools.common.selenium import Configuration

from ..common.errors import USDKFailure
from ..common.utils.general_utils import get_env_with_prefix
from ..core.ec_client_settings import ECClientCapabilities, ECClientSettings
from .__version__ import __version__
from .command_executor import CommandExecutor
from .fluent.selenium_check_settings import SeleniumCheckSettings
from .fluent.target import Target
from .runner import ClassicRunner, EyesRunner, log_session_results_and_raise_exception
from .schema import (
    demarshal_locate_result,
    demarshal_match_result,
    demarshal_test_results,
)

if typing.TYPE_CHECKING:
    from applitools.common import MatchResult, Region, TestResults
    from applitools.common.utils.custom_types import FrameReference, ViewPort
    from applitools.core import (
        PositionProvider,
        TextRegionSettings,
        VisualLocatorSettings,
    )
    from applitools.core.extract_text import PATTERN_TEXT_REGIONS
    from applitools.core.locators import LOCATORS_TYPE
    from applitools.selenium import OCRRegion
    from applitools.selenium.optional_deps import WebDriver, WebElement

    from ..playwright.optional_deps import ElementHandle, Page, PlaywrightLocator


class Eyes(object):
    DefaultRunner = ClassicRunner

    def __init__(self, runner=None):
        # type: (Union[None, EyesRunner, Text]) -> None
        self.configure = Configuration()
        self._object_registry = None
        self._driver = None
        self._eyes_ref = None
        if runner is None:
            self._runner = self.DefaultRunner()
        elif isinstance(runner, string_types):
            self.configure.server_url = runner
            self._runner = self.DefaultRunner()
        else:
            self._runner = runner  # type: EyesRunner
        self._commands = self._runner._commands  # noqa

    def open(
        self,
        driver,  # type: Union[WebDriver, Page]
        app_name=None,  # type: Optional[Text]
        test_name=None,  # type: Optional[Text]
        viewport_size=None,  # type: Optional[ViewPort]
    ):
        # type: (...) -> Union[WebDriver, Page]
        if app_name is not None:
            self.configure.app_name = app_name
        if test_name is not None:
            self.configure.test_name = test_name
        if viewport_size is not None:
            self.configure.viewport_size = viewport_size
        if self.configure.app_name is None:
            raise ValueError("app_name should be set via configuration or an argument")
        if self.configure.test_name is None:
            raise ValueError("test_name should be set via configuration or an argument")

        if self.configure.is_disabled:
            pass
        else:
            self._runner._set_connection_config(self.configure)  # noqa, friend
            self._object_registry = self._runner.Protocol.object_registry()
            self._driver = driver
            self._eyes_ref = self._commands.manager_open_eyes(
                self._object_registry,
                self._runner._ref,  # noqa
                driver,
                config=self.configure,
            )
        return driver

    @typing.overload
    def check(self, name, check_settings):
        # type: (Text, SeleniumCheckSettings) -> MatchResult
        """
        Takes a snapshot and matches it with the expected output.

        :param name: The name of the tag.
        :param check_settings: target which area of the window to check.
        """
        pass

    @typing.overload
    def check(self, check_settings):
        # type: (SeleniumCheckSettings) -> None
        """
        Takes a snapshot and matches it with the expected output.

        :param check_settings: target which area of the window to check.
        """
        pass

    def check(self, check_settings, name=None):
        # type: (SeleniumCheckSettings, Optional[Text]) -> Optional[MatchResult]
        if isinstance(name, SeleniumCheckSettings) or isinstance(
            check_settings, string_types
        ):
            check_settings, name = name, check_settings
        if check_settings is None:
            check_settings = Target.window()
        if name:
            check_settings = check_settings.with_name(name)

        if self.configure.is_disabled:
            return None
        if not self.is_open:
            self.abort()
            raise EyesError("you must call open() before checking")

        results = self._commands.eyes_check(
            self._object_registry,
            self._eyes_ref,
            None,
            check_settings,
            self.configure,
        )
        if results:
            # Original API only returns one result
            results = demarshal_match_result(results[0])
            if (
                not results.as_expected
                and self.configure.failure_reports is FailureReports.IMMEDIATE
            ):
                raise TestFailedError(
                    "Mismatch found in '{}' of '{}'".format(
                        self.configure.test_name, self.configure.app_name
                    )
                )
            else:
                return results
        else:
            return None

    def locate(self, visual_locator_settings):
        # type: (VisualLocatorSettings) -> LOCATORS_TYPE
        results = self._commands.core_locate(
            self.driver,
            visual_locator_settings,
            self.configure,
        )
        return demarshal_locate_result(results)

    def extract_text(self, *regions):
        # type: (*OCRRegion) -> List[Text]
        return self._commands.core_extract_text(
            self.driver,
            regions,
            self.configure,
        )

    @deprecated.attribute(
        "The `extract_text_regions` is deprecated. Use `locate_text` instead"
    )
    def extract_text_regions(self, config):
        # type: (TextRegionSettings) -> PATTERN_TEXT_REGIONS
        return self.locate_text(config)

    def locate_text(self, config):
        # type: (TextRegionSettings) -> PATTERN_TEXT_REGIONS
        return self._commands.core_locate_text(self.driver, config, self.configure)

    def close(self, raise_ex=True):
        # type: (bool) -> Optional[TestResults]
        """
        Ends the test.

        :param raise_ex: If true, an exception will be raised for failed/new tests.
        :return: The test results.
        """
        return self._close(raise_ex, True)

    def close_async(self):
        # type: () -> Optional[TestResults]
        return self._close(False, False)

    def abort(self):
        # type: () -> Optional[TestResults]
        """
        If a test is running, aborts it. Otherwise, does nothing.
        """
        return self._abort(True)

    def abort_async(self):
        return self._abort(False)

    @deprecated.attribute("use `abort()` instead")
    def abort_if_not_closed(self):
        return self.abort()

    @classmethod
    def get_viewport_size(cls, driver):
        # type: (Union[WebDriver, Page]) -> RectangleSize
        cmd = CommandExecutor.get_instance(
            cls.DefaultRunner.Protocol, cls.DefaultRunner.BASE_AGENT_ID, __version__
        )
        result = cmd.core_get_viewport_size(driver)
        return RectangleSize.from_(result)

    @classmethod
    def set_viewport_size(cls, driver, viewport_size):
        # type: (Union[WebDriver, Page], ViewPort) -> None
        cmd = CommandExecutor.get_instance(
            cls.DefaultRunner.Protocol, cls.DefaultRunner.BASE_AGENT_ID, __version__
        )
        cmd.core_set_viewport_size(driver, viewport_size)

    @property
    def configuration(self):
        return self.configure

    @configuration.setter
    def configuration(self, value):
        self.configure = value

    def get_configuration(self):
        # type:() -> Configuration
        return self.configure.clone()

    def set_configuration(self, configuration):
        # type:(Configuration) -> None
        self.configure = configuration.clone()

    @staticmethod
    def set_nmg_capabilities(
        caps,  # type: dict
        api_key=None,  # type: Optional[Text]
        eyes_server_url=None,  # type: Optional[Text]
        proxy_settings=None,  # type: Optional[Union[Text, ProxySettings]]
    ):
        # type: (...) -> None
        if not api_key:
            api_key = get_env_with_prefix("APPLITOOLS_API_KEY")
            if not api_key:
                raise EyesError("No API key was given, or is an empty string.")
        env_caps = {
            "NML_API_KEY": api_key,
        }

        if not eyes_server_url:
            eyes_server_url = get_env_with_prefix("APPLITOOLS_SERVER_URL")
        if eyes_server_url:
            env_caps["NML_SERVER_URL"] = eyes_server_url

        if not proxy_settings:
            proxy_settings = ProxySettings.from_env()
        elif isinstance(proxy_settings, string_types):
            proxy_settings = ProxySettings(proxy_settings)
        if proxy_settings:
            env_caps["NML_PROXY_URL"] = proxy_settings.url

        # for iOS
        ios_env_caps = {
            "DYLD_INSERT_LIBRARIES": (
                "@executable_path/Frameworks/UFG_lib.xcframework/ios-arm64_x86_64-simulator/UFG_lib.framework/UFG_lib"
                ":@executable_path/Frameworks/UFG_lib.xcframework/ios-arm64/UFG_lib.framework/UFG_lib"
            )
        }
        ios_env_caps.update(env_caps)
        caps["processArguments"] = {
            "args": [],
            "env": ios_env_caps,
        }
        # for Android
        caps["optionalIntentArguments"] = "--es APPLITOOLS '{}'".format(
            json.dumps(env_caps, sort_keys=True)
        )

    @classmethod
    def get_execution_cloud_url(cls, api_key=None, server_url=None, proxy=None):
        # type: (Text, Text, ProxySettings) -> Text
        cmd = CommandExecutor.get_instance(
            cls.DefaultRunner.Protocol, cls.DefaultRunner.BASE_AGENT_ID, __version__
        )
        result = cmd.core_make_ec_client(
            ECClientSettings(ECClientCapabilities(api_key, server_url), proxy)
        )
        return result["url"]

    @property
    def is_open(self):
        # type: () -> bool
        return self._eyes_ref is not None

    @property
    def server_connector(self):
        raise NotImplementedError

    @server_connector.setter
    def server_connector(self, server_connector):
        raise NotImplementedError

    @property
    def base_agent_id(self):
        # type: () -> Text
        """
        Must return version of SDK. (e.g. selenium, visualgrid) in next format:
            "eyes.{package}.python/{lib_version}"
        """
        return "{}/{}".format(self._runner.BASE_AGENT_ID, __version__)

    @property
    def full_agent_id(self):
        # type: () -> Text
        """
        Gets the agent id, which identifies the current library using the SDK.

        """
        if self.configure.agent_id is None:
            return self.base_agent_id
        else:
            return "{} [{}]".format(self.configure.agent_id, self.base_agent_id)

    @property
    def is_cut_provider_explicitly_set(self):
        # type: () -> bool
        """
        Gets is cut provider explicitly set.
        """
        raise self.configure.cut_provider is not None

    @property
    def driver(self):
        # type: () -> WebDriver
        return self._driver

    def check_window(self, tag=None, match_timeout=-1, fully=None):
        # type: (Optional[Text], int, Optional[bool]) -> MatchResult
        """
        Takes a snapshot of the application under test and matches it with the expected
         output.

        :param tag: An optional tag to be associated with the snapshot.
        :param match_timeout:  The amount of time to retry matching (milliseconds)
        :param fully: Defines that the screenshot will contain the entire window.
        """
        return self.check(tag, Target.window().timeout(match_timeout).fully(fully))

    def check_frame(self, frame_reference, tag=None, match_timeout=-1):
        # type: (FrameReference, Optional[Text], int) -> MatchResult
        """
        Check frame.

        :param frame_reference: The name or id of the frame to check. (The same
                name/id as would be used in a call to driver.switch_to.frame()).
        :param tag: An optional tag to be associated with the match.
        :param match_timeout: The amount of time to retry matching. (Milliseconds)
        """
        return self.check(
            tag, Target.frame(frame_reference).fully().timeout(match_timeout)
        )

    def check_region(
        self,
        region,  # type: Union[Region, Text, List, Tuple, WebElement]
        tag=None,  # type: Optional[Text]
        match_timeout=-1,  # type: int
        stitch_content=False,  # type: bool
    ):
        # type: (...) -> MatchResult
        """
        Takes a snapshot of the given region from the browser using the web driver
        and matches it with the expected output. If the current context is a frame,
        the region is offsetted relative to the frame.

        :param region: The region which will be visually validated. The coordinates are
                       relative to the viewport of the current frame.
        :param tag: Description of the visual validation checkpoint.
        :param match_timeout: Timeout for the visual validation checkpoint
                              (milliseconds).
        :param stitch_content: If `True`, stitch the internal content of the region
        """
        return self.check(
            tag,
            Target.region(region).timeout(match_timeout).fully(stitch_content),
        )

    def check_element(
        self,
        element,
        # type: Union[Text,List,Tuple,WebElement,PlaywrightLocator,ElementHandle]
        tag=None,  # type: Optional[Text]
        match_timeout=-1,  # type: int
    ):
        # type: (...) -> MatchResult
        """
        Takes a snapshot of the given region from the browser using the web driver
        and matches it with the expected output. If the current context is a frame,
        the region is offsetted relative to the frame.

        :param element: The element to check.
        :param tag: Description of the visual validation checkpoint.
        :param match_timeout: Timeout for the visual validation checkpoint
                              (milliseconds).
        """
        return self.check(
            tag,
            Target.region(element).timeout(match_timeout).fully(),
        )

    def check_region_in_frame(
        self,
        frame_reference,  # type: FrameReference
        region,
        # type: Union[Region,Text,List,Tuple,WebElement,PlaywrightLocator,ElementHandle]
        tag=None,  # type: Optional[Text]
        match_timeout=-1,  # type: int
        stitch_content=False,  # type: bool
    ):
        # type: (...) -> MatchResult
        """
        Checks a region within a frame, and returns to the current frame.

        :param frame_reference: A reference to the frame in which the region
                                should be checked.
        :param region: Specifying the region to check inside the frame.
        :param tag: Description of the visual validation checkpoint.
        :param match_timeout: Timeout for the visual validation checkpoint
                              (milliseconds).
        :param stitch_content: If `True`, stitch the internal content of the region
        """
        return self.check(
            tag,
            Target.region(region)
            .frame(frame_reference)
            .stitch_content(stitch_content)
            .timeout(match_timeout),
        )

    # Impossible to implement via universal sdk
    @property
    def should_stitch_content(self):
        # type: () -> bool
        raise NotImplementedError

    @property
    def original_fc(self):
        """Gets original frame chain

        Before check() call we save original frame chain

        Returns:
            Frame chain saved before check() call
        """
        raise NotImplementedError

    @property
    def device_pixel_ratio(self):
        # type: () -> int
        """
        Gets device pixel ratio.

        :return The device pixel ratio, or if the DPR is not known yet or if it wasn't
        possible to extract it.
        """
        raise NotImplementedError

    @property
    def debug_screenshots_provider(self):
        raise NotImplementedError

    @property
    def position_provider(self):
        """
        Sets position provider.
        """
        raise NotImplementedError

    @property
    def current_frame_position_provider(self):
        # type: () -> Optional[PositionProvider]
        raise NotImplementedError

    def add_mouse_trigger_by_element(self, action, element):
        # type: (Text, WebElement) -> None
        """
        Adds a mouse trigger.

        :param action: Mouse action (click, double click etc.)
        :param element: The element on which the action was performed.
        """
        raise NotImplementedError

    def add_text_trigger_by_element(self, element, text):
        # type: (WebElement, Text) -> None
        """
        Adds a text trigger.

        :param element: The element to which the text was sent.
        :param text: The trigger's text.
        """
        raise NotImplementedError

    @property
    def agent_setup(self):
        # Saved for backward compatibility
        return None

    def _close(self, raise_ex, wait_result):
        # type: (bool, bool) -> Optional[TestResults]
        if self.configure.is_disabled:
            return None
        if not self.is_open:
            raise EyesError("Eyes not open")
        self._commands.eyes_close(
            self._object_registry, self._eyes_ref, raise_ex, self.configure
        )
        if wait_result:
            results = self._commands.eyes_get_results(self._eyes_ref, raise_ex)
        else:
            results = None
        self._eyes_ref = None
        self._driver = None
        self._object_registry = None
        if results is not None:
            results = demarshal_test_results(results, self.configure)
            if results:  # eyes are already aborted by closed runner
                for r in results:
                    log_session_results_and_raise_exception(raise_ex, r)
                return results[0]  # Original interface returns just one result
        return None

    def _abort(self, wait_result):
        # type: (bool) -> Optional[TestResults]
        if self.configure.is_disabled:
            return None
        elif self.is_open:
            self._commands.eyes_abort(self._object_registry, self._eyes_ref)
            if wait_result:
                results = self._commands.eyes_get_results(self._eyes_ref, False)
            else:
                results = None
            self._eyes_ref = None
            self._driver = None
            self._object_registry = None
            if results is not None:
                if results:  # abort after close does not return results
                    results = demarshal_test_results(results, self.configure)
                    for r in results:
                        log_session_results_and_raise_exception(False, r)
                    return results[0]  # Original interface returns just one result
            return None

    def __getattr__(self, item):
        return getattr(self.configure, item)

    def __setattr__(self, key, value):
        if "configure" in vars(self) and (
            key in vars(self.configure)
            or key in ("match_level", "ignore_displacements")
        ):
            return setattr(self.configure, key, value)
        else:
            return super(Eyes, self).__setattr__(key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._abort(self._runner.AUTO_CLOSE_MODE_SYNC)
        else:
            self._close(True, self._runner.AUTO_CLOSE_MODE_SYNC)

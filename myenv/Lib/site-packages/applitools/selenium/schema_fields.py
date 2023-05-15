from __future__ import absolute_import

import enum
import typing as t

from marshmallow.fields import Dict, Field

from applitools.selenium.optional_deps import StaleElementReferenceException

from ..common import (
    AndroidDeviceInfo,
    ChromeEmulationInfo,
    DesktopBrowserInfo,
    DiffsFoundError,
    IosDeviceInfo,
    NewTestError,
    TestFailedError,
)
from ..common.errors import USDKFailure
from ..core import FloatingRegionByRectangle, RegionByRectangle
from ..core.extract_text import OCRRegion
from ..core.fluent import AccessibilityRegionByRectangle
from .fluent import FloatingRegionBySelector, RegionBySelector
from .fluent.region import AccessibilityRegionBySelector
from .fluent.target_path import RegionLocator

if t.TYPE_CHECKING:
    from applitools.common import config as cfg
    from applitools.common import ultrafastgrid as ufg
    from applitools.core.fluent import region
    from applitools.selenium.fluent import selenium_check_settings as cs
    from applitools.selenium.fluent import target_path


class Enum(Field):
    def __init__(self, enum_type, *args, **kwargs):
        super(Enum, self).__init__(*args, **kwargs)
        self.enum_type = enum_type

    def _serialize(self, value, *_):
        # type: (t.Union[enum.Enum, t.Text], *t.Any) -> t.Optional[enum.Enum.value]
        if value is None:
            return None
        elif isinstance(value, self.enum_type):
            return value.value
        elif isinstance(value, enum.Enum):
            # robotframework library defines customized enums like RobotStitchMode
            # allow them but verify their values are matching
            return self.enum_type(value.value).value
        else:  # accept raw enum values but check their correctness
            return self.enum_type(value).value

    def _deserialize(self, value, *_):
        # type: (t.Any, *t.Any) -> t.Optional[enum.Enum]
        if value is None:
            return None
        else:
            return self.enum_type(value)


class Error(Field):
    def _deserialize(self, value, *_):
        # type: (dict, *t.Any) -> Exception
        return demarshal_error(value)


class DebugScreenshots(Field):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, config):
        # type: (t.Any, t.Any, cfg.Configuration) -> dict
        from .schema import DebugScreenshotHandler

        if config.save_debug_screenshots:
            return check_error(DebugScreenshotHandler().dump(config))


class EnvironmentField(Field):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, config):
        # type: (t.Any, t.Any, cfg.Configuration) -> dict
        from .schema import Environment

        return check_error(Environment().dump(config))


class VisualGridOptions(Field):
    def _serialize(self, value, *_):
        # type: (t.Optional[t.List[ufg.VisualGridOption]], *t.Any) -> t.Optional[dict]
        if value is not None:
            return {r.key: r.value for r in value}
        else:
            return None


class ElementReference(Dict):
    def _serialize(self, locator, _, __):
        # type: (t.Any, t.Any, target_path.TargetPathLocator) -> t.Optional[dict]
        return None if locator is None else locator.to_dict(self.context["registry"])


class FrameReference(Field):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, frame):
        # type: (t.Any, t.Any, cs.FrameLocator) -> t.Union[int, t.Text, dict]
        if frame.frame_index is not None:
            return frame.frame_index
        elif frame.frame_name_or_id is not None:
            return frame.frame_name_or_id
        else:
            return frame.frame_locator.to_dict(self.context["registry"])


class NormalizationField(Field):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, config):
        from .schema import Normalization

        return check_error(Normalization().dump(config))


class StitchOverlap(Field):
    def _serialize(self, value, *_):
        # type: (t.Any, int, *t.Any) -> dict
        if value is not None:
            return {"bottom": value}


class TargetReference(Field):
    _CHECK_ATTRIBUTE = False  # it might be target_locator or target_region

    def _serialize(self, _, __, check_settings):
        # type: (t.Any, t.Any, cs.SeleniumCheckSettingsValues) -> t.Optional[dict]
        if check_settings.target_locator:
            return check_settings.target_locator.to_dict(self.context["registry"])
        elif check_settings.target_region:
            from .schema import Region

            return check_error(Region().dump(check_settings.target_region))
        else:
            return None


class RegionReference(Field):
    _CHECK_ATTRIBUTE = False

    def _serialize(self, _, __, obj):
        # type: (t.Any, t.Any, t.Union[region.GetRegion, OCRRegion]) -> dict
        from .schema import Region

        if isinstance(
            obj,
            (RegionBySelector, FloatingRegionBySelector, AccessibilityRegionBySelector),
        ):
            return obj._target_path.to_dict(self.context["registry"])  # noqa
        elif isinstance(obj, RegionByRectangle):
            return check_error(Region().dump(obj._region))  # noqa
        elif isinstance(
            obj, (FloatingRegionByRectangle, AccessibilityRegionByRectangle)
        ):
            return check_error(Region().dump(obj._rect))  # noqa
        elif isinstance(obj, OCRRegion):
            if isinstance(obj.target, RegionLocator):
                return obj.target.to_dict(self.context["registry"])
            else:
                return check_error(Region().dump(obj.target))
        else:
            raise RuntimeError("Unexpected region type", type(obj))


class BrowserInfo(Field):
    def _serialize(self, value, *_):
        # type: (ufg.IRenderBrowserInfo, *t.Any) -> dict
        if isinstance(value, DesktopBrowserInfo):
            from .schema import DesktopBrowserRenderer

            return check_error(DesktopBrowserRenderer().dump(value))
        elif isinstance(value, ChromeEmulationInfo):
            from .schema import ChromeEmulationRenderer

            return {
                "chromeEmulationInfo": check_error(
                    ChromeEmulationRenderer().dump(value)
                )
            }
        elif isinstance(value, AndroidDeviceInfo):
            from .schema import AndroidDeviceRenderer

            return {
                "androidDeviceInfo": check_error(AndroidDeviceRenderer().dump(value))
            }
        elif isinstance(value, IosDeviceInfo):
            from .schema import IosDeviceRenderer

            return {"iosDeviceInfo": check_error(IosDeviceRenderer().dump(value))}
        else:
            raise RuntimeError("Unexpected BrowserInfo type", type(value))

    def _deserialize(self, value, *_):
        # type: (t.Optional[dict], *t.Any) -> t.Optional[ufg.IRenderBrowserInfo]
        if value is None:
            return None
        elif "iosDeviceInfo" in value:
            from .schema import IosDeviceRenderer

            return check_error(IosDeviceRenderer().load(value["iosDeviceInfo"]))
        elif "androidDeviceInfo" in value:
            from .schema import AndroidDeviceRenderer

            return check_error(AndroidDeviceRenderer().load(value["androidDeviceInfo"]))
        elif "chromeEmulationInfo" in value:
            from .schema import ChromeEmulationRenderer

            return check_error(
                ChromeEmulationRenderer().load(value["chromeEmulationInfo"])
            )
        else:
            from .schema import DesktopBrowserRenderer

            return check_error(DesktopBrowserRenderer().load(value))


def check_error(marshmellow_result):
    # type: (t.Tuple[t.Any, t.List[dict]]) -> t.Any
    result, errors = marshmellow_result
    if errors:
        raise RuntimeError("Internal serialization error", errors)
    else:
        return result


def demarshal_error(error_dict):
    # type: (dict) -> Exception
    message = error_dict["message"]
    if message.startswith("stale element reference"):
        return StaleElementReferenceException(message)
    elif error_dict.get("reason") in _matching_failures:
        return _matching_failures[error_dict["reason"]](message)
    else:
        stack = error_dict["stack"]
        if message:  # Sometimes when internal error occurs the message is empty
            # There is usually a copy of message in stack trace too, remove it
            stack = stack.split(message)[-1].strip("\n")
        return USDKFailure(message, stack)


_matching_failures = {
    "test different": DiffsFoundError,
    "test failed": TestFailedError,
    "test new": NewTestError,
}

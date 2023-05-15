from base64 import b64encode
from typing import TYPE_CHECKING, ByteString, Optional, Text, Union, overload

import attr
from six import PY2, BytesIO, binary_type, string_types

from applitools.selenium.fluent import SeleniumCheckSettings
from applitools.selenium.fluent.selenium_check_settings import (
    SeleniumCheckSettingsValues,
)

from .optional_deps import Image, PathLike, fspath

if TYPE_CHECKING:
    from applitools.common import Region


@attr.s
class ImagesCheckSettingsValues(SeleniumCheckSettingsValues):
    image = attr.ib(default=None)  # type: Optional[Text]
    dom = attr.ib(default=None)  # type: Optional[Text]


@attr.s
class ImagesCheckSettings(SeleniumCheckSettings):
    values = attr.ib(
        factory=ImagesCheckSettingsValues
    )  # type: ImagesCheckSettingsValues

    def with_dom(self, dom):
        # type: (Text) -> ImagesCheckSettings
        """
        Attach given DOM source text to the image.
        Needed by the Root Cause Analysis tool
        """
        self.values.dom = dom
        return self


class Target(object):
    """
    Target for an eyes.check_window/region.
    """

    @staticmethod  # noqa
    @overload
    def image(image):
        # type: (Image) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    @overload
    def image(image):
        # type: (ByteString) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    @overload
    def image(path):
        # type: (Union[Text, PathLike]) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    def image(image_or_path):
        check_settings = ImagesCheckSettings()
        check_settings.values.image = image_path_or_bytes(image_or_path)
        return check_settings

    @staticmethod  # noqa
    @overload
    def region(image, rect):
        # type: (Image, Region) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    @overload
    def region(image, rect):
        # type: (ByteString, Region) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    @overload
    def region(path, rect):
        # type: (Union[Text, PathLike], Region) -> ImagesCheckSettings
        pass

    @staticmethod  # noqa
    def region(image_or_path, rect):
        check_settings = Target.image(image_or_path)
        check_settings.values.target_region = rect
        return check_settings


def image_path_or_bytes(image_or_path):
    # type: (Union[ByteString, Image, Text, PathLike]) -> Text
    if not PY2 and isinstance(image_or_path, binary_type):
        image_bytes = b64encode(image_or_path)
        return image_bytes.decode("utf-8")
    elif isinstance(image_or_path, PathLike):
        return fspath(image_or_path)
    elif isinstance(image_or_path, Image):
        image_bytes = BytesIO()
        image_or_path.save(image_bytes, format="PNG")
        image_bytes = b64encode(image_bytes.getvalue())
        return image_bytes.decode("utf-8")
    elif isinstance(image_or_path, string_types):
        return image_or_path
    else:
        raise ValueError("Invalid image type", type(image_or_path))

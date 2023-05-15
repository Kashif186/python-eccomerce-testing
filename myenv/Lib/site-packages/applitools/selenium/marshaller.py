from typing import TYPE_CHECKING

from .schema import (
    CheckSettings,
    CloseBatchSettings,
    CloseSettings,
    DeleteTestSettings,
    ECClientSettings,
    ExtractTextSettings,
    EyesConfig,
    ImageTarget,
    LocateSettings,
    OCRSearchSettings,
    OpenSettings,
    Size,
)
from .schema_fields import check_error

if TYPE_CHECKING:
    from typing import List, Tuple

    from .. import common
    from ..common import config as cfg
    from ..common import target as t
    from ..common.utils.custom_types import ViewPort
    from ..core import ec_client_settings, extract_text, locators
    from ..core.batch_close import _EnabledBatchClose  # noqa
    from .fluent import selenium_check_settings as cs
    from .object_registry import ObjectRegistry
    from .optional_deps import WebDriver


class Marshaller(object):
    def __init__(self, object_registry):
        # type: (ObjectRegistry) -> None
        self._object_registry = object_registry
        self._sa = dict(context={"registry": object_registry})

    def marshal_viewport_size(self, viewport_size):
        # type: (ViewPort) -> dict
        return check_error(Size(**self._sa).dump(viewport_size))

    def marshal_webdriver_ref(self, driver):
        # type: (WebDriver) -> dict
        return self._object_registry.marshal_driver(driver)

    def marshal_ec_client_settings(self, client_settings):
        # type: (ec_client_settings.ECClientSettings) -> dict
        return check_error(ECClientSettings().dump(client_settings))

    def marshal_enabled_batch_close(self, close_batches):
        # type: (_EnabledBatchClose) -> dict
        return check_error(CloseBatchSettings(**self._sa).dump(close_batches))

    def marshal_delete_test_settings(self, test_results):
        # type: (common.TestResults) -> dict
        return check_error(DeleteTestSettings(**self._sa).dump(test_results))

    def marshal_configuration(self, configuration):
        # type: (cfg.Configuration) -> dict
        open = check_error(OpenSettings(**self._sa).dump(configuration))
        config = check_error(EyesConfig(**self._sa).dump(configuration))
        close = check_error(CloseSettings(**self._sa).dump(configuration))
        return {"open": open, "screenshot": config, "check": config, "close": close}

    def marshal_check_settings(self, check_settings):
        # type: (cs.SeleniumCheckSettings) -> dict
        return check_error(CheckSettings(**self._sa).dump(check_settings.values))

    def marshal_image_target(self, image_target):
        # type: (t.ImageTarget) -> dict
        return check_error(ImageTarget(**self._sa).dump(image_target))

    def marshal_locate_settings(self, locate_settings):
        # type: (locators.VisualLocatorSettings) -> dict
        return check_error(LocateSettings(**self._sa).dump(locate_settings.values))

    def marshal_ocr_extract_settings(self, extract_settings):
        # type: (Tuple[extract_text.OCRRegion, ...]) -> List[dict]
        return [
            check_error(ExtractTextSettings(**self._sa).dump(s))
            for s in extract_settings
        ]

    def marshal_ocr_search_settings(self, search_settings):
        # type: (extract_text.TextRegionSettings) -> dict
        return check_error(OCRSearchSettings(**self._sa).dump(search_settings))

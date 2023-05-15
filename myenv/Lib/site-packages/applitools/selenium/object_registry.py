from typing import TYPE_CHECKING

from ..common.object_registry import ObjectRegistry

if TYPE_CHECKING:
    from .optional_deps import WebDriver, WebElement


class SeleniumWebdriverObjectRegistry(ObjectRegistry):
    def marshal_driver(self, driver):
        # type: (WebDriver) -> dict
        return {
            "sessionId": driver.session_id,
            "serverUrl": driver.command_executor._url,
            "capabilities": driver.capabilities,
        }

    def marshal_element(self, element):
        # type: (WebElement) -> dict
        return {"elementId": element._id}

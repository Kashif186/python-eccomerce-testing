from __future__ import absolute_import


def is_list_or_tuple(elm):
    return isinstance(elm, (list, tuple))


def is_webelement(elm):
    from applitools.playwright.optional_deps import ElementHandle, PlaywrightLocator
    from applitools.selenium.optional_deps import (
        AppiumWebElement,
        EventFiringWebElement,
        WebElement,
    )

    return isinstance(
        elm,
        (
            WebElement,
            AppiumWebElement,
            EventFiringWebElement,
            PlaywrightLocator,
            ElementHandle,
        ),
    )

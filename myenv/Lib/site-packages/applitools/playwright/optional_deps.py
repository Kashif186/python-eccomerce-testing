try:
    from playwright.sync_api import ElementHandle
    from playwright.sync_api import Locator as PlaywrightLocator
    from playwright.sync_api import Page
except ImportError:

    class PlaywrightNotInstalled(object):
        """Please install playwright package to use this functionality"""

    Page = PlaywrightNotInstalled
    PlaywrightLocator = PlaywrightNotInstalled
    ElementHandle = PlaywrightNotInstalled

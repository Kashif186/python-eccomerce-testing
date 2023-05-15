from __future__ import absolute_import

from applitools.selenium import runner as selenium_runner
from applitools.selenium.runner import RunnerOptions  # noqa

from .protocol import PlaywrightSpecDriver


class ClassicRunner(selenium_runner.ClassicRunner):
    BASE_AGENT_ID = "eyes.playwright.python"
    Protocol = PlaywrightSpecDriver


class VisualGridRunner(selenium_runner.VisualGridRunner):
    BASE_AGENT_ID = "eyes.playwright.visualgrid.python"
    Protocol = PlaywrightSpecDriver

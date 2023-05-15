from applitools.selenium import eyes as selenium_eyes

from .runner import ClassicRunner


class Eyes(selenium_eyes.Eyes):
    DefaultRunner = ClassicRunner

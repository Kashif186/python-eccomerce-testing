from copy import deepcopy
from typing import TYPE_CHECKING, List, Optional, Text, Tuple, Union, overload

import attr
from six import raise_from

from applitools.common.config import Configuration as ConfigurationBase
from applitools.common.ultrafastgrid import (
    AndroidDeviceInfo,
    ChromeEmulationInfo,
    DesktopBrowserInfo,
    IosDeviceInfo,
    IRenderBrowserInfo,
    RenderBrowserInfo,
    ScreenOrientation,
    VisualGridOption,
)
from applitools.common.utils import argument_guard
from applitools.common.validators import is_list_or_tuple

from .misc import BrowserType, StitchMode

if TYPE_CHECKING:
    from applitools.common.ultrafastgrid import DeviceName
    from applitools.core.cut import CutProvider

__all__ = ("Configuration",)


@attr.s
class Configuration(ConfigurationBase):
    force_full_page_screenshot = attr.ib(default=None)  # type: bool
    wait_before_screenshots = attr.ib(
        default=None,
    )  # type: Optional[int]  # ms
    stitch_mode = attr.ib(default=None)  # type: Optional[StitchMode]
    hide_scrollbars = attr.ib(default=None)  # type: bool
    hide_caret = attr.ib(default=None)  # type: Optional[bool]
    # Indicates that a mobile simulator is being used
    is_simulator = attr.ib(default=None)  # type: Optional[bool]

    # Rendering Configuration
    browsers_info = attr.ib(init=False, factory=list)  # type: List[IRenderBrowserInfo]
    visual_grid_options = attr.ib(
        default=None
    )  # type: Optional[Tuple[VisualGridOption]]
    disable_browser_fetching = attr.ib(default=None)  # type: Optional[bool]
    enable_cross_origin_rendering = attr.ib(default=None)  # type: Optional[bool]
    dont_use_cookies = attr.ib(default=None)  # type: Optional[bool]
    dont_close_batches = attr.ib(default=None)  # type: Optional[bool]
    layout_breakpoints = attr.ib(default=None)  # type: Optional[Union[bool, List[int]]]
    scale_ratio = attr.ib(default=None)  # type: Optional[float]
    cut_provider = attr.ib(default=None)  # type: Optional[CutProvider]
    rotation = attr.ib(default=None)  # type: Optional[int]

    def set_force_full_page_screenshot(self, force_full_page_screenshot):
        # type: (bool) -> Configuration
        self.force_full_page_screenshot = force_full_page_screenshot
        return self

    def set_wait_before_screenshots(self, wait_before_screenshots):
        # type: (int) -> Configuration
        self.wait_before_screenshots = wait_before_screenshots
        return self

    def set_stitch_mode(self, stitch_mode):
        # type: (StitchMode) -> Configuration
        self.stitch_mode = stitch_mode
        return self

    def set_hide_scrollbars(self, hide_scrollbars):
        # type: (bool) -> Configuration
        self.hide_scrollbars = hide_scrollbars
        return self

    def set_hide_caret(self, hide_caret):
        # type: (bool) -> Configuration
        self.hide_caret = hide_caret
        return self

    def set_visual_grid_options(self, *options):
        # type: (*VisualGridOption) -> Configuration
        if options == (None,):
            self.visual_grid_options = None
        else:
            argument_guard.are_(options, VisualGridOption)
            self.visual_grid_options = options
        return self

    def set_disable_browser_fetching(self, disable_browser_fetching):
        # type: (bool) -> Configuration
        self.disable_browser_fetching = disable_browser_fetching
        return self

    def set_enable_cross_origin_rendering(self, enable_cross_origin_rendering):
        # type: (bool) -> Configuration
        self.enable_cross_origin_rendering = enable_cross_origin_rendering
        return self

    def set_dont_use_cookies(self, dont_use_cookies):
        # type: (bool) -> Configuration
        self.dont_use_cookies = dont_use_cookies
        return self

    @overload
    def set_layout_breakpoints(self, enabled):
        # type: (bool) -> Configuration
        pass

    @overload
    def set_layout_breakpoints(self, *breakpoints):
        # type: (*int) -> Configuration
        pass

    def set_layout_breakpoints(self, enabled_or_first, *rest):
        if isinstance(enabled_or_first, bool):
            self.layout_breakpoints = enabled_or_first
        elif isinstance(enabled_or_first, int):
            self.layout_breakpoints = [enabled_or_first] + list(rest)
        else:
            raise TypeError(
                "{} is not an instance of bool or int".format(enabled_or_first)
            )
        return self

    @overload  # noqa
    def add_browser(self, desktop_browser_info):
        # type: (DesktopBrowserInfo) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, ios_device_info):
        # type: (IosDeviceInfo) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, chrome_emulation_info):
        # type: (ChromeEmulationInfo) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, width, height, browser_type):
        # type: (int, int, BrowserType) -> Configuration
        pass

    @overload  # noqa
    def add_browser(self, width, height, browser_type, baseline_env_name):
        # type: (int, int, BrowserType, Text) -> Configuration
        pass

    def add_browser(self, *args):  # noqa
        if isinstance(args[0], IRenderBrowserInfo):
            self.browsers_info.append(args[0])
        elif (
            isinstance(args[0], int)
            and isinstance(args[1], int)
            and isinstance(args[2], BrowserType)
        ):
            if len(args) == 4:
                baseline_env_name = args[3]
            else:
                baseline_env_name = self.baseline_env_name
            self.browsers_info.append(
                DesktopBrowserInfo(args[0], args[1], args[2], baseline_env_name)
            )
        else:
            raise TypeError(
                "Unsupported parameter: \n\ttype: {} \n\tvalue: {}".format(
                    type(args), args
                )
            )
        return self

    @overload
    def add_browsers(self, renders_info):
        # type:(List[Union[DesktopBrowserInfo,IosDeviceInfo,ChromeEmulationInfo]])->Configuration  # noqa
        pass

    @overload
    def add_browsers(self, renders_info):
        # type:(*Union[DesktopBrowserInfo,IosDeviceInfo,ChromeEmulationInfo])->Configuration
        pass

    def add_browsers(self, *renders_info):
        if len(renders_info) == 1 and is_list_or_tuple(renders_info[0]):
            renders_info = renders_info[0]

        for render_info in renders_info:
            try:
                self.add_browser(render_info)
            except TypeError as e:
                raise_from(TypeError("Wrong argument in .add_browsers()"), e)
        return self

    def add_device_emulation(self, device_name, orientation=ScreenOrientation.PORTRAIT):
        # type: (DeviceName, ScreenOrientation) -> Configuration
        argument_guard.not_none(device_name)
        self.add_browser(ChromeEmulationInfo(device_name, orientation))
        return self

    def add_mobile_device(self, mobile_device_info):
        # type: (Union[IosDeviceInfo, AndroidDeviceInfo]) -> Configuration
        return self.add_mobile_devices(mobile_device_info)

    def add_mobile_devices(self, *mobile_device_infos):
        # type: (*Union[IosDeviceInfo, AndroidDeviceInfo]) -> Configuration
        return self.add_browsers(*mobile_device_infos)

    def clone(self):
        # type: () -> Configuration
        # TODO: Remove this huck when get rid of Python2
        conf = super(Configuration, self).clone()
        conf.browsers_info = deepcopy(self.browsers_info)
        conf.visual_grid_options = deepcopy(self.visual_grid_options)
        return conf

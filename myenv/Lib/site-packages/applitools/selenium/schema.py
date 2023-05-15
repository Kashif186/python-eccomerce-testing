from __future__ import absolute_import

import typing as t

from marshmallow import Schema, post_dump, post_load
from marshmallow.fields import (
    Boolean,
    DateTime,
    Dict,
    Field,
    Float,
    Integer,
    List,
    Nested,
    String,
)
from marshmallow.schema import BaseSchema, SchemaMeta, with_metaclass

from applitools.core import extract_text

from .. import common
from ..common import (
    AccessibilityGuidelinesVersion,
    AccessibilityLevel,
    AccessibilityRegionType,
    AndroidDeviceName,
    AndroidVersion,
    DeviceName,
    IosDeviceName,
    IosVersion,
    MatchLevel,
    ScreenOrientation,
    SessionType,
    StitchMode,
)
from ..common.accessibility import AccessibilityStatus
from ..common.selenium import BrowserType
from ..common.test_results import TestResultsStatus
from .schema_fields import demarshal_error  # noqa
from .schema_fields import (
    BrowserInfo,
    DebugScreenshots,
    ElementReference,
    Enum,
    EnvironmentField,
    Error,
    FrameReference,
    NormalizationField,
    RegionReference,
    StitchOverlap,
    TargetReference,
    VisualGridOptions,
    check_error,
)

if t.TYPE_CHECKING:
    from applitools.common import config


# Default marshmallow.Schema has no option to skip attributes with None value
# or empty lists / dicts. Because it uses metaclass, it should be re-defined
# instead of simple subclassing
class USDKSchema(with_metaclass(SchemaMeta, BaseSchema)):
    __doc__ = BaseSchema.__doc__
    _always_skip_values = (None, [])
    _keep_empty_objects = ("lazyLoad",)  # fields that are allowed to have {} value

    @classmethod
    def should_keep(cls, key, value):
        # type: (t.Text, t.Any) -> bool
        if value in cls._always_skip_values:
            return False
        if value == {} and key not in cls._keep_empty_objects:
            return False
        return True

    @post_dump
    def remove_none_values_empty_lists(self, data, **_):
        # type: (dict, **t.Any) -> dict
        return {k: v for k, v in data.items() if self.should_keep(k, v)}


class Size(USDKSchema):
    width = Integer()
    height = Integer()


class DebugScreenshotHandler(USDKSchema):
    debug_screenshots_path = String(dump_to="path")
    debug_screenshots_prefix = String(dump_to="prefix")


class Environment(USDKSchema):
    host_os = String(dump_to="os")
    # osInfo
    host_app = String(dump_to="hostingApp")
    # hostingAppInfo
    # deviceName
    viewport_size = Nested(Size, dump_to="viewportSize")


class DesktopBrowserRenderer(USDKSchema):
    width = Float()
    height = Float()
    browser_type = Enum(BrowserType, dump_to="name", load_from="name")

    @post_load
    def to_python(self, data, **_):
        return common.DesktopBrowserInfo(**data)


class ChromeEmulationRenderer(USDKSchema):
    device_name = Enum(DeviceName, dump_to="deviceName", load_from="deviceName")
    screen_orientation = Enum(
        ScreenOrientation, dump_to="screenOrientation", load_from="screenOrientation"
    )

    @post_load
    def to_python(self, data, **_):
        return common.ChromeEmulationInfo(**data)


class AndroidDeviceRenderer(USDKSchema):
    device_name = Enum(AndroidDeviceName, dump_to="deviceName", load_from="deviceName")
    screen_orientation = Enum(
        ScreenOrientation, dump_to="screenOrientation", load_from="screenOrientation"
    )
    android_version = Enum(AndroidVersion, dump_to="version", load_from="version")

    @post_load
    def to_python(self, data, **_):
        return common.AndroidDeviceInfo(**data)


class IosDeviceRenderer(USDKSchema):
    device_name = Enum(IosDeviceName, dump_to="deviceName", load_from="deviceName")
    screen_orientation = Enum(
        ScreenOrientation, dump_to="screenOrientation", load_from="screenOrientation"
    )
    ios_version = Enum(IosVersion, dump_to="version", load_from="version")

    @post_load
    def to_python(self, data, **_):
        return common.IosDeviceInfo(**data)


class Region(USDKSchema):
    left = Float(dump_to="x", load_from="x")  # this allows both x and left when loading
    top = Float(dump_to="y", load_from="y")  # this allows both x and top when loading
    width = Float()
    height = Float()

    @post_load
    def to_python(self, data, **_):
        return common.geometry.Region.from_(data)


class Offset(USDKSchema):
    max_left_offset = Float(dump_to="left")
    max_up_offset = Float(dump_to="top")
    max_right_offset = Float(dump_to="right")
    max_down_offset = Float(dump_to="bottom")


class ContextReference(USDKSchema):
    frame = FrameReference()
    scroll_root_locator = ElementReference(dump_to="scrollRootElement")


class ImageCropRect(USDKSchema):
    header = Float(dump_to="top")
    right = Float()
    footer = Float(dump_to="bottom")
    left = Float()


class Normalization(USDKSchema):
    cut_provider = Nested(ImageCropRect, dump_to="cut")
    rotation = Integer()
    scale_ratio = Float(dump_to="scaleRatio")


class Batch(USDKSchema):
    id = String()
    name = String()
    sequence_name = String(dump_to="sequenceName")
    started_at = DateTime("%Y-%m-%dT%H:%M:%SZ", dump_to="startedAt")
    notify_on_completion = Boolean(dump_to="notifyOnCompletion")
    properties = List(Dict())


class Proxy(USDKSchema):
    url = String(required=True)
    username = String()
    password = String()


class ImageTarget(USDKSchema):
    image = String()
    dom = String()


class AccessibilitySettings(USDKSchema):
    level = Enum(AccessibilityLevel)
    guidelines_version = Enum(AccessibilityGuidelinesVersion, dump_to="version")


class CodedRegionReference(USDKSchema):
    region = RegionReference()
    padding = Field()
    region_id = String(dump_to="regionId")


class FloatingRegionReference(USDKSchema):
    _target_path = RegionReference(dump_to="region")
    _bounds = Nested(Offset(), dump_to="offset")


class AccessibilityRegionReference(USDKSchema):
    _target_path = RegionReference(dump_to="region")
    _type = Enum(AccessibilityRegionType, dump_to="type")


class LazyLoadOptions(USDKSchema):
    scroll_length = Integer(dump_to="scrollLength")
    waiting_time = Integer(dump_to="waitingTime")
    max_amount_to_scroll = Integer(dump_to="maxAmountToScroll")


class EyesConfig(USDKSchema):
    # region
    # frames
    force_full_page_screenshot = Boolean(dump_to="fully")
    # scrollRootElement
    stitch_mode = Enum(StitchMode, dump_to="stitchMode")
    hide_scrollbars = Boolean(dump_to="hideScrollbars")
    hide_caret = Boolean(dump_to="hideCaret")
    stitch_overlap = StitchOverlap(dump_to="overlap")
    wait_before_capture = Integer(dump_to="waitBeforeCapture")
    # lazyLoad
    ignore_displacements = Boolean(
        attribute="default_match_settings.ignore_displacements",
        dump_to="ignoreDisplacements",
    )
    # name
    # pageId
    ignore_regions = List(
        Nested(CodedRegionReference),
        attribute="default_match_settings.ignore_regions",
        dump_to="ignoreRegions",
    )
    layout_regions = List(
        Nested(CodedRegionReference),
        attribute="default_match_settings.layout_regions",
        dump_to="layoutRegions",
    )

    strict_regions = List(
        Nested(CodedRegionReference),
        attribute="default_match_settings.strict_regions",
        dump_to="strictRegions",
    )
    content_regions = List(
        Nested(CodedRegionReference),
        attribute="default_match_settings.content_regions",
        dump_to="contentRegions",
    )
    floating_match_settings = List(
        Nested(FloatingRegionReference),
        attribute="default_match_settings.floating_match_settings",
        dump_to="floatingRegions",
    )
    accessibility = List(
        Nested(AccessibilityRegionReference),
        attribute="default_match_settings.accessibility",
        dump_to="accessibilityRegions",
    )
    accessibility_settings = Nested(
        AccessibilitySettings,
        attribute="default_match_settings.accessibility_settings",
        dump_to="accessibilitySettings",
    )

    match_level = Enum(
        MatchLevel, attribute="default_match_settings.match_level", dump_to="matchLevel"
    )
    send_dom = Boolean(dump_to="sendDom")
    use_dom = Boolean(attribute="default_match_settings.use_dom", dump_to="useDom")
    enable_patterns = Boolean(
        attribute="default_match_settings.enable_patterns", dump_to="enablePatterns"
    )
    ignore_caret = Boolean(
        attribute="default_match_settings.ignore_caret", dump_to="ignoreCaret"
    )
    # enablePatterns
    # ignoreCaret
    visual_grid_options = VisualGridOptions(dump_to="ufgOptions")
    layout_breakpoints = Field(dump_to="layoutBreakpoints")
    disable_browser_fetching = Boolean(dump_to="disableBrowserFetching")
    match_timeout = Float(dump_to="retryTimeout")
    browsers_info = List(BrowserInfo(), dump_to="renderers")
    # autProxy
    normalization = NormalizationField()
    debug_images = DebugScreenshots(dump_to="debugImages")

    # wait_before_screenshots = Float(dump_to="waitBeforeScreenshots")


class OpenSettings(USDKSchema):
    is_disabled = Boolean(dump_to="isDisabled")
    server_url = String(dump_to="serverUrl")
    api_key = String(dump_to="apiKey")
    proxy = Nested(Proxy)
    _timeout = Integer(dump_to="connectionTimeout")
    # removeSession
    agent_id = String(dump_to="agentId")
    app_name = String(dump_to="appName")
    test_name = String(dump_to="testName")
    # displayName
    user_test_id = String(dump_to="userTestId")
    session_type = Enum(SessionType, dump_to="sessionType")
    properties = List(Dict())
    batch = Nested(Batch)
    dont_close_batches = Boolean(dump_to="keepBatchOpen")
    environment_name = String(dump_to="environmentName")
    environment = EnvironmentField()
    branch_name = String(dump_to="branchName")
    parent_branch_name = String(dump_to="parentBranchName")
    baseline_env_name = String(dump_to="baselineEnvName")
    baseline_branch_name = String(dump_to="baselineBranchName")
    # compareWithParentBranch
    # ignoreBaseline
    # ignoreGitBranching
    save_diffs = Boolean(dump_to="saveDiffs")
    # abortIdleTestTimeout


class CheckSettings(USDKSchema):
    name = String()
    disable_browser_fetching = Boolean(dump_to="disableBrowserFetching")
    layout_breakpoints = Field(dump_to="layoutBreakpoints")
    visual_grid_options = VisualGridOptions(dump_to="ufgOptions")
    script_hooks = Dict(dump_to="hooks")
    page_id = String(dump_to="pageId")
    variation_group_id = String(dump_to="userCommandId")
    timeout = Integer(dump_to="retryTimeout")
    wait_before_capture = Integer(dump_to="waitBeforeCapture")
    lazy_load = Nested(LazyLoadOptions, dump_to="lazyLoad")
    # ScreenshotSettings
    region = TargetReference()
    frame_chain = List(Nested(ContextReference), dump_to="frames")
    scroll_root_locator = ElementReference(dump_to="scrollRootElement")
    stitch_content = Boolean(dump_to="fully")
    # MatchSettings
    match_level = Enum(MatchLevel, dump_to="matchLevel")
    send_dom = Boolean(dump_to="sendDom")
    use_dom = Boolean(dump_to="useDom")
    enable_patterns = Boolean(dump_to="enablePatterns")
    ignore_caret = Boolean(dump_to="ignoreCaret")
    ignore_displacements = Boolean(dump_to="ignoreDisplacements")
    ignore_regions = List(Nested(CodedRegionReference), dump_to="ignoreRegions")
    layout_regions = List(Nested(CodedRegionReference), dump_to="layoutRegions")
    strict_regions = List(Nested(CodedRegionReference), dump_to="strictRegions")
    content_regions = List(Nested(CodedRegionReference), dump_to="contentRegions")
    floating_regions = List(Nested(FloatingRegionReference), dump_to="floatingRegions")
    accessibility_regions = List(
        Nested(AccessibilityRegionReference), dump_to="accessibilityRegions"
    )
    webview = Field()


class LocateSettings(USDKSchema):
    names = List(String(), dump_to="locatorNames")
    first_only = Boolean(dump_to="firstOnly")


class OCRSearchSettings(USDKSchema):
    _patterns = List(String(), dump_to="patterns")
    _ignore_case = Boolean(dump_to="ignoreCase")
    _first_only = Boolean(dump_to="firstOnly")
    _language = String(dump_to="language")


class ExtractTextSettings(USDKSchema):
    target = RegionReference(dump_to="region")
    _hint = String(dump_to="hint")
    _min_match = Float(dump_to="minMatch")
    _language = String(dump_to="language")


class CloseSettings(USDKSchema):
    # raise_ex = Boolean(dump_to="throwErr")  # not present in config
    save_new_tests = Boolean(dump_to="updateBaselineIfNew")
    save_failed_tests = Boolean(dump_to="updateBaselineIfDifferent")


class CloseBatchSettings(USDKSchema):
    batch_id = String(dump_to="batchId")
    server_url = String(dump_to="serverUrl")
    api_key = String(dump_to="apiKey")
    proxy = Nested(Proxy)


class DeleteTestSettings(USDKSchema):
    id = String(dump_to="testId")
    batch_id = String(dump_to="batchId")
    secret_token = String(dump_to="secretToken")
    server_url = String(attribute="_connection_config.server_url", dump_to="serverUrl")
    api_key = String(attribute="_connection_config.api_key", dump_to="apiKey")
    proxy = Nested(Proxy, attribute="_connection_config.proxy")


class ECClientCapabilities(USDKSchema):
    server_url = String(dump_to="serverUrl")
    api_key = String(dump_to="apiKey")


class ECClientSettings(USDKSchema):
    capabilities = Nested(ECClientCapabilities)
    proxy = Nested(Proxy)


# De-marshaling schema
class RectangleSize(Schema):
    width = Integer()
    height = Integer()

    @post_load
    def to_python(self, data, **_):
        return common.RectangleSize(**data)


class ServerInfo(Schema):
    logs_dir = String(load_from="logsDir")

    @post_load
    def to_python(self, data, **_):
        return common.ServerInfo(**data)


class SessionUrls(Schema):
    batch = String()
    session = String()

    @post_load
    def to_python(self, data, **_):
        return common.test_results.SessionUrls(**data)


class ApiUrls(Schema):
    baseline_image = String(load_from="baselineImage")
    current_image = String(load_from="currentImage")
    diff_image = String(load_from="diffImage")
    checkpoint_image = String(load_from="checkpointImage")
    checkpoint_image_thumbnail = String(load_from="checkpointImageThumbnail")

    @post_load
    def to_python(self, data, **_):
        return common.test_results.StepInfo.ApiUrls(**data)


class AppUrls(Schema):
    step = String(load_from="step")
    step_editor = String(load_from="stepEditor")

    @post_load
    def to_python(self, data, **_):
        return common.test_results.StepInfo.AppUrls(**data)


class SessionAccessibilityStatus(Schema):
    level = Enum(AccessibilityLevel)
    version = Enum(AccessibilityGuidelinesVersion)
    status = Enum(AccessibilityStatus)

    @post_load
    def to_python(self, data, **_):
        return common.accessibility.SessionAccessibilityStatus(**data)


class StepInfo(Schema):
    name = String()
    is_different = Boolean(load_from="isDifferent")
    has_baseline_image = Boolean(load_from="hasBaselineImage")
    has_current_image = Boolean(load_from="hasCurrentImage")
    has_checkpoint_image = Boolean(load_from="hasCheckpointImage")
    api_urls = Nested(ApiUrls, load_from="apiUrls")
    app_urls = Nested(AppUrls, load_from="appUrls")

    @post_load
    def to_python(self, data, **_):
        return common.test_results.StepInfo(**data)


class MatchResult(Schema):
    as_expected = Boolean(load_from="asExpected")
    window_id = String(load_from="windowId")

    @post_load
    def to_python(self, data, **_):
        return common.MatchResult(**data)


class LocateTextResponse(Schema):
    left = Integer(load_from="x")
    top = Integer(load_from="y")
    width = Integer()
    height = Integer()
    text = String()

    @post_load
    def to_python(self, data, **_):
        return extract_text.TextRegion(**data)


class TestResults(Schema):
    steps = Integer()
    matches = Integer()
    mismatches = Integer()
    missing = Integer()
    exact_matches = Integer(load_from="exactMatches")
    strict_matches = Integer(load_from="strictMatches")
    content_matches = Integer(load_from="contentMatches")
    layout_matches = Integer(load_from="layoutMatches")
    none_matches = Integer(load_from="noneMatches")
    is_new = Boolean(load_from="isNew")
    url = String()
    status = Enum(TestResultsStatus)
    name = String()
    secret_token = String(load_from="secretToken")
    id = String()
    app_name = String(load_from="appName")
    batch_name = String(load_from="batchName")
    batch_id = String(load_from="batchId")
    branch_name = String(load_from="branchName")
    host_os = String(load_from="hostOS")
    host_app = String(load_from="hostApp")
    host_display_size = Nested(RectangleSize, load_from="hostDisplaySize")
    started_at = String(load_from="startedAt")
    duration = Integer()
    is_different = Boolean(load_from="isDifferent")
    is_aborted = Boolean(load_from="isAborted")
    is_empty = Boolean(load_from="isEmpty")
    app_urls = Nested(SessionUrls, load_from="appUrls")
    api_urls = Nested(SessionUrls, load_from="apiUrls")
    steps_info = List(Nested(StepInfo), load_from="stepsInfo")
    baseline_id = String(load_from="baselineId")
    accessibility_status = Nested(
        SessionAccessibilityStatus, load_from="accessibilityStatus"
    )
    user_test_id = String(load_from="userTestId")

    @post_load
    def to_python(self, data, **_):
        return common.TestResults(**data)


class TestResultContainer(Schema):
    test_results = Nested(TestResults, load_from="result")
    browser_info = BrowserInfo(load_from="renderer")
    exception = Error(allow_none=True, load_from="error")
    user_test_id = String(load_from="userTestId")

    @post_load
    def to_python(self, data, **_):
        return common.TestResultContainer(**data)


class TestResultsSummary(Schema):
    results = List(Nested(TestResultContainer))
    exceptions = Integer()
    passed = Integer()
    unresolved = Integer()
    failed = Integer()
    # these attributes get None value when Eyes.locate call fails
    mismatches = Integer(allow_none=True)
    missing = Integer(allow_none=True)
    matches = Integer(allow_none=True)

    @post_load
    def to_python(self, data, **_):
        return common.TestResultsSummary(**data)


def demarshal_match_result(results_dict):
    # type: (dict) -> MatchResult
    return check_error(MatchResult().load(results_dict))


def demarshal_locate_result(results):
    # type: (dict) -> t.Dict[t.Text, t.List[common.Region]]
    return {
        locator_id: [check_error(Region().load(r)) for r in regions] if regions else []
        for locator_id, regions in results.items()
    }


def demarshal_locate_text_result(results):
    # type: (dict) -> t.Dict[t.Text, t.List[extract_text.TextRegion]]
    return {
        locator_id: [check_error(LocateTextResponse().load(r)) for r in regions]
        if regions
        else []
        for locator_id, regions in results.items()
    }


def demarshal_test_results(results_list, conf):
    # type: (t.List[dict], config.Configuration) -> t.List[common.TestResults]
    # When locating visual locators, result might be None
    results = [check_error(TestResults().load(r)) for r in results_list if r]
    for result in results:
        result.set_connection_config(conf.server_url, conf.api_key, conf.proxy)
    return results


def demarshal_close_manager_results(close_manager_result_dict, conf):
    # type: (dict, config.Configuration) -> common.TestResultsSummary
    results = check_error(TestResultsSummary().load(close_manager_result_dict))
    for container in results:
        if container.test_results:
            container.test_results.set_connection_config(
                conf.server_url, conf.api_key, conf.proxy
            )
    return results


def demarshal_server_info(info_dict):
    # type: (dict) -> common.ServerInfo
    return check_error(ServerInfo().load(info_dict))

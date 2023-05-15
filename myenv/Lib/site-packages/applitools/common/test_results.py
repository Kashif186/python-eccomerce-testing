from __future__ import absolute_import

from collections import namedtuple
from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Text, Tuple

import attr

from .accessibility import SessionAccessibilityStatus
from .geometry import RectangleSize
from .match import ImageMatchSettings
from .ultrafastgrid import RenderBrowserInfo

if TYPE_CHECKING:
    from . import ProxySettings

__all__ = (
    "TestResults",
    "TestResultsStatus",
    "TestResultsSummary",
    "TestResultContainer",
)

ConnectionConfig = namedtuple("ConnectionConfig", "server_url api_key proxy")


class TestResultsStatus(Enum):
    """
    Status values for tests results.
    """

    Passed = "Passed"
    Unresolved = "Unresolved"
    Failed = "Failed"

    __test__ = False  # avoid warnings in test frameworks


@attr.s
class SessionUrls(object):
    batch = attr.ib(default=None)  # type: Text
    session = attr.ib(default=None)  # type: Text


@attr.s
class StepInfo(object):
    @attr.s(repr_ns="StepInfo")
    class AppUrls(object):
        step = attr.ib(default=None)  # type: Text
        step_editor = attr.ib(default=None)  # type: Text

    @attr.s(repr_ns="StepInfo")
    class ApiUrls(object):
        baseline_image = attr.ib(default=None)  # type: Text
        current_image = attr.ib(default=None)  # type: Text
        diff_image = attr.ib(default=None)  # type: Text
        checkpoint_image = attr.ib(default=None)  # type: Text
        checkpoint_image_thumbnail = attr.ib(default=None)  # type: Text

    name = attr.ib(default=None)  # type: Text
    is_different = attr.ib(default=None)  # type: bool
    has_baseline_image = attr.ib(default=None)  # type: bool
    has_current_image = attr.ib(default=None)  # type: bool
    has_checkpoint_image = attr.ib(default=None)  # type: bool
    api_urls = attr.ib(default=None, type=ApiUrls)  # type: ApiUrls
    app_urls = attr.ib(default=None, type=AppUrls)  # type: AppUrls


@attr.s
class TestResults(object):
    """
    Eyes test results.
    """

    steps = attr.ib(default=0)  # type: int
    matches = attr.ib(default=0)  # type: int
    mismatches = attr.ib(default=0)  # type: int
    missing = attr.ib(default=0)  # type: int
    exact_matches = attr.ib(default=0, repr=False)  # type: int
    strict_matches = attr.ib(default=0, repr=False)  # type: int
    content_matches = attr.ib(default=0, repr=False)  # type: int
    layout_matches = attr.ib(default=0, repr=False)  # type: int
    none_matches = attr.ib(default=0, repr=False)  # type: int
    is_new = attr.ib(default=None, repr=False)  # type: Optional[bool]

    url = attr.ib(default=None)  # type: Optional[Text]
    status = attr.ib(
        converter=lambda v: TestResultsStatus(v) if v else None,
        type=TestResultsStatus,
        default=None,
        repr=False,
    )  # type: Optional[TestResultsStatus]

    name = attr.ib(default=None, repr=False)  # type: Text
    secret_token = attr.ib(default=None, repr=False)  # type: Text
    id = attr.ib(default=None, repr=False)  # type: Text
    app_name = attr.ib(default=None, repr=False)  # type: Text
    batch_name = attr.ib(default=None, repr=False)  # type: Text
    batch_id = attr.ib(default=None, repr=False)  # type: Text
    branch_name = attr.ib(default=None, repr=False)  # type: Text
    host_os = attr.ib(default=None, repr=False)  # type: Text
    host_app = attr.ib(default=None, repr=False)  # type: Text
    host_display_size = attr.ib(
        default=None, repr=False, type=RectangleSize
    )  # type: RectangleSize
    started_at = attr.ib(default=None, repr=False)  # type: Text
    duration = attr.ib(default=None, repr=False)  # type: int
    is_different = attr.ib(default=None, repr=False)  # type: bool
    is_aborted = attr.ib(default=None, repr=False)  # type: bool
    is_empty = attr.ib(default=None, repr=False)  # type: bool
    app_urls = attr.ib(default=None, repr=False, type=SessionUrls)  # type: SessionUrls
    api_urls = attr.ib(default=None, repr=False, type=SessionUrls)  # type: SessionUrls
    steps_info = attr.ib(
        default=None, repr=False, type=StepInfo
    )  # type: List[StepInfo]
    baseline_id = attr.ib(default=None, repr=False)  # type: Text
    default_match_settings = attr.ib(
        default=None, repr=False, type=ImageMatchSettings
    )  # type: ImageMatchSettings
    accessibility_status = attr.ib(
        default=None, type=SessionAccessibilityStatus
    )  # type: SessionAccessibilityStatus
    user_test_id = attr.ib(default=None)  # type: Optional[Text]
    _connection_config = attr.ib(
        default=(None, None, None), eq=False, order=False, repr=False
    )  # type: Tuple[Optional[Text], Optional[Text], Optional[ProxySettings]]
    __test__ = False  # avoid warnings in test frameworks

    @property
    def is_passed(self):
        # type: () -> bool
        return self.status == TestResultsStatus.Passed

    @property
    def is_unresolved(self):
        # type: () -> bool
        return self.status == TestResultsStatus.Unresolved

    @property
    def is_failed(self):
        # type: () -> bool
        return self.status == TestResultsStatus.Failed

    def set_connection_config(self, server_url, api_key, proxy_settings):
        # type: (Text, Text, Optional[ProxySettings]) -> None
        self._connection_config = ConnectionConfig(server_url, api_key, proxy_settings)

    def delete(self):
        # type: () -> None
        from applitools.selenium.__version__ import __version__
        from applitools.selenium.command_executor import CommandExecutor
        from applitools.selenium.eyes import EyesRunner

        cmd = CommandExecutor.get_instance(
            EyesRunner.Protocol, EyesRunner.BASE_AGENT_ID, __version__
        )
        cmd.core_delete_test(self)


@attr.s(repr=False, str=False)
class TestResultContainer(object):
    test_results = attr.ib(default=None, type=TestResults)  # type: TestResults
    browser_info = attr.ib(default=None)  # type: Optional[RenderBrowserInfo]
    exception = attr.ib(default=None)  # type: Optional[Exception]
    user_test_id = attr.ib(default=None)  # type: Optional[Text]
    __test__ = False  # avoid warnings in test frameworks

    def __str__(self):
        browser_info = (
            "\n browser_info = {}".format(self.browser_info)
            if self.browser_info
            else ""
        )
        return (
            "TestResultContainer{{"
            "\n test_results = {test_results}"
            "{browser_info}"
            "\n exception = {exception}"
            "}}".format(
                test_results=self.test_results,
                browser_info=browser_info,
                exception=self.exception,
            )
        )


@attr.s(repr=False, str=False)
class TestResultsSummary(object):
    results = attr.ib(
        factory=list, type=TestResultContainer
    )  # type: List[TestResultContainer]
    exceptions = attr.ib(default=0)  # type: int
    passed = attr.ib(default=0)  # type: int
    unresolved = attr.ib(default=0)  # type: int
    failed = attr.ib(default=0)  # type: int
    mismatches = attr.ib(default=0)  # type: int
    missing = attr.ib(default=0)  # type: int
    matches = attr.ib(default=0)  # type: int
    __test__ = False  # avoid warnings in test frameworks

    @property
    def all_results(self):
        # type: () -> List[TestResultContainer]
        return self.results

    def size(self):
        # type: () -> int
        return len(self)

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return iter(self.results)

    def __getitem__(self, item):
        # type: (int) -> TestResultContainer
        return self.results[item]

    def __str__(self):
        return """
result summary {{
    all results={all_results}
    passed={passed}
    unresolved={unresolved}
    failed={failed}
    exceptions={exceptions}
    mismatches={mismatches}
    missing={missing}
    matches={matches}
}}""".format(
            all_results="\n".join(map(str, self.results)),
            passed=self.passed,
            unresolved=self.unresolved,
            failed=self.failed,
            exceptions=self.exceptions,
            mismatches=self.mismatches,
            missing=self.missing,
            matches=self.matches,
        )

from typing import TYPE_CHECKING

import attr

if TYPE_CHECKING:
    from typing import Optional, Text

    from applitools.common import ProxySettings


@attr.s
class ECClientCapabilities(object):
    api_key = attr.ib(default=None)  # type: Optional[Text]
    server_url = attr.ib(default=None)  # type: Optional[Text]


@attr.s
class ECClientSettings(object):
    capabilities = attr.ib(type=ECClientCapabilities)  # type: ECClientCapabilities
    proxy = attr.ib(default=None)  # type: Optional[ProxySettings]

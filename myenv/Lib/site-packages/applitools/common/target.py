from typing import TYPE_CHECKING

import attr

if TYPE_CHECKING:
    from typing import Optional, Text


@attr.s
class ImageTarget(object):
    image = attr.ib(default=None)  # type: Optional[Text]
    dom = attr.ib(default=None)  # type: Optional[Text]

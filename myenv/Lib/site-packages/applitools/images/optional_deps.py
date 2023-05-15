from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Text

    from six import BytesIO, binary_type

try:
    from os import PathLike, fspath
except ImportError:

    class PathLike(object):
        """Dummy class to avoid conditions in Target methods"""

    def fspath(_):
        """Dummy function to avoid conditions in Target methods"""


try:
    from PIL.Image import Image
except ImportError:

    class Image(object):
        """Dummy class to avoid conditions in Target methods"""

        def __init__(self):
            raise RuntimeError("Please install pillow package if you need Image class.")

        def save(self, _, __):
            # type: (BytesIO, Text) -> binary_type
            raise RuntimeError("Please install pillow package if you need Image class.")

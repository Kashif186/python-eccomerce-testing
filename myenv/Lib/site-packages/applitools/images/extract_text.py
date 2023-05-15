from typing import List, Optional, Text, Union

from applitools.common import Region
from applitools.core import TextRegionSettings as TextRegionSettingsBase
from applitools.core.extract_text import OCRRegion as BaseOCRRegion

from .fluent import Image, image_path_or_bytes


class OCRRegion(BaseOCRRegion):
    def __init__(self, image, region_in_image=None):
        # type: (Union[Image, Text], Optional[Region]) -> None
        super(OCRRegion, self).__init__(region_in_image)
        self.image = image_path_or_bytes(image)


class TextRegionSettings(TextRegionSettingsBase):
    def __init__(self, *patterns):
        # type: (*Union[Text, List[Text]]) -> None
        super(TextRegionSettings, self).__init__(*patterns)
        self._image = None

    def image(self, image):
        # type: (Union[Image, Text]) -> TextRegionSettings
        cloned = self._clone()
        cloned._image = image_path_or_bytes(image)
        return cloned

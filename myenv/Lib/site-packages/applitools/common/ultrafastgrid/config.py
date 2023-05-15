from enum import Enum
from typing import Any, Text

from ..utils.general_utils import DynamicEnumGetter


class ScreenOrientation(Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class DeviceName(Enum):
    BlackBerry_Z30 = "BlackBerry Z30"
    Blackberry_PlayBook = "Blackberry PlayBook"
    Galaxy_A5 = "Galaxy A5"
    Galaxy_Note_10 = "Galaxy Note 10"
    Galaxy_Note_10_Plus = "Galaxy Note 10 Plus"
    Galaxy_Note_2 = "Galaxy Note 2"
    Galaxy_Note_3 = "Galaxy Note 3"
    Galaxy_Note_4 = "Galaxy Note 4"
    Galaxy_Note_8 = "Galaxy Note 8"
    Galaxy_Note_9 = "Galaxy Note 9"
    Galaxy_S10 = "Galaxy S10"
    Galaxy_S10_Plus = "Galaxy S10 Plus"
    Galaxy_S20 = "Galaxy S20"
    Galaxy_S22 = "Galaxy S22"
    Galaxy_S3 = "Galaxy S3"
    Galaxy_S5 = "Galaxy S5"
    Galaxy_S8 = "Galaxy S8"
    Galaxy_S8_Plus = "Galaxy S8 Plus"
    Galaxy_S9 = "Galaxy S9"
    Galaxy_S9_Plus = "Galaxy S9 Plus"
    Galaxy_Tab_S7 = "Galaxy Tab S7"
    Huawei_Mate_50_Pro = "Huawei Mate 50 Pro"
    Huawei_Matepad_11 = "Huawei Matepad 11"
    Kindle_Fire_HDX = "Kindle Fire HDX"
    LG_G6 = "LG G6"
    LG_Optimus_L70 = "LG Optimus L70"
    Laptop_with_HiDPI_screen = "Laptop with HiDPI screen"
    Laptop_with_MDPI_screen = "Laptop with MDPI screen"
    Laptop_with_touch = "Laptop with touch"
    Microsoft_Lumia_550 = "Microsoft Lumia 550"
    Microsoft_Lumia_950 = "Microsoft Lumia 950"
    Nexus_10 = "Nexus 10"
    Nexus_4 = "Nexus 4"
    Nexus_5 = "Nexus 5"
    Nexus_5X = "Nexus 5X"
    Nexus_6 = "Nexus 6"
    Nexus_6P = "Nexus 6P"
    Nexus_7 = "Nexus 7"
    Nokia_Lumia_520 = "Nokia Lumia 520"
    Nokia_N9 = "Nokia N9"
    OnePlus_7T = "OnePlus 7T"
    OnePlus_7T_Pro = "OnePlus 7T Pro"
    Pixel_2 = "Pixel 2"
    Pixel_2_XL = "Pixel 2 XL"
    Pixel_3 = "Pixel 3"
    Pixel_3_XL = "Pixel 3 XL"
    Pixel_4 = "Pixel 4"
    Pixel_4_XL = "Pixel 4 XL"
    Pixel_5 = "Pixel 5"
    Sony_Xperia_10_II = "Sony Xperia 10 II"
    iPad = "iPad"
    iPad_6th_Gen = "iPad 6th Gen"
    iPad_7th_Gen = "iPad 7th Gen"
    iPad_Air_2 = "iPad Air 2"
    iPad_Mini = "iPad Mini"
    iPad_Pro = "iPad Pro"
    iPhone_11 = "iPhone 11"
    iPhone_11_Pro = "iPhone 11 Pro"
    iPhone_11_Pro_Max = "iPhone 11 Pro Max"
    iPhone_4 = "iPhone 4"
    iPhone_5SE = "iPhone 5/SE"
    iPhone_6_7_8 = "iPhone 6/7/8"
    iPhone_6_7_8_Plus = "iPhone 6/7/8 Plus"
    iPhone_X = "iPhone X"
    iPhone_XR = "iPhone XR"
    iPhone_XS = "iPhone XS"
    iPhone_XS_Max = "iPhone XS Max"


class AndroidVersion(Enum):
    LATEST = "latest"
    ONE_VERSION_BACK = "latest-1"


class IosVersion(Enum):
    LATEST = "latest"
    ONE_VERSION_BACK = "latest-1"


class AndroidDeviceName(Enum):
    Galaxy_Note_10 = "Galaxy Note 10"
    Galaxy_Note_10_Plus = "Galaxy Note 10 Plus"
    Galaxy_S10 = "Galaxy S10"
    Galaxy_S10_Plus = "Galaxy S10 Plus"
    Galaxy_S20 = "Galaxy S20"
    Galaxy_S20_Plus = "Galaxy S20 Plus"
    Galaxy_S21 = "Galaxy S21"
    Galaxy_S21_Plus = "Galaxy S21 Plus"
    Galaxy_S21_Ultra = "Galaxy S21 Ultra"
    Galaxy_S22 = "Galaxy S22"
    Galaxy_S22_Plus = "Galaxy S22 Plus"
    Galaxy_Tab_S7 = "Galaxy Tab S7"
    Galaxy_Tab_S8 = "Galaxy Tab S8"
    Huawei_P30_Lite = "Huawei P30 Lite"
    Pixel_3_XL = "Pixel 3 XL"
    Pixel_4 = "Pixel 4"
    Pixel_4_XL = "Pixel 4 XL"
    Pixel_5 = "Pixel 5"
    Pixel_6 = "Pixel 6"
    Sony_Xperia_10_II = "Sony Xperia 10 II"
    Sony_Xperia_1_II = "Sony Xperia 1 II"
    Sony_Xperia_Ace_II = "Sony Xperia Ace II"
    Xiaomi_Redmi_Note_10_JE = "Xiaomi Redmi Note 10 JE"
    Xiaomi_Redmi_Note_11 = "Xiaomi Redmi Note 11"
    Xiaomi_Redmi_Note_11_Pro = "Xiaomi Redmi Note 11 Pro"

    # historical aliases
    @DynamicEnumGetter
    def Galaxy_S20_PLUS(self):
        return AndroidDeviceName.Galaxy_S20_Plus

    @DynamicEnumGetter
    def Galaxy_S21_PLUS(self):
        return AndroidDeviceName.Galaxy_S21_Plus

    @DynamicEnumGetter
    def Galaxy_S21_ULTRA(self):
        return AndroidDeviceName.Galaxy_S21_Ultra


class IosDeviceName(Enum):
    iPad_7 = "iPad (7th generation)"
    iPad_9 = "iPad (9th generation)"
    iPad_Air_2 = "iPad Air (2nd generation)"
    iPad_Air_4 = "iPad Air (4th generation)"
    iPad_Pro_3 = "iPad Pro (12.9-inch) (3rd generation)"
    iPad_Pro_4 = "iPad Pro (11-inch) (4th generation)"
    iPhone_11 = "iPhone 11"
    iPhone_11_Pro = "iPhone 11 Pro"
    iPhone_11_Pro_Max = "iPhone 11 Pro Max"
    iPhone_12 = "iPhone 12"
    iPhone_12_Pro = "iPhone 12 Pro"
    iPhone_12_Pro_Max = "iPhone 12 Pro Max"
    iPhone_12_mini = "iPhone 12 mini"
    iPhone_13 = "iPhone 13"
    iPhone_13_Pro = "iPhone 13 Pro"
    iPhone_13_Pro_Max = "iPhone 13 Pro Max"
    iPhone_14 = "iPhone 14"
    iPhone_14_Pro_Max = "iPhone 14 Pro Max"
    iPhone_7 = "iPhone 7"
    iPhone_8 = "iPhone 8"
    iPhone_8_Plus = "iPhone 8 Plus"
    iPhone_SE = "iPhone SE (1st generation)"
    iPhone_X = "iPhone X"
    iPhone_XR = "iPhone XR"
    iPhone_XS = "iPhone Xs"


class VisualGridOption(object):
    def __init__(self, key, value):
        # type: (Text, Any) -> None
        self.key = key
        self.value = value

    def __eq__(self, other):
        # type: (VisualGridOption) -> bool
        return other and self.key == other.key and self.value == other.value
